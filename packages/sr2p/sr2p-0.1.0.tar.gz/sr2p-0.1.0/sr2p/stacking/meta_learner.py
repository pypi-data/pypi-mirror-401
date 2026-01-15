# stacking/meta_learner.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List, Dict, Any, Tuple, Union

import numpy as np
import pandas as pd


# ----------------------------
# Types
# ----------------------------
NDArray = np.ndarray


# ----------------------------
# Config
# ----------------------------
@dataclass
class MetaLearnerRunnerConfig:
    """
    Meta learner training config.

    export_feature_importance_dir:
        if not None, export per-protein feature importance CSVs.
    """
    export_feature_importance_dir: Optional[str] = None
    verbose: int = 1


# ----------------------------
# Meta learner spec
# ----------------------------
@dataclass
class MetaModelSpec:
    """
    One meta learner entry.

    name:
        label used for prints.

    model:
        must provide:
          - fit(X_meta_train, Y_train_df, protein_names) -> self
          - predict(X_meta_test) -> DataFrame (n_test, n_prots)

        Optional:
          - export_feature_importance(X_meta_train, dir_path, protein_names)
    """
    name: str
    model: Any


# ----------------------------
# Runner
# ----------------------------
class MetaLearnerRunner:
    """
    Train meta learner(s) given meta features from base learners.

    Typical usage:
        runner = MetaLearnerRunner(cfg)
        runner.set_meta_model(MetaModelSpec("ExtraTrees", ExtraTreesMetaModel(...)))
        preds = runner.fit_predict(meta_X_train, meta_X_test, Y_train_df, protein_names)
    """

    def __init__(self, cfg: Optional[MetaLearnerRunnerConfig] = None):
        self.cfg = cfg or MetaLearnerRunnerConfig()
        self.spec: Optional[MetaModelSpec] = None
        self.fitted_model: Optional[Any] = None

    def set_meta_model(self, spec: MetaModelSpec) -> None:
        self.spec = spec

    def fit(
        self,
        *,
        meta_X_train: pd.DataFrame,
        Y_train_df: pd.DataFrame,
        protein_names: List[str],
    ) -> "MetaLearnerRunner":
        if self.spec is None:
            raise ValueError("No meta model set. Call set_meta_model() first.")

        if self.cfg.verbose:
            print(f"\n[MetaLearner] Fitting meta model: {self.spec.name}")

        model = self.spec.model
        model.fit(meta_X_train, Y_train_df, protein_names)
        self.fitted_model = model

        # optional importance export
        if self.cfg.export_feature_importance_dir is not None:
            if hasattr(model, "export_feature_importance"):
                if self.cfg.verbose:
                    print(f"[MetaLearner] Exporting feature importance -> {self.cfg.export_feature_importance_dir}")
                model.export_feature_importance(
                    meta_X_train,
                    self.cfg.export_feature_importance_dir,
                    protein_names,
                )
            else:
                if self.cfg.verbose:
                    print("[MetaLearner] export_feature_importance_dir set but model has no export_feature_importance(). Skipped.")

        return self

    def predict(self, *, meta_X_test: pd.DataFrame) -> pd.DataFrame:
        if self.fitted_model is None:
            raise RuntimeError("MetaLearnerRunner.predict() called before fit().")

        if self.cfg.verbose:
            print("[MetaLearner] Predicting with fitted meta model...")

        preds = self.fitted_model.predict(meta_X_test)
        if not isinstance(preds, pd.DataFrame):
            # enforce DataFrame output for consistency
            preds = pd.DataFrame(preds, index=meta_X_test.index)
        return preds

    def fit_predict(
        self,
        *,
        meta_X_train: pd.DataFrame,
        meta_X_test: pd.DataFrame,
        Y_train_df: pd.DataFrame,
        protein_names: List[str],
    ) -> pd.DataFrame:
        self.fit(meta_X_train=meta_X_train, Y_train_df=Y_train_df, protein_names=protein_names)
        return self.predict(meta_X_test=meta_X_test)
