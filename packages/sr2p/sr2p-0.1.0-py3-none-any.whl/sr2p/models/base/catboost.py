# models/base/catboost.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Sequence, Union

import numpy as np
import pandas as pd
from joblib import Parallel, delayed

try:
    from catboost import CatBoostRegressor
except Exception:
    CatBoostRegressor = None  # type: ignore


ArrayLike = Union[np.ndarray, pd.DataFrame]


@dataclass
class CatBoostConfig:
    # core
    loss_function: str = "RMSE"
    random_seed: int = 42
    verbose: int = 0

    iterations: int = 300
    depth: int = 6
    learning_rate: float = 0.05
    l2_leaf_reg: float = 3.0

    bootstrap_type: str = "Bernoulli"
    subsample: float = 0.7

    task_type: str = "CPU"      # "CPU" or "GPU"

    # IMPORTANT:
    # - thread_count is per-catboost-model threads. Keep 1 if you use joblib outside.
    thread_count: int = 1

    # protein-level parallelism
    parallel_proteins: int = 1  # joblib n_jobs for proteins

    # memory
    dtype: str = "float32"


class CatBoostRegressorWrapper:
    """
    CatBoost base model for SR2P.

    Trains ONE CatBoostRegressor per protein (target column).

    fit:
        fit(X_train, Y_train_df, protein_names=None)

    predict:
        predict(X_test) -> DataFrame (n_samples, n_proteins)

    Notes:
      - OOF is handled by stacking/level1.py.
      - No saving and no metric computation here.
    """

    def __init__(self, cfg: Optional[CatBoostConfig] = None):
        if CatBoostRegressor is None:
            raise ImportError("catboost is not available. Please install catboost.")
        self.cfg = cfg or CatBoostConfig()
        self.models: Dict[str, CatBoostRegressor] = {}
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
    ) -> "CatBoostRegressorWrapper":
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

        def _fit_one(p: str) -> tuple[str, CatBoostRegressor]:
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
            raise RuntimeError("CatBoostRegressorWrapper.predict() called before fit().")

        X_arr = self._to_numpy(X_test).astype(self.cfg.dtype, copy=False)
        index = X_test.index if isinstance(X_test, pd.DataFrame) else None

        preds = {}
        for p, m in self.models.items():
            preds[p] = np.asarray(m.predict(X_arr)).reshape(-1)

        return pd.DataFrame(preds, index=index)

    def _build_model(self) -> "CatBoostRegressor":
        params = {
            "loss_function": self.cfg.loss_function,
            "random_seed": self.cfg.random_seed,
            "verbose": self.cfg.verbose,
            "iterations": self.cfg.iterations,
            "depth": self.cfg.depth,
            "learning_rate": self.cfg.learning_rate,
            "l2_leaf_reg": self.cfg.l2_leaf_reg,
            "bootstrap_type": self.cfg.bootstrap_type,
            "subsample": self.cfg.subsample,
            "task_type": self.cfg.task_type,
            "thread_count": self.cfg.thread_count,
        }
        return CatBoostRegressor(**params)

    def get_params(self) -> dict:
        return {
            "loss_function": self.cfg.loss_function,
            "random_seed": self.cfg.random_seed,
            "verbose": self.cfg.verbose,
            "iterations": self.cfg.iterations,
            "depth": self.cfg.depth,
            "learning_rate": self.cfg.learning_rate,
            "l2_leaf_reg": self.cfg.l2_leaf_reg,
            "bootstrap_type": self.cfg.bootstrap_type,
            "subsample": self.cfg.subsample,
            "task_type": self.cfg.task_type,
            "thread_count": self.cfg.thread_count,
            "parallel_proteins": self.cfg.parallel_proteins,
            "dtype": self.cfg.dtype,
        }
