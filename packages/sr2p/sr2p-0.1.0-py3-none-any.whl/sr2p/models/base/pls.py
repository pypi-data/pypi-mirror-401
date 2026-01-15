# models/base/pls.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence, Union, Dict

import numpy as np
import pandas as pd
from sklearn.cross_decomposition import PLSRegression
from joblib import Parallel, delayed


ArrayLike = Union[np.ndarray, pd.DataFrame]


@dataclass
class PLSConfig:
    n_components: int = 5
    n_jobs: int = 1          # protein-level parallelism; set >1 if you want joblib parallel
    dtype: str = "float32"   # reduce memory


class PLSRegressor:
    """
    PLS base model for SR2P.

    Design:
      - One PLSRegression per protein (consistent with your previous implementation).
      - fit() takes X and Y (DataFrame recommended).
      - predict() returns DataFrame with protein columns.

    Notes:
      - OOF logic is NOT here (handled by stacking/level1.py).
      - No saving, no correlation here (handled by evaluation utilities if needed).
    """

    def __init__(self, cfg: Optional[PLSConfig] = None):
        self.cfg = cfg or PLSConfig()
        self.models: Dict[str, PLSRegression] = {}
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
    ) -> "PLSRegressor":
        X_arr = self._to_numpy(X_train).astype(self.cfg.dtype, copy=False)

        if isinstance(X_train, pd.DataFrame):
            self.feature_names_ = list(X_train.columns)
        else:
            self.feature_names_ = None

        if isinstance(Y_train, pd.DataFrame):
            Y_df = Y_train
        else:
            # if ndarray, require protein_names
            if protein_names is None:
                raise ValueError("protein_names must be provided when Y_train is ndarray.")
            Y_df = pd.DataFrame(Y_train, columns=list(protein_names))

        if protein_names is None:
            protein_names = list(Y_df.columns)
        else:
            protein_names = list(protein_names)

        self.protein_names_ = protein_names
        self.models = {}

        def _fit_one(p: str) -> tuple[str, PLSRegression]:
            y = Y_df[p].to_numpy()
            m = PLSRegression(n_components=self.cfg.n_components)
            m.fit(X_arr, y)
            return p, m

        if self.cfg.n_jobs and self.cfg.n_jobs > 1:
            fitted = Parallel(n_jobs=self.cfg.n_jobs)(
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
            raise RuntimeError("PLSRegressor.predict() called before fit().")

        X_arr = self._to_numpy(X_test).astype(self.cfg.dtype, copy=False)
        index = X_test.index if isinstance(X_test, pd.DataFrame) else None

        preds = {}
        for p, m in self.models.items():
            preds[p] = m.predict(X_arr).reshape(-1)

        return pd.DataFrame(preds, index=index)
