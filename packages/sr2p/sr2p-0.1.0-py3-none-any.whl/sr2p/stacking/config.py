# config.py
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


# -------------------------
# Global / runtime configs
# -------------------------
@dataclass
class RuntimeConfig:
    """
    Global runtime behavior.

    seed:
        random seed for numpy and torch (if used)
    n_jobs:
        used by classical ML models when supported (xgboost/lightgbm/extratrees)
        For CatBoost, use thread_count in CatBoostConfig.
    device:
        for torch models: "cpu", "cuda", or None (auto)
    verbose:
        0 = silent, 1 = basic logs
    """
    seed: int = 42
    n_jobs: int = 1
    device: Optional[str] = None
    verbose: int = 1


# -------------------------
# Data configs (optional)
# -------------------------
@dataclass
class DataConfig:
    """
    Optional data processing config.

    sample_col / x_col / y_col:
        required column names in coords_df.
    """
    sample_col: str = "sample_id"
    x_col: str = "x"
    y_col: str = "y"


# -------------------------
# Stacking configs
# -------------------------
@dataclass
class CVConfig:
    """
    Cross validation config for OOF.
    """
    n_splits: int = 5
    shuffle: bool = True
    random_state: int = 42


@dataclass
class StackingConfig:
    """
    High-level stacking config.

    save_intermediate:
        if True, users may optionally dump OOF and test meta features to disk
        (the pipeline itself does NOT force saving).
    """
    cv: CVConfig = field(default_factory=CVConfig)
    save_intermediate: bool = False


# -------------------------
# Model selection configs
# -------------------------
@dataclass
class BaseModelFlags:
    """
    Turn on/off base learners quickly.
    """
    use_pls: bool = True
    use_pls_spatial: bool = True

    use_xgboost: bool = True
    use_xgboost_spatial: bool = True

    use_lightgbm: bool = True
    use_lightgbm_spatial: bool = True

    use_catboost: bool = True
    use_catboost_spatial: bool = True

    use_gs: bool = True
    use_gat: bool = True
    use_dgat: bool = True


@dataclass
class MetaModelFlags:
    """
    Choose meta learner(s).
    """
    use_extratrees: bool = True
