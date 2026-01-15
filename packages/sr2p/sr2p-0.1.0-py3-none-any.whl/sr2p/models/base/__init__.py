# sr2p/models/base/__init__.py
from __future__ import annotations

from .pls import PLSRegression, PLSConfig
from .xgboost import XGBoostRegressorWrapper, XGBoostConfig
from .lightgbm import LightGBMRegressorWrapper, LightGBMConfig
from .catboost import CatBoostRegressorWrapper, CatBoostConfig

from .gs import GraphSAGEBaseModel, GraphSAGEConfig
from .gat import GATBaseModel, GATConfig
from .dgat import DGATBaseModel, DGATConfig

from .gnn_utils import (
    build_samplewise_graph,
    build_samplewise_dual_graphs,
)

__all__ = [
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
    "build_samplewise_graph",
    "build_samplewise_dual_graphs",
]
