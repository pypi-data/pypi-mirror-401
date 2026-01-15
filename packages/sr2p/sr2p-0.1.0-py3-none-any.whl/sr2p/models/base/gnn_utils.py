# models/base/gnn_utils.py
from __future__ import annotations

from typing import Tuple

import numpy as np
import pandas as pd
import torch
from sklearn.neighbors import NearestNeighbors


def _safe_knn_indices(
    data: np.ndarray,
    *,
    n_neighbors: int,
    metric: str = "euclidean",
) -> np.ndarray:
    """
    Return neighbor indices for each row.
    This function automatically clamps n_neighbors to <= n_samples.
    """
    n = data.shape[0]
    if n == 0:
        return np.zeros((0, 0), dtype=int)

    k = min(int(n_neighbors), n)
    knn = NearestNeighbors(n_neighbors=k, metric=metric).fit(data)
    _, nbrs = knn.kneighbors(data)
    return nbrs


def build_samplewise_graph(
    X_data: np.ndarray,
    coords_df: pd.DataFrame,
    *,
    sample_col: str = "sample_id",
    x_col: str = "x",
    y_col: str = "y",
    n_neighbors: int = 4,
    bidirectional: bool = True,
    include_self: bool = False,
) -> Tuple[torch.Tensor, torch.Tensor]:
    """
    Build a spatial kNN graph within each sample.

    IMPORTANT:
      - X_data row order must match coords_df row order.
      - coords_df must contain columns: sample_col, x_col, y_col.

    Returns
    -------
    x:
        (n_nodes, n_features) torch.float32
    edge_index:
        (2, n_edges) torch.long
    """
    if X_data.shape[0] != coords_df.shape[0]:
        raise ValueError(
            f"X_data rows ({X_data.shape[0]}) must match coords_df rows ({coords_df.shape[0]})."
        )

    x_all = []
    edge_indices = []
    base_idx = 0

    # preserve sample iteration order as they appear
    for sid in coords_df[sample_col].unique():
        group = coords_df[coords_df[sample_col] == sid]
        if group.shape[0] == 0:
            continue

        # positions in the global table (preserve order)
        pos = np.flatnonzero((coords_df[sample_col] == sid).to_numpy())
        coords = coords_df.iloc[pos][[x_col, y_col]].to_numpy()
        Xs = X_data[pos]

        nbrs = _safe_knn_indices(coords, n_neighbors=n_neighbors, metric="euclidean")

        edges = []
        for i, neigh in enumerate(nbrs):
            # drop self if requested and if it exists
            neigh_iter = neigh if include_self else neigh[1:] if neigh.shape[0] > 1 else []
            for j in neigh_iter:
                edges.append([i, int(j)])
                if bidirectional:
                    edges.append([int(j), i])

        edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()
        if edge_index.numel() > 0:
            edge_index = edge_index + base_idx
        else:
            edge_index = torch.empty((2, 0), dtype=torch.long)

        x_all.append(torch.tensor(Xs, dtype=torch.float32))
        edge_indices.append(edge_index)

        base_idx += Xs.shape[0]

    x = torch.cat(x_all, dim=0) if x_all else torch.empty((0, X_data.shape[1]), dtype=torch.float32)
    edge_index = (
        torch.cat(edge_indices, dim=1) if edge_indices else torch.empty((2, 0), dtype=torch.long)
    )
    return x, edge_index


def build_samplewise_dual_graphs(
    X_data: np.ndarray,
    coords_df: pd.DataFrame,
    *,
    sample_col: str = "sample_id",
    x_col: str = "x",
    y_col: str = "y",
    n_spatial: int = 4,
    n_expr: int = 6,
    bidirectional: bool = True,
    include_self: bool = False,
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """
    Build two graphs within each sample:
      - spatial kNN graph (based on coordinates)
      - expression kNN graph (based on X features)

    IMPORTANT:
      - X_data row order must match coords_df row order.

    Returns
    -------
    x:
        (n_nodes, n_features) torch.float32
    edge_spatial:
        (2, n_edges_s) torch.long
    edge_expr:
        (2, n_edges_e) torch.long
    """
    if X_data.shape[0] != coords_df.shape[0]:
        raise ValueError(
            f"X_data rows ({X_data.shape[0]}) must match coords_df rows ({coords_df.shape[0]})."
        )

    x_all, e_sp_all, e_ex_all = [], [], []
    base_idx = 0

    for sid in coords_df[sample_col].unique():
        pos = np.flatnonzero((coords_df[sample_col] == sid).to_numpy())
        if pos.size == 0:
            continue

        coords = coords_df.iloc[pos][[x_col, y_col]].to_numpy()
        Xs = X_data[pos]

        # spatial knn (coords)
        nbrs_s = _safe_knn_indices(coords, n_neighbors=n_spatial, metric="euclidean")
        edges_s = []
        for i, neigh in enumerate(nbrs_s):
            neigh_iter = neigh if include_self else neigh[1:] if neigh.shape[0] > 1 else []
            for j in neigh_iter:
                edges_s.append([i, int(j)])
                if bidirectional:
                    edges_s.append([int(j), i])
        edge_sp = torch.tensor(edges_s, dtype=torch.long).t().contiguous()
        edge_sp = edge_sp + base_idx if edge_sp.numel() > 0 else torch.empty((2, 0), dtype=torch.long)

        # expr knn (Xs)
        nbrs_e = _safe_knn_indices(Xs, n_neighbors=n_expr, metric="euclidean")
        edges_e = []
        for i, neigh in enumerate(nbrs_e):
            neigh_iter = neigh if include_self else neigh[1:] if neigh.shape[0] > 1 else []
            for j in neigh_iter:
                edges_e.append([i, int(j)])
                if bidirectional:
                    edges_e.append([int(j), i])
        edge_ex = torch.tensor(edges_e, dtype=torch.long).t().contiguous()
        edge_ex = edge_ex + base_idx if edge_ex.numel() > 0 else torch.empty((2, 0), dtype=torch.long)

        x_all.append(torch.tensor(Xs, dtype=torch.float32))
        e_sp_all.append(edge_sp)
        e_ex_all.append(edge_ex)

        base_idx += Xs.shape[0]

    x = torch.cat(x_all, dim=0) if x_all else torch.empty((0, X_data.shape[1]), dtype=torch.float32)
    edge_spatial = torch.cat(e_sp_all, dim=1) if e_sp_all else torch.empty((2, 0), dtype=torch.long)
    edge_expr = torch.cat(e_ex_all, dim=1) if e_ex_all else torch.empty((2, 0), dtype=torch.long)

    return x, edge_spatial, edge_expr
