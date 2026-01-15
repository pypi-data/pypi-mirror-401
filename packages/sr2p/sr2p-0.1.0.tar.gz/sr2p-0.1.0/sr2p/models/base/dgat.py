# models/base/dgat.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence, Union

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F

from torch_geometric.nn import GATConv

from .gnn_utils import build_samplewise_dual_graphs


ArrayLike = Union[np.ndarray, pd.DataFrame]


@dataclass
class DGATConfig:
    # graph
    n_spatial: int = 4
    n_expr: int = 6

    # model
    hidden_dim: int = 64
    heads: int = 4
    num_layers: int = 3
    dropout: float = 0.2

    # optimization
    epochs: int = 200
    lr: float = 1e-3
    weight_decay: float = 1e-4
    lambda_recon: float = 0.3  # reconstruction loss weight

    # runtime
    device: Optional[str] = None  # None -> auto
    dtype: str = "float32"
    verbose: bool = False


class _DualGraphGAT(nn.Module):
    def __init__(
        self,
        in_feats: int,
        hidden_dim: int,
        out_prots: int,
        *,
        heads: int,
        num_layers: int,
        dropout: float,
    ):
        super().__init__()
        if num_layers < 1:
            raise ValueError("DGAT num_layers must be >= 1.")

        self.num_layers = num_layers
        self.dropout = dropout

        self.s_convs = nn.ModuleList()
        self.e_convs = nn.ModuleList()
        self.gates = nn.ParameterList()

        in_dim = in_feats
        for _ in range(num_layers):
            self.s_convs.append(GATConv(in_dim, hidden_dim, heads=heads, concat=True))
            self.e_convs.append(GATConv(in_dim, hidden_dim, heads=heads, concat=True))
            self.gates.append(nn.Parameter(torch.tensor(0.5)))
            in_dim = hidden_dim * heads  # concat=True

        self.protein_head = nn.Sequential(
            nn.Linear(in_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, out_prots),
        )
        self.rna_recon = nn.Sequential(
            nn.Linear(in_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, in_feats),
        )

    def forward(self, x: torch.Tensor, edge_spatial: torch.Tensor, edge_expr: torch.Tensor):
        h = x
        for l in range(self.num_layers):
            hs = self.s_convs[l](h, edge_spatial)
            he = self.e_convs[l](h, edge_expr)
            g = torch.sigmoid(self.gates[l])
            h = g * hs + (1.0 - g) * he

            if l < self.num_layers - 1:
                h = F.elu(h)
                h = F.dropout(h, p=self.dropout, training=self.training)

        z = h
        prot_pred = self.protein_head(z)
        rna_hat = self.rna_recon(z)
        return prot_pred, rna_hat, z


class DGATBaseModel:
    """
    DGAT-style Dual-Graph GAT base model for SR2P.

    Transductive inference:
      - build dual graphs for train
      - build dual graphs for test
      - concatenate into one big dual-graph
      - predict on test nodes

    fit:
        fit(X_train, Y_train_df, coords_train_df, protein_names=None)

    predict:
        predict(X_test, coords_test_df) -> DataFrame (n_test, n_proteins)

    Notes:
      - coords_df must include columns: sample_id, x, y
      - X rows should align with coords_df index; if X is DataFrame we align by index.
    """

    def __init__(self, cfg: Optional[DGATConfig] = None):
        self.cfg = cfg or DGATConfig()
        self.device = torch.device(self.cfg.device) if self.cfg.device else torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        self.model: Optional[_DualGraphGAT] = None
        self.protein_names_: Optional[list[str]] = None

        # cached train graph
        self._x_train: Optional[torch.Tensor] = None
        self._e_sp_train: Optional[torch.Tensor] = None
        self._e_ex_train: Optional[torch.Tensor] = None
        self._y_train: Optional[torch.Tensor] = None

    @staticmethod
    def _align_X_to_coords(X: ArrayLike, coords_df: pd.DataFrame) -> np.ndarray:
        if isinstance(X, pd.DataFrame):
            return X.loc[coords_df.index].to_numpy()
        return np.asarray(X)

    @staticmethod
    def _align_Y_to_coords(
        Y: Union[pd.DataFrame, np.ndarray],
        coords_df: pd.DataFrame,
        protein_names: Optional[Sequence[str]],
    ) -> tuple[np.ndarray, list[str]]:
        if isinstance(Y, pd.DataFrame):
            Y_df = Y.loc[coords_df.index]
            return Y_df.to_numpy(), list(Y_df.columns)

        if protein_names is None:
            raise ValueError("protein_names must be provided when Y is ndarray.")
        return np.asarray(Y), list(protein_names)

    def fit(
        self,
        X_train: ArrayLike,
        Y_train: Union[pd.DataFrame, np.ndarray],
        coords_train: pd.DataFrame,
        protein_names: Optional[Sequence[str]] = None,
    ) -> "DGATBaseModel":
        X_arr = self._align_X_to_coords(X_train, coords_train).astype(self.cfg.dtype, copy=False)
        Y_arr, protein_names_list = self._align_Y_to_coords(Y_train, coords_train, protein_names)
        Y_arr = Y_arr.astype(self.cfg.dtype, copy=False)

        self.protein_names_ = protein_names_list

        x_tr, e_sp_tr, e_ex_tr = build_samplewise_dual_graphs(
            X_arr,
            coords_train,
            sample_col="sample_id",
            x_col="x",
            y_col="y",
            n_spatial=self.cfg.n_spatial,
            n_expr=self.cfg.n_expr,
            bidirectional=True,
            include_self=False,
        )

        y_tr = torch.tensor(Y_arr, dtype=torch.float32)

        self._x_train = x_tr
        self._e_sp_train = e_sp_tr
        self._e_ex_train = e_ex_tr
        self._y_train = y_tr

        self.model = _DualGraphGAT(
            in_feats=x_tr.shape[1],
            hidden_dim=self.cfg.hidden_dim,
            out_prots=Y_arr.shape[1],
            heads=self.cfg.heads,
            num_layers=self.cfg.num_layers,
            dropout=self.cfg.dropout,
        ).to(self.device)

        optimizer = torch.optim.Adam(self.model.parameters(), lr=self.cfg.lr, weight_decay=self.cfg.weight_decay)

        # all nodes are train nodes here (train-only graph)
        train_mask = torch.ones(x_tr.shape[0], dtype=torch.bool, device=self.device)

        x_tr = x_tr.to(self.device)
        e_sp_tr = e_sp_tr.to(self.device)
        e_ex_tr = e_ex_tr.to(self.device)
        y_tr = y_tr.to(self.device)

        for epoch in range(self.cfg.epochs):
            self.model.train()
            optimizer.zero_grad()

            prot_pred, rna_hat, _ = self.model(x_tr, e_sp_tr, e_ex_tr)
            loss_prot = F.mse_loss(prot_pred[train_mask], y_tr)
            loss_recon = F.mse_loss(rna_hat[train_mask], x_tr[train_mask])
            loss = loss_prot + self.cfg.lambda_recon * loss_recon

            loss.backward()
            optimizer.step()

            if self.cfg.verbose and (epoch == 0 or (epoch + 1) % 50 == 0 or (epoch + 1) == self.cfg.epochs):
                print(
                    f"[DGAT] epoch {epoch+1}/{self.cfg.epochs} "
                    f"loss={loss.item():.6f} prot={loss_prot.item():.6f} recon={loss_recon.item():.6f}"
                )

        return self

    @torch.no_grad()
    def predict(self, X_test: ArrayLike, coords_test: pd.DataFrame) -> pd.DataFrame:
        if self.model is None:
            raise RuntimeError("DGATBaseModel.predict() called before fit().")
        if self._x_train is None or self._e_sp_train is None or self._e_ex_train is None or self._y_train is None:
            raise RuntimeError("Internal train graph not found. Call fit() first.")
        if self.protein_names_ is None:
            raise RuntimeError("protein_names_ not found. Call fit() first.")

        X_te = self._align_X_to_coords(X_test, coords_test).astype(self.cfg.dtype, copy=False)

        self.model.eval()

        x_te, e_sp_te, e_ex_te = build_samplewise_dual_graphs(
            X_te,
            coords_test,
            sample_col="sample_id",
            x_col="x",
            y_col="y",
            n_spatial=self.cfg.n_spatial,
            n_expr=self.cfg.n_expr,
            bidirectional=True,
            include_self=False,
        )

        # concat full graph
        x_full = torch.cat([self._x_train, x_te], dim=0)

        # shift test edges
        offset = self._x_train.shape[0]
        e_sp_te = e_sp_te + offset
        e_ex_te = e_ex_te + offset

        e_sp_full = torch.cat([self._e_sp_train, e_sp_te], dim=1)
        e_ex_full = torch.cat([self._e_ex_train, e_ex_te], dim=1)

        test_mask = torch.zeros(x_full.shape[0], dtype=torch.bool)
        test_mask[offset:] = True

        x_full = x_full.to(self.device)
        e_sp_full = e_sp_full.to(self.device)
        e_ex_full = e_ex_full.to(self.device)
        test_mask = test_mask.to(self.device)

        prot_pred, _, _ = self.model(x_full, e_sp_full, e_ex_full)
        preds = prot_pred[test_mask].detach().cpu().numpy()

        return pd.DataFrame(preds, index=coords_test.index, columns=self.protein_names_)

    def get_params(self) -> dict:
        return {
            "n_spatial": self.cfg.n_spatial,
            "n_expr": self.cfg.n_expr,
            "hidden_dim": self.cfg.hidden_dim,
            "heads": self.cfg.heads,
            "num_layers": self.cfg.num_layers,
            "dropout": self.cfg.dropout,
            "epochs": self.cfg.epochs,
            "lr": self.cfg.lr,
            "weight_decay": self.cfg.weight_decay,
            "lambda_recon": self.cfg.lambda_recon,
            "device": str(self.device),
            "dtype": self.cfg.dtype,
        }
