# stacking/base_learner.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Tuple, List, Any, Union

import os
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold

# ----------------------------
# Types
# ----------------------------
NDArray = np.ndarray


# ----------------------------
# Config
# ----------------------------
@dataclass
class BaseLearnerRunnerConfig:
    n_splits: int = 5
    shuffle: bool = True
    random_state: int = 42

    # memory / io
    dtype: str = "float32"  # float32 saves memory
    cache_dir: Optional[str] = None  # if provided -> save per model oof/test csv

    # speed
    verbose: int = 1


# ----------------------------
# Helpers
# ----------------------------
def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _to_dtype(arr: NDArray, dtype: str) -> NDArray:
    return np.asarray(arr).astype(dtype, copy=False)


def _as_df(
    arr: NDArray,
    index: pd.Index,
    columns: List[str],
    dtype: str,
) -> pd.DataFrame:
    arr = _to_dtype(arr, dtype)
    return pd.DataFrame(arr, index=index, columns=columns)


def _save_if_needed(df: pd.DataFrame, path: Optional[str]) -> None:
    if path is None:
        return
    _ensure_dir(os.path.dirname(path))
    df.to_csv(path)


def _prefix_columns(df: pd.DataFrame, prefix: str) -> pd.DataFrame:
    # prefix + "_" to be consistent with your previous convention
    return df.add_prefix(f"{prefix}_")


# ----------------------------
# Base model spec
# ----------------------------
@dataclass
class BaseModelSpec:
    """
    One base learner entry.

    name:
        used as prefix in meta features.

    model:
        must provide:
          - fit(...)
          - predict(...)

    feature_kind:
        "plain"   -> use X_train / X_test
        "spatial" -> use X_train_spatial / X_test_spatial

    requires_coords:
        if True, fit/predict will receive coords_train/coords_test.
        (used by GNN models)
    """
    name: str
    model: Any
    feature_kind: str = "plain"  # "plain" | "spatial"
    requires_coords: bool = False


# ----------------------------
# Main runner
# ----------------------------
class BaseLearnerRunner:
    """
    Run OOF + test predictions for a list of base learners, and build meta features.

    Expected inputs:
      - X_train: (n_train, n_genes)
      - Y_train: (n_train, n_prots)  [array or DataFrame]
      - X_test:  (n_test, n_genes)
      - protein_names: list[str]
      - train_index/test_index: pandas index (spot ids)

    Optional spatial features:
      - X_train_spatial: (n_train, 5*n_genes)  (your fixed-neighbor concat)
      - X_test_spatial:  (n_test, 5*n_genes)

    Optional coords:
      - coords_train/coords_test: DataFrame with columns [sample_id, x, y]
        aligned to X rows order.
    """

    def __init__(self, cfg: Optional[BaseLearnerRunnerConfig] = None):
        self.cfg = cfg or BaseLearnerRunnerConfig()
        self.base_models: List[BaseModelSpec] = []

    def add_model(self, spec: BaseModelSpec) -> None:
        if spec.feature_kind not in ("plain", "spatial"):
            raise ValueError(f"feature_kind must be 'plain' or 'spatial', got {spec.feature_kind}")
        self.base_models.append(spec)

    def run(
        self,
        *,
        X_train: NDArray,
        Y_train: Union[NDArray, pd.DataFrame],
        X_test: NDArray,
        protein_names: List[str],
        train_index: pd.Index,
        test_index: pd.Index,
        # spatial features (optional)
        X_train_spatial: Optional[NDArray] = None,
        X_test_spatial: Optional[NDArray] = None,
        # coords (optional, required for gnn specs)
        coords_train: Optional[pd.DataFrame] = None,
        coords_test: Optional[pd.DataFrame] = None,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Returns
        -------
        meta_X_train: DataFrame (n_train, n_base * n_prots) with prefixed columns
        meta_X_test:  DataFrame (n_test,  n_base * n_prots)
        """
        if len(self.base_models) == 0:
            raise ValueError("No base models added. Call add_model() first.")

        X_train = np.asarray(X_train)
        X_test = np.asarray(X_test)

        if isinstance(Y_train, pd.DataFrame):
            Y_arr = Y_train[protein_names].values
        else:
            Y_arr = np.asarray(Y_train)

        n_train = X_train.shape[0]
        n_test = X_test.shape[0]
        n_prots = len(protein_names)

        if Y_arr.shape[0] != n_train or Y_arr.shape[1] != n_prots:
            raise ValueError(f"Y_train shape must be (n_train, n_prots)=({n_train},{n_prots}), got {Y_arr.shape}")

        # check spatial features if needed
        any_spatial = any(m.feature_kind == "spatial" for m in self.base_models)
        if any_spatial:
            if X_train_spatial is None or X_test_spatial is None:
                raise ValueError("Some base models require spatial features, but X_train_spatial/X_test_spatial is None.")

        # check coords if needed
        any_coords = any(m.requires_coords for m in self.base_models)
        if any_coords:
            if coords_train is None or coords_test is None:
                raise ValueError("Some base models require coords, but coords_train/coords_test is None.")

        kf = KFold(
            n_splits=self.cfg.n_splits,
            shuffle=self.cfg.shuffle,
            random_state=self.cfg.random_state,
        )

        meta_train_parts: List[pd.DataFrame] = []
        meta_test_parts: List[pd.DataFrame] = []

        cache_dir = self.cfg.cache_dir
        if cache_dir is not None:
            _ensure_dir(cache_dir)

        # ----------------------------
        # run each base model
        # ----------------------------
        for spec in self.base_models:
            if self.cfg.verbose:
                print(f"\n[BaseLearner] Running: {spec.name} (kind={spec.feature_kind}, coords={spec.requires_coords})")

            # pick features
            if spec.feature_kind == "plain":
                Xtr_all = X_train
                Xte_all = X_test
            else:
                assert X_train_spatial is not None and X_test_spatial is not None
                Xtr_all = X_train_spatial
                Xte_all = X_test_spatial

            # allocate
            oof = np.zeros((n_train, n_prots), dtype=self.cfg.dtype)
            test_fold_preds: List[NDArray] = []

            # OOF folds
            fold_id = 1
            for tr_idx, va_idx in kf.split(Xtr_all):
                if self.cfg.verbose:
                    print(f"  - fold {fold_id}/{self.cfg.n_splits} (val={len(va_idx)})")
                fold_id += 1

                # slice
                X_tr = Xtr_all[tr_idx]
                X_va = Xtr_all[va_idx]
                Y_tr = Y_arr[tr_idx]

                # coords slices for gnn
                if spec.requires_coords:
                    assert coords_train is not None and coords_test is not None
                    coords_tr = coords_train.iloc[tr_idx].reset_index(drop=True)
                    coords_va = coords_train.iloc[va_idx].reset_index(drop=True)
                    coords_te = coords_test.reset_index(drop=True)
                else:
                    coords_tr = coords_va = coords_te = None

                # build a fresh model per fold
                model = spec.model  # could be class instance OR factory-like
                # Important:
                # - if user passed an instance, we must clone it, otherwise folds will share weights.
                # simplest: require a `.get_params()` and re-init is messy for torch models.
                # pragmatic: allow passing a callable `model_ctor()` as spec.model.
                if callable(model) and not hasattr(model, "fit"):
                    # user passed a constructor function/class
                    m = model()
                else:
                    # user passed an instance -> try to rebuild by type + get_params if available
                    if hasattr(model, "get_params"):
                        params = model.get_params()
                        m = type(model)(getattr(model, "cfg", None))  # best-effort
                        # overwrite cfg fields if possible
                        # if wrapper stores cfg dataclass, copying is complicated; ignore and use current cfg
                        # This path is fallback only.
                        # Recommendation: pass model constructor instead of instance.
                    else:
                        raise ValueError(
                            f"{spec.name}: spec.model is an instance without get_params(). "
                            f"Please pass a constructor function, e.g. model=lambda: XGBoostBaseModel(cfg)."
                        )

                # fit & predict
                if spec.requires_coords:
                    # fit(X_train, coords_train, Y_train)
                    m.fit(X_tr, coords_tr, Y_tr)
                    pred_va = m.predict(X_va, coords_va)
                    pred_te = m.predict(Xte_all, coords_te)
                else:
                    # fit(X_train, Y_train) , supports multi-target in your wrappers
                    m.fit(X_tr, Y_tr)
                    pred_va = m.predict(X_va)
                    pred_te = m.predict(Xte_all)

                pred_va = np.asarray(pred_va)
                pred_te = np.asarray(pred_te)

                if pred_va.shape != (len(va_idx), n_prots):
                    raise ValueError(f"{spec.name}: val pred shape expected {(len(va_idx), n_prots)}, got {pred_va.shape}")
                if pred_te.shape != (n_test, n_prots):
                    raise ValueError(f"{spec.name}: test pred shape expected {(n_test, n_prots)}, got {pred_te.shape}")

                oof[va_idx] = _to_dtype(pred_va, self.cfg.dtype)
                test_fold_preds.append(_to_dtype(pred_te, self.cfg.dtype))

            test_mean = np.mean(np.stack(test_fold_preds, axis=0), axis=0).astype(self.cfg.dtype, copy=False)

            # to dataframe with prefix
            oof_df = _as_df(oof, index=train_index, columns=protein_names, dtype=self.cfg.dtype)
            te_df = _as_df(test_mean, index=test_index, columns=protein_names, dtype=self.cfg.dtype)

            oof_df = _prefix_columns(oof_df, spec.name)
            te_df = _prefix_columns(te_df, spec.name)

            # optional cache to disk (per base model)
            if cache_dir is not None:
                _save_if_needed(oof_df, os.path.join(cache_dir, f"{spec.name}_OOF_train.csv"))
                _save_if_needed(te_df, os.path.join(cache_dir, f"{spec.name}_test_preds.csv"))

            meta_train_parts.append(oof_df)
            meta_test_parts.append(te_df)

        meta_X_train = pd.concat(meta_train_parts, axis=1)
        meta_X_test = pd.concat(meta_test_parts, axis=1)
        return meta_X_train, meta_X_test
