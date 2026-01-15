# sr2p/__init__.py
from __future__ import annotations

__version__ = "0.1.0"

# ---- data ----
from .data.normalization import (
    split_quality_control,
    normalize_rna_and_protein,
    normalize_rna,
)

from .data.spatial_construction import (
    make_expand_fn_within_sample_fixed_neighbours,
)

# ---- models (base) ----
from .models.base.pls import PLSRegression, PLSConfig
from .models.base.xgboost import XGBoostRegressorWrapper, XGBoostConfig
from .models.base.lightgbm import LightGBMRegressorWrapper, LightGBMConfig
from .models.base.catboost import CatBoostRegressorWrapper, CatBoostConfig

from .models.base.gs import GraphSAGEBaseModel, GraphSAGEConfig
from .models.base.gat import GATBaseModel, GATConfig
from .models.base.dgat import DGATBaseModel, DGATConfig

# ---- models (meta) ----
from .models.meta.extratrees import ExtraTreesMetaModel, ExtraTreesMetaConfig

# ---- stacking ----
from .stacking.config import StackingConfig
from .stacking.base_learner import BaseLearnerRunner
from .stacking.meta_learner import MetaLearnerRunner
from .stacking.pipeline import StackingPipeline

__all__ = [
    "__version__",
    # data
    "split_quality_control",
    "normalize_rna_and_protein",
    "normalize_rna",
    "make_expand_fn_within_sample_fixed_neighbours",
    # base models
    "PLSRegression",
    "PLSConfig",
    "XGBoostRegressorWrapper",
    "XGBoostConfig",
    "LightGBMRegressorWrapper",
    "LightGBMConfig",
    "CatBoostRegressorWrapper",
    "CatBoostConfig",
    "GraphSAGEBaseModel",
    "GraphSAGEConfig",
    "GATBaseModel",
    "GATConfig",
    "DGATBaseModel",
    "DGATConfig",
    # meta models
    "ExtraTreesMetaModel",
    "ExtraTreesMetaConfig",
    # stacking
    "StackingConfig",
    "BaseLearnerRunner",
    "MetaLearnerRunner",
    "StackingPipeline",
]
