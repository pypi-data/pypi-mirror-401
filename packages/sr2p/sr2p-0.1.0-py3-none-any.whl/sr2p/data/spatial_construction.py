# sr2p/data/spatial_construction.py
from __future__ import annotations

from typing import Callable, List, Tuple, Optional, Any

import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors


def make_expand_fn_within_sample_fixed_neighbours(
    X_data: np.ndarray,
    coords_df: pd.DataFrame,
    *,
    sample_col: str = "sample_id",
    x_col: str = "x",
    y_col: str = "y",
    neighbor_feats: int = 5,
    grid_step: int = 2,
    knn_pool_multiplier: int = 4,
) -> Callable[[np.ndarray, pd.DataFrame, bool], Tuple[np.ndarray, List[Any]]]:
    """
    Construct spatial augmented features using within sample fixed neighbors.

    Each spot will be expanded to:
        [self_features,
         neighbor_1_features,
         neighbor_2_features,
         neighbor_3_features,
         neighbor_4_features]

    Default neighbor rules:
        (-grid_step, 0), (+grid_step, 0), (0, -grid_step), (0, +grid_step)

    If fixed neighbors are missing, fill from KNN pool within the same sample.

    Parameters
    ----------
    X_data:
        Full feature matrix aligned with coords_df rows.
        Shape: (n_nodes, n_features)
    coords_df:
        DataFrame aligned with X_data rows, must contain:
        [sample_col, x_col, y_col]
    neighbor_feats:
        Must be 5 (self + 4 neighbors) in this implementation.
    grid_step:
        Step size used in fixed neighbor rule. Visium often uses 2.
    knn_pool_multiplier:
        KNN pool size = neighbor_feats * knn_pool_multiplier

    Returns
    -------
    expand_fn:
        expand_fn(X_src, coords_src, is_train) -> (X_expanded, center_indices)
        X_expanded shape: (n_src, n_features * 5)
        center_indices: list of center spot index labels (coords_src.index values)
    """
    if neighbor_feats != 5:
        raise ValueError("neighbor_feats must be 5 (self + 4 fixed neighbors).")

    if not isinstance(coords_df, pd.DataFrame):
        raise TypeError("coords_df must be a pandas DataFrame.")

    required_cols = {sample_col, x_col, y_col}
    missing = required_cols - set(coords_df.columns)
    if missing:
        raise ValueError(f"coords_df missing required columns: {sorted(missing)}")

    X_data = np.asarray(X_data)
    if coords_df.shape[0] != X_data.shape[0]:
        raise ValueError(
            f"X_data and coords_df must have the same number of rows. "
            f"Got X_data={X_data.shape[0]}, coords_df={coords_df.shape[0]}"
        )

    # ------------------------------
    # Precompute per sample lookup and KNN
    # ------------------------------
    index_by_coord = {}
    knn_models = {}
    index_by_sample = {}

    for sid, group_df in coords_df.groupby(sample_col):
        coords = group_df[[x_col, y_col]].values

        # (x, y) -> index label (coords_df.index)
        coord_dict = {(row[x_col], row[y_col]): idx for idx, row in group_df.iterrows()}
        index_by_coord[sid] = coord_dict
        index_by_sample[sid] = group_df.index.to_list()

        n_neighbors = neighbor_feats * knn_pool_multiplier
        n_neighbors = min(n_neighbors, coords.shape[0])  # safety
        knn = NearestNeighbors(n_neighbors=n_neighbors, metric="euclidean").fit(coords)
        knn_models[sid] = knn

    neighbours_rules = [
        (-grid_step, 0),
        (grid_step, 0),
        (0, -grid_step),
        (0, grid_step),
    ]

    def expand(
        X_src: np.ndarray,
        coords_src: pd.DataFrame,
        is_train: bool = True,
    ) -> Tuple[np.ndarray, List[Any]]:
        """
        Expand X_src using coords_src (row aligned).

        Returns
        -------
        X_expanded:
            shape (n_src, n_features * 5)
        center_indices:
            list of coords_src.index labels (original center spot index)
        """
        X_src = np.asarray(X_src)
        if coords_src.shape[0] != X_src.shape[0]:
            raise ValueError(
                f"X_src and coords_src must have the same number of rows. "
                f"Got X_src={X_src.shape[0]}, coords_src={coords_src.shape[0]}"
            )

        mats: List[np.ndarray] = []
        center_indices: List[Any] = []

        for i in range(X_src.shape[0]):
            row = coords_src.iloc[i]
            sid = row[sample_col]
            x = row[x_col]
            y = row[y_col]

            if sid not in index_by_coord:
                raise ValueError(f"sample_id '{sid}' not found in coords_df.")

            coord_dict = index_by_coord[sid]
            knn = knn_models[sid]
            sample_indices = index_by_sample[sid]

            # keep center index label
            center_idx_label = coords_src.index[i]
            center_indices.append(center_idx_label)

            feats = [X_src[i]]
            used_global_pos = set()

            # mark itself used (requires center exists in coords_df.index)
            if center_idx_label in coords_df.index:
                self_pos = coords_df.index.get_loc(center_idx_label)
                used_global_pos.add(self_pos)
            else:
                raise ValueError(
                    f"Center index '{center_idx_label}' not found in coords_df.index. "
                    f"Make sure coords_src is derived from coords_df without resetting index."
                )

            neighbor_feats_list: List[Optional[np.ndarray]] = [None] * 4

            # 1) fixed neighbor lookup
            for k, (dx, dy) in enumerate(neighbours_rules):
                nb_coord = (x + dx, y + dy)
                if nb_coord in coord_dict:
                    nb_idx_label = coord_dict[nb_coord]
                    nb_pos = coords_df.index.get_loc(nb_idx_label)
                    neighbor_feats_list[k] = X_data[nb_pos]
                    used_global_pos.add(nb_pos)

            # 2) knn fallback within sample
            missing_slots = [k for k, v in enumerate(neighbor_feats_list) if v is None]
            if missing_slots:
                this_coord = np.array([[x, y]])
                _, neigh_idx = knn.kneighbors(this_coord)
                pool = neigh_idx[0].tolist()

                for local_pos in pool:
                    candidate_idx_label = sample_indices[local_pos]
                    candidate_global_pos = coords_df.index.get_loc(candidate_idx_label)

                    if candidate_global_pos in used_global_pos:
                        continue

                    k = missing_slots.pop(0)
                    neighbor_feats_list[k] = X_data[candidate_global_pos]
                    used_global_pos.add(candidate_global_pos)

                    if not missing_slots:
                        break

            if any(v is None for v in neighbor_feats_list):
                raise ValueError(
                    f"Spot '{center_idx_label}' in sample '{sid}' "
                    f"cannot find enough neighbors to fill 4 slots."
                )

            feats.extend(neighbor_feats_list)  # type: ignore[arg-type]
            mats.append(np.concatenate(feats, axis=0))

        X_expanded = np.vstack(mats)
        return X_expanded, center_indices

    return expand


def build_fixed_neighbor_concat(
    X_data: np.ndarray,
    coords_df: pd.DataFrame,
    *,
    sample_col: str = "sample_id",
    x_col: str = "x",
    y_col: str = "y",
    grid_step: int = 2,
    knn_pool_multiplier: int = 4,
) -> Tuple[np.ndarray, List[Any]]:
    """
    Convenience wrapper: directly return expanded features for (X_data, coords_df).

    Returns
    -------
    X_expanded, center_indices
    """
    expand_fn = make_expand_fn_within_sample_fixed_neighbours(
        X_data=X_data,
        coords_df=coords_df,
        sample_col=sample_col,
        x_col=x_col,
        y_col=y_col,
        neighbor_feats=5,
        grid_step=grid_step,
        knn_pool_multiplier=knn_pool_multiplier,
    )
    return expand_fn(X_data, coords_df, is_train=True)


def build_fixed_neighbor_concat_df(
    X_df: pd.DataFrame,
    coords_df: pd.DataFrame,
    *,
    sample_col: str = "sample_id",
    x_col: str = "x",
    y_col: str = "y",
    grid_step: int = 2,
    knn_pool_multiplier: int = 4,
    col_prefix: str = "f",
) -> pd.DataFrame:
    """
    Directly return expanded features as a DataFrame with center spot original index.

    Notes
    -----
    - Column names are auto generated: f0_self, f1_self, ... then f0_nb1, ...
      If you want gene based names, you can pass X_df with gene columns and adapt naming.
    """
    X_expanded, center_indices = build_fixed_neighbor_concat(
        X_data=X_df.values,
        coords_df=coords_df,
        sample_col=sample_col,
        x_col=x_col,
        y_col=y_col,
        grid_step=grid_step,
        knn_pool_multiplier=knn_pool_multiplier,
    )

    n_feat = X_df.shape[1]
    base_names = list(X_df.columns) if X_df.columns is not None else [f"{col_prefix}{i}" for i in range(n_feat)]

    # self + 4 neighbors
    suffixes = ["self", "nb1", "nb2", "nb3", "nb4"]
    cols = [f"{name}_{suf}" for suf in suffixes for name in base_names]

    return pd.DataFrame(X_expanded, index=pd.Index(center_indices), columns=cols)
