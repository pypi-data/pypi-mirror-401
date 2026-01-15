# models/base/gs.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence, Union

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from torch.optim import Adam
from torch_geometric.data import Data
from torch_geometric.nn import SAGEConv

from .gnn_utils import build_samplewise_graph


ArrayLike = Union[np.ndarray, pd.DataFrame]


@dataclass
class GraphSAGEConfig:
    # graph
    n_neighbors: int = 4

    # model
    hidden_dim: int = 64
    num_layers: int = 3
    dropout: float = 0.2

    # optimization
    lr: float = 1e-3
    weight_decay: float = 1e-4
    epochs: int = 200

    # runtime
    device: Optional[str] = None  # None -> auto
    dtype: str = "float32"
    verbose: bool = False


class _GraphSAGE(torch.nn.Module):
    def __init__(self, in_feats: int, hidden_dim: int, out_feats: int, num_layers: int, dropout: float):
        super().__init__()
        self.dropout = dropout

        if num_layers < 2:
            raise ValueError("GraphSAGE num_layers must be >= 2.")

        self.convs = torch.nn.ModuleList([SAGEConv(in_feats, hidden_dim)])
        for _ in range(num_layers - 2):
            self.convs.append(SAGEConv(hidden_dim, hidden_dim))
        self.convs.append(SAGEConv(hidden_dim, out_feats))

    def forward(self, x: torch.Tensor, edge_index: torch.Tensor) -> torch.Tensor:
        for conv in self.convs[:-1]:
            x = conv(x, edge_index)
            x = F.relu(x)
            x = F.dropout(x, p=self.dropout, training=self.training)
        return self.convs[-1](x, edge_index)


class GraphSAGEBaseModel:
    """
    GraphSAGE base model for SR2P.

    This is transductive inference:
      - build sample-wise train graphs
      - build sample-wise test graphs
      - concatenate into one big graph
      - predict on test nodes

    fit:
        fit(X_train, Y_train_df, coords_train_df, protein_names=None)

    predict:
        predict(X_test, coords_test_df) -> DataFrame (n_test, n_proteins)

    Notes:
      - coords_df must include columns: sample_id, x, y
      - X rows should align with coords_df index; if X is DataFrame we align by index.
    """

    def __init__(self, cfg: Optional[GraphSAGEConfig] = None):
        self.cfg = cfg or GraphSAGEConfig()
        self.device = torch.device(self.cfg.device) if self.cfg.device else torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        self.model: Optional[_GraphSAGE] = None
        self.protein_names_: Optional[list[str]] = None

        # cached train graph
        self._x_train: Optional[torch.Tensor] = None
        self._edge_train: Optional[torch.Tensor] = None
        self._y_train: Optional[torch.Tensor] = None

    @staticmethod
    def _to_numpy(X: ArrayLike) -> np.ndarray:
        if isinstance(X, pd.DataFrame):
            return X.to_numpy()
        return np.asarray(X)

    @staticmethod
    def _align_X_to_coords(X: ArrayLike, coords_df: pd.DataFrame) -> np.ndarray:
        if isinstance(X, pd.DataFrame):
            # align by index to avoid subtle mis-order bugs
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
    ) -> "GraphSAGEBaseModel":
        X_arr = self._align_X_to_coords(X_train, coords_train).astype(self.cfg.dtype, copy=False)
        Y_arr, protein_names_list = self._align_Y_to_coords(Y_train, coords_train, protein_names)
        Y_arr = Y_arr.astype(self.cfg.dtype, copy=False)

        self.protein_names_ = protein_names_list

        # build train graph
        x_train, edge_train = build_samplewise_graph(
            X_arr,
            coords_train,
            sample_col="sample_id",
            x_col="x",
            y_col="y",
            n_neighbors=self.cfg.n_neighbors,
            bidirectional=True,
            include_self=False,
        )

        y_train = torch.tensor(Y_arr, dtype=torch.float32)

        self._x_train = x_train
        self._edge_train = edge_train
        self._y_train = y_train

        # init model
        self.model = _GraphSAGE(
            in_feats=x_train.shape[1],
            hidden_dim=self.cfg.hidden_dim,
            out_feats=Y_arr.shape[1],
            num_layers=self.cfg.num_layers,
            dropout=self.cfg.dropout,
        ).to(self.device)

        data = Data(x=x_train, y=y_train, edge_index=edge_train)
        data.train_mask = torch.ones(x_train.shape[0], dtype=torch.bool)
        data = data.to(self.device)

        optimizer = Adam(self.model.parameters(), lr=self.cfg.lr, weight_decay=self.cfg.weight_decay)

        self.model.train()
        for epoch in range(self.cfg.epochs):
            optimizer.zero_grad()
            out = self.model(data.x, data.edge_index)
            loss = F.mse_loss(out[data.train_mask], data.y[data.train_mask])
            loss.backward()
            optimizer.step()

            if self.cfg.verbose and (epoch == 0 or (epoch + 1) % 50 == 0 or (epoch + 1) == self.cfg.epochs):
                print(f"[GraphSAGE] epoch {epoch+1}/{self.cfg.epochs} loss={loss.item():.6f}")

        return self

    @torch.no_grad()
    def predict(self, X_test: ArrayLike, coords_test: pd.DataFrame) -> pd.DataFrame:
        if self.model is None:
            raise RuntimeError("GraphSAGEBaseModel.predict() called before fit().")
        if self._x_train is None or self._edge_train is None or self._y_train is None:
            raise RuntimeError("Internal train graph not found. Call fit() first.")
        if self.protein_names_ is None:
            raise RuntimeError("protein_names_ not found. Call fit() first.")

        X_te = self._align_X_to_coords(X_test, coords_test).astype(self.cfg.dtype, copy=False)

        self.model.eval()

        x_test, edge_test = build_samplewise_graph(
            X_te,
            coords_test,
            sample_col="sample_id",
            x_col="x",
            y_col="y",
            n_neighbors=self.cfg.n_neighbors,
            bidirectional=True,
            include_self=False,
        )

        # full graph = train + test
        x_full = torch.cat([self._x_train, x_test], dim=0)

        # pad y for test nodes (dummy)
        y_pad = torch.zeros((x_test.shape[0], self._y_train.shape[1]), dtype=torch.float32)
        y_full = torch.cat([self._y_train, y_pad], dim=0)

        # shift test edges
        edge_test = edge_test + self._x_train.shape[0]
        edge_full = torch.cat([self._edge_train, edge_test], dim=1)

        train_mask = torch.zeros(x_full.shape[0], dtype=torch.bool)
        test_mask = torch.zeros(x_full.shape[0], dtype=torch.bool)
        train_mask[: self._x_train.shape[0]] = True
        test_mask[self._x_train.shape[0] :] = True

        data = Data(x=x_full, y=y_full, edge_index=edge_full)
        data.train_mask = train_mask
        data.test_mask = test_mask
        data = data.to(self.device)

        out = self.model(data.x, data.edge_index).detach().cpu().numpy()
        preds = out[data.test_mask.cpu().numpy()]

        return pd.DataFrame(preds, index=coords_test.index, columns=self.protein_names_)

    def get_params(self) -> dict:
        return {
            "n_neighbors": self.cfg.n_neighbors,
            "hidden_dim": self.cfg.hidden_dim,
            "num_layers": self.cfg.num_layers,
            "dropout": self.cfg.dropout,
            "lr": self.cfg.lr,
            "weight_decay": self.cfg.weight_decay,
            "epochs": self.cfg.epochs,
            "device": str(self.device),
            "dtype": self.cfg.dtype,
        }
