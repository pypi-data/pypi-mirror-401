# stacking/pipeline.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, List, Tuple, Any

import numpy as np
import pandas as pd

from .base_learner import BaseLearnerRunner, BaseModelSpec, BaseLearnerRunnerConfig
from .meta_learner import MetaLearnerRunner, MetaLearnerRunnerConfig, MetaModelSpec


@dataclass
class StackingPipelineConfig:
    """
    End-to-end stacking config.

    n_splits:
        CV folds for OOF generation in base learners.
    """
    n_splits: int = 5
    base_runner: BaseLearnerRunnerConfig = BaseLearnerRunnerConfig()
    meta_runner: MetaLearnerRunnerConfig = MetaLearnerRunnerConfig()
    verbose: int = 1


class StackingPipeline:
    """
    End-to-end stacking pipeline:

    1) Run base learners:
        - OOF predictions for train (meta_X_train)
        - averaged fold predictions for test (meta_X_test)
       (no mandatory saving; base learners can choose to cache models or not)

    2) Train meta learner on meta_X_train -> predict meta_X_test

    Inputs
    ------
    X_train, Y_train:
        RNA and protein matrices for paired training data
    X_test:
        RNA matrix for test data (can be RNA-only ST without proteins)

    coords_train, coords_test:
        DataFrames with columns: ['sample_id','x','y'] aligned with X_* rows.

    Notes
    -----
    - For classical ML base learners, set their per-model `requires_coords=False`.
    - For GNN base learners, set `requires_coords=True`.
    - For spatial feature base learners (fixed neighbor concat), you should pass
      X_train_spatial / X_test_spatial as alternative X for that learner
      via BaseModelSpec.x_kind = "spatial".
    """

    def __init__(
        self,
        *,
        cfg: Optional[StackingPipelineConfig] = None,
    ):
        self.cfg = cfg or StackingPipelineConfig()

        self.base_runner = BaseLearnerRunner(cfg=self.cfg.base_runner)
        self.meta_runner = MetaLearnerRunner(cfg=self.cfg.meta_runner)

        self.base_specs: List[BaseModelSpec] = []
        self.meta_spec: Optional[MetaModelSpec] = None

    # -------------------------
    # register learners
    # -------------------------
    def add_base_learner(self, spec: BaseModelSpec) -> None:
        self.base_specs.append(spec)

    def set_meta_learner(self, spec: MetaModelSpec) -> None:
        self.meta_spec = spec
        self.meta_runner.set_meta_model(spec)

    # -------------------------
    # main API
    # -------------------------
    def fit_predict(
        self,
        *,
        X_train: np.ndarray,
        Y_train: np.ndarray,
        X_test: np.ndarray,
        coords_train: pd.DataFrame,
        coords_test: pd.DataFrame,
        protein_names: List[str],
        # optional spatial-expanded features
        X_train_spatial: Optional[np.ndarray] = None,
        X_test_spatial: Optional[np.ndarray] = None,
        return_meta_features: bool = False,
    ) -> Dict[str, Any]:
        """
        Run full stacking and return predictions.

        Returns dict with keys:
          - "stacking_preds": DataFrame (n_test, n_prots) final output
          - "meta_X_train": DataFrame (optional)
          - "meta_X_test": DataFrame (optional)
          - "base_outputs": Dict[name -> {"oof": DataFrame, "test": DataFrame}]
        """
        if self.meta_spec is None:
            raise ValueError("Meta learner not set. Call set_meta_learner().")
        if len(self.base_specs) == 0:
            raise ValueError("No base learners added. Call add_base_learner().")

        if self.cfg.verbose:
            print("\n==============================")
            print("[StackingPipeline] Start")
            print("==============================")

        # 1) base learners -> meta features
        base_outputs: Dict[str, Dict[str, pd.DataFrame]] = {}

        meta_train_blocks = []
        meta_test_blocks = []

        for spec in self.base_specs:
            if self.cfg.verbose:
                print(f"\n[StackingPipeline] Base learner: {spec.name}")

            # choose which X to use
            if spec.x_kind == "raw":
                X_tr_use, X_te_use = X_train, X_test
            elif spec.x_kind == "spatial":
                if X_train_spatial is None or X_test_spatial is None:
                    raise ValueError(
                        f"Base learner '{spec.name}' requires spatial X, "
                        "but X_train_spatial / X_test_spatial is None."
                    )
                X_tr_use, X_te_use = X_train_spatial, X_test_spatial
            else:
                raise ValueError(f"Unknown x_kind={spec.x_kind} for base learner '{spec.name}'")

            # run OOF + test prediction
            oof_df, test_df = self.base_runner.run_oof_and_predict_test(
                spec=spec,
                X_train=X_tr_use,
                Y_train=Y_train,
                X_test=X_te_use,
                coords_train=coords_train,
                coords_test=coords_test,
                protein_names=protein_names,
                n_splits=self.cfg.n_splits,
            )

            # prefix columns with base learner name for meta features
            oof_df = oof_df.add_prefix(f"{spec.meta_prefix}_")
            test_df = test_df.add_prefix(f"{spec.meta_prefix}_")

            base_outputs[spec.name] = {"oof": oof_df, "test": test_df}
            meta_train_blocks.append(oof_df)
            meta_test_blocks.append(test_df)

        meta_X_train = pd.concat(meta_train_blocks, axis=1)
        meta_X_test = pd.concat(meta_test_blocks, axis=1)

        if self.cfg.verbose:
            print("\n[StackingPipeline] Meta feature shapes:")
            print(f"  meta_X_train: {meta_X_train.shape}")
            print(f"  meta_X_test : {meta_X_test.shape}")

        # 2) meta learner
        Y_train_df = pd.DataFrame(Y_train, columns=protein_names, index=meta_X_train.index)
        stacking_preds = self.meta_runner.fit_predict(
            meta_X_train=meta_X_train,
            meta_X_test=meta_X_test,
            Y_train_df=Y_train_df,
            protein_names=protein_names,
        )

        # enforce output format
        stacking_preds = pd.DataFrame(stacking_preds, index=meta_X_test.index, columns=protein_names)

        out: Dict[str, Any] = {
            "stacking_preds": stacking_preds,
            "base_outputs": base_outputs,
        }
        if return_meta_features:
            out["meta_X_train"] = meta_X_train
            out["meta_X_test"] = meta_X_test

        if self.cfg.verbose:
            print("\n==============================")
            print("[StackingPipeline] Done")
            print("==============================")

        return out
