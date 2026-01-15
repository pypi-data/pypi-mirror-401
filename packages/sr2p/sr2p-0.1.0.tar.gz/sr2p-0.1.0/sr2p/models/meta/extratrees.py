# models/meta/extratrees.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Union

import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesRegressor


ArrayLike = Union[np.ndarray, pd.DataFrame, pd.Series]


@dataclass
class ExtraTreesMetaConfig:
    n_estimators: int = 300
    max_depth: Optional[int] = None
    min_samples_split: int = 2
    random_state: int = 0
    n_jobs: int = -1


class ExtraTreesMetaModel:
    """
    ExtraTrees meta learner for stacking.

    This model trains ONE regressor per protein (target column).

    fit:
        fit(meta_X_train, Y_train_df, protein_names)

    predict:
        predict(meta_X_test) -> DataFrame (n_samples, n_proteins)

    export_feature_importance:
        export_feature_importance(dir_path)  # per-protein feature importance csv
    """

    def __init__(self, cfg: Optional[ExtraTreesMetaConfig] = None):
        self.cfg = cfg or ExtraTreesMetaConfig()
        self.models: Dict[str, ExtraTreesRegressor] = {}
        self.feature_names: Optional[list[str]] = None

    def fit(
        self,
        X_meta: Union[pd.DataFrame, np.ndarray],
        Y_train_df: pd.DataFrame,
        protein_names: list[str],
    ) -> "ExtraTreesMetaModel":
        if isinstance(X_meta, pd.DataFrame):
            self.feature_names = list(X_meta.columns)
            X_arr = X_meta.values
        else:
            X_arr = np.asarray(X_meta)
            self.feature_names = None

        for protein in protein_names:
            y = Y_train_df[protein].values

            model = ExtraTreesRegressor(
                n_estimators=self.cfg.n_estimators,
                max_depth=self.cfg.max_depth,
                min_samples_split=self.cfg.min_samples_split,
                n_jobs=self.cfg.n_jobs,
                random_state=self.cfg.random_state,
            )
            model.fit(X_arr, y)
            self.models[protein] = model

        return self

    def predict(self, X_meta: Union[pd.DataFrame, np.ndarray]) -> pd.DataFrame:
        if not self.models:
            raise RuntimeError("ExtraTreesMetaModel.predict() called before fit().")

        if isinstance(X_meta, pd.DataFrame):
            X_arr = X_meta.values
            index = X_meta.index
        else:
            X_arr = np.asarray(X_meta)
            index = None

        preds = {}
        for protein, model in self.models.items():
            preds[protein] = model.predict(X_arr)

        return pd.DataFrame(preds, index=index)

    def export_feature_importance(
        self,
        X_meta: Union[pd.DataFrame, np.ndarray],
        dir_path: str,
        protein_names: list[str],
    ) -> None:
        """
        Export per-protein feature importance to CSV.

        Output file name:
            {dir_path}/{protein}_feature_importance.csv

        Note:
            No base importance aggregation is performed.
        """
        import os

        os.makedirs(dir_path, exist_ok=True)

        if isinstance(X_meta, pd.DataFrame):
            feature_names = list(X_meta.columns)
        else:
            if self.feature_names is None:
                raise ValueError(
                    "X_meta is ndarray and feature names are unknown. "
                    "Pass DataFrame to export feature importance."
                )
            feature_names = self.feature_names

        for protein in protein_names:
            if protein not in self.models:
                continue
            model = self.models[protein]

            fi = pd.DataFrame(
                {"feature": feature_names, "importance": model.feature_importances_}
            ).sort_values("importance", ascending=False)

            out_path = os.path.join(dir_path, f"{protein}_feature_importance.csv")
            fi.to_csv(out_path, index=False)

    def get_params(self) -> dict:
        return {
            "n_estimators": self.cfg.n_estimators,
            "max_depth": self.cfg.max_depth,
            "min_samples_split": self.cfg.min_samples_split,
            "random_state": self.cfg.random_state,
            "n_jobs": self.cfg.n_jobs,
        }
