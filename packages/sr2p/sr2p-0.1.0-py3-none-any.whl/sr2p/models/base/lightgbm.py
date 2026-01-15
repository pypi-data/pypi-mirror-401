# models/base/lightgbm.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Sequence, Union

import numpy as np
import pandas as pd
from joblib import Parallel, delayed

try:
    from lightgbm import LGBMRegressor
except Exception:
    LGBMRegressor = None  # type: ignore


ArrayLike = Union[np.ndarray, pd.DataFrame]


@dataclass
class LightGBMConfig:
    # core
    n_estimators: int = 300
    learning_rate: float = 0.05

    max_depth: int = -1
    num_leaves: int = 31

    # sampling
    subsample: float = 0.8
    colsample_bytree: float = 0.8

    # system
    random_state: int = 42

    # IMPORTANT:
    # - n_jobs here is per-lightgbm-model threads. Keep it 1 if you use joblib outside.
    n_jobs: int = 1
    verbose: int = -1

    # protein-level parallelism
    parallel_proteins: int = 1  # joblib n_jobs for proteins

    # memory
    dtype: str = "float32"


class LightGBMRegressorWrapper:
    """
    LightGBM base model for SR2P.

    Trains ONE LGBMRegressor per protein (target column).

    fit:
        fit(X_train, Y_train_df, protein_names=None)

    predict:
        predict(X_test) -> DataFrame (n_samples, n_proteins)

    Notes:
      - OOF is handled by stacking/level1.py.
      - No saving and no metric computation here.
    """

    def __init__(self, cfg: Optional[LightGBMConfig] = None):
        if LGBMRegressor is None:
            raise ImportError("lightgbm is not available. Please install lightgbm.")
        self.cfg = cfg or LightGBMConfig()
        self.models: Dict[str, LGBMRegressor] = {}
        self.protein_names_: Optional[list[str]] = None
        self.feature_names_: Optional[list[str]] = None

    @staticmethod
    def _to_numpy(X: ArrayLike) -> np.ndarray:
        if isinstance(X, pd.DataFrame):
            return X.to_numpy()
        return np.asarray(X)

    def fit(
        self,
        X_train: ArrayLike,
        Y_train: Union[pd.DataFrame, np.ndarray],
        protein_names: Optional[Sequence[str]] = None,
    ) -> "LightGBMRegressorWrapper":
        X_arr = self._to_numpy(X_train).astype(self.cfg.dtype, copy=False)

        if isinstance(X_train, pd.DataFrame):
            self.feature_names_ = list(X_train.columns)
        else:
            self.feature_names_ = None

        if isinstance(Y_train, pd.DataFrame):
            Y_df = Y_train
        else:
            if protein_names is None:
                raise ValueError("protein_names must be provided when Y_train is ndarray.")
            Y_df = pd.DataFrame(Y_train, columns=list(protein_names))

        if protein_names is None:
            protein_names = list(Y_df.columns)
        else:
            protein_names = list(protein_names)

        self.protein_names_ = protein_names
        self.models = {}

        def _fit_one(p: str) -> tuple[str, LGBMRegressor]:
            y = Y_df[p].to_numpy()
            m = self._build_model()
            m.fit(X_arr, y)
            return p, m

        if self.cfg.parallel_proteins and self.cfg.parallel_proteins > 1:
            fitted = Parallel(n_jobs=self.cfg.parallel_proteins)(
                delayed(_fit_one)(p) for p in protein_names
            )
            self.models = dict(fitted)
        else:
            for p in protein_names:
                name, m = _fit_one(p)
                self.models[name] = m

        return self

    def predict(self, X_test: ArrayLike) -> pd.DataFrame:
        if not self.models:
            raise RuntimeError("LightGBMRegressorWrapper.predict() called before fit().")

        X_arr = self._to_numpy(X_test).astype(self.cfg.dtype, copy=False)
        index = X_test.index if isinstance(X_test, pd.DataFrame) else None

        preds = {}
        for p, m in self.models.items():
            preds[p] = m.predict(X_arr).reshape(-1)

        return pd.DataFrame(preds, index=index)

    def _build_model(self) -> "LGBMRegressor":
        params = {
            "n_estimators": self.cfg.n_estimators,
            "learning_rate": self.cfg.learning_rate,
            "max_depth": self.cfg.max_depth,
            "num_leaves": self.cfg.num_leaves,
            "subsample": self.cfg.subsample,
            "colsample_bytree": self.cfg.colsample_bytree,
            "random_state": self.cfg.random_state,
            "n_jobs": self.cfg.n_jobs,   # per-model threads
            "verbose": self.cfg.verbose,
        }
        return LGBMRegressor(**params)

    def get_params(self) -> dict:
        return {
            "n_estimators": self.cfg.n_estimators,
            "learning_rate": self.cfg.learning_rate,
            "max_depth": self.cfg.max_depth,
            "num_leaves": self.cfg.num_leaves,
            "subsample": self.cfg.subsample,
            "colsample_bytree": self.cfg.colsample_bytree,
            "random_state": self.cfg.random_state,
            "n_jobs": self.cfg.n_jobs,
            "verbose": self.cfg.verbose,
            "parallel_proteins": self.cfg.parallel_proteins,
            "dtype": self.cfg.dtype,
        }
