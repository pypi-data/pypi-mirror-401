# data/normalization.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple, List, Dict

import numpy as np
import pandas as pd
import scipy.sparse as sp

import anndata as ad
import scanpy as sc


@dataclass
class RNAProteinPrepConfig:
    # RNA
    rna_target_sum: float = 1e4
    rna_hvg_top_genes_train: int = 10000   # used in normalize_rna_and_protein
    rna_hvg_top_genes_test: int = 5000     # used in normalize_rna
    rna_scale_max_value: float = 10.0

    # Protein
    protein_pseudocount: float = 1.0


# ----------------------------
# 1) Quality control split
# ----------------------------
def split_quality_control(
    adata,
    *,
    feature_type_col: str = "feature_types",
    rna_feature_name: str = "Gene Expression",
    protein_feature_name: str = "Antibody Capture",
    exclude_protein_pattern: str = "mouse|rat",
) -> Tuple[ad.AnnData, ad.AnnData]:
    """
    Split AnnData into RNA and Protein AnnData.

    Cases:
      1) If adata.var has `feature_type_col`, split by feature types.
      2) If not, treat ALL features as RNA (e.g. ST RNA-only),
         and return an empty protein AnnData with same obs.
    """
    # Case 2: no feature_types column -> RNA only
    if feature_type_col not in adata.var.columns:
        rna_adata = adata.copy()
        rna_adata.var_names_make_unique()

        protein_adata = ad.AnnData(
            X=np.zeros((adata.n_obs, 0), dtype=np.float32),
            obs=adata.obs.copy(),
            var=pd.DataFrame(index=pd.Index([], name="features")),
        )
        return rna_adata, protein_adata

    # Case 1: has feature_types
    rna_mask = adata.var[feature_type_col] == rna_feature_name
    ab_mask = adata.var[feature_type_col] == protein_feature_name
    valid_ab_mask = ab_mask & ~adata.var_names.str.contains(exclude_protein_pattern, case=False)

    rna_adata = adata[:, rna_mask].copy()
    protein_adata = adata[:, valid_ab_mask].copy()

    rna_adata.var_names_make_unique()
    protein_adata.var_names_make_unique()
    return rna_adata, protein_adata


# ----------------------------
# 2) Helper transforms
# ----------------------------
def _manual_scale(adata: ad.AnnData, *, max_value: float = 10.0) -> ad.AnnData:
    """
    Manual standardization (mean=0 std=1) and clip max value.
    Reproduces your current behavior.
    """
    X = adata.X.toarray() if sp.issparse(adata.X) else np.asarray(adata.X).copy()
    gene_means = np.mean(X, axis=0)
    gene_stds = np.std(X, axis=0)
    gene_stds[gene_stds == 0] = 1.0

    X_scaled = (X - gene_means) / gene_stds
    X_scaled = np.clip(X_scaled, a_min=None, a_max=max_value)
    adata.X = X_scaled.astype(np.float32)
    return adata


def _clr_transform(protein_adata: ad.AnnData, *, pseudocount: float = 1.0) -> ad.AnnData:
    """
    CLR transform for protein matrix.
    """
    if protein_adata.n_vars == 0:
        return protein_adata

    X = protein_adata.X.toarray() if hasattr(protein_adata.X, "toarray") else np.asarray(protein_adata.X)
    geometric_mean = np.exp(np.mean(np.log(X + pseudocount), axis=1, keepdims=True))
    clr_transformed = np.log((X + pseudocount) / geometric_mean)
    protein_adata.X = clr_transformed.astype(np.float32)
    return protein_adata


# ----------------------------
# 3) Normalization
# ----------------------------
def normalize_rna_and_protein(
    rna_adata: ad.AnnData,
    protein_adata: ad.AnnData,
    *,
    cfg: Optional[RNAProteinPrepConfig] = None,
) -> Tuple[ad.AnnData, ad.AnnData]:
    """
    Normalize RNA + Protein for paired multi-omics samples.
    - RNA: normalize_total -> log1p -> HVG selection -> subset to HVGs -> scale
    - Protein: CLR transform
    """
    cfg = cfg or RNAProteinPrepConfig()

    sc.pp.normalize_total(rna_adata, target_sum=cfg.rna_target_sum)
    sc.pp.log1p(rna_adata)

    sc.pp.highly_variable_genes(rna_adata, n_top_genes=cfg.rna_hvg_top_genes_train)
    rna_adata = rna_adata[:, rna_adata.var["highly_variable"]].copy()

    rna_adata = _manual_scale(rna_adata, max_value=cfg.rna_scale_max_value)

    protein_adata = _clr_transform(protein_adata, pseudocount=cfg.protein_pseudocount)
    return rna_adata, protein_adata


def normalize_rna(
    rna_adata: ad.AnnData,
    *,
    cfg: Optional[RNAProteinPrepConfig] = None,
) -> ad.AnnData:
    """
    Normalize RNA for RNA-only samples.
    - normalize_total -> log1p -> HVG flagging -> scale
    Note: does NOT subset to HVGs (matches your current code).
    """
    cfg = cfg or RNAProteinPrepConfig()
    rna_adata.var_names_make_unique()

    sc.pp.normalize_total(rna_adata, target_sum=cfg.rna_target_sum)
    sc.pp.log1p(rna_adata)

    sc.pp.highly_variable_genes(rna_adata, n_top_genes=cfg.rna_hvg_top_genes_test)
    rna_adata = _manual_scale(rna_adata, max_value=cfg.rna_scale_max_value)
    return rna_adata


# ----------------------------
# 4) Intersections
# ----------------------------
def intersect_genes(rna_list: List[ad.AnnData]) -> Tuple[List[ad.AnnData], List[str]]:
    """
    Intersect genes across multiple RNA AnnData objects and subset them.
    """
    if len(rna_list) == 0:
        raise ValueError("rna_list must not be empty.")

    shared_genes = rna_list[0].var_names
    for rna in rna_list[1:]:
        shared_genes = shared_genes.intersection(rna.var_names)

    rna_list = [rna[:, shared_genes].copy() for rna in rna_list]
    return rna_list, shared_genes.tolist()


def intersect_proteins(prot_list: List[ad.AnnData]) -> Tuple[List[ad.AnnData], List[str]]:
    """
    Intersect proteins across multiple Protein AnnData objects and subset them.
    """
    if len(prot_list) == 0:
        raise ValueError("prot_list must not be empty.")

    shared_prot = prot_list[0].var_names
    for prot in prot_list[1:]:
        shared_prot = shared_prot.intersection(prot.var_names)

    prot_list = [prot[:, shared_prot].copy() for prot in prot_list]
    return prot_list, shared_prot.tolist()


# ----------------------------
# 5) Coordinates extraction
# ----------------------------
def extract_coords_from_raw(
    adata_raw,
    adata_processed,
    *,
    row_col: str = "array_row",
    col_col: str = "array_col",
    sample_col: str = "sample_id",
    out_x: str = "x",
    out_y: str = "y",
) -> pd.DataFrame:
    """
    Create coords df aligned to adata_processed.obs_names.
    Requires raw obs to contain row_col/col_col (typical Visium: array_row/array_col).
    """
    coords = adata_raw.obs.rename(columns={row_col: out_x, col_col: out_y})[[out_x, out_y]].copy()
    coords[sample_col] = adata_raw.obs[sample_col].values
    coords = coords.loc[adata_processed.obs_names]
    coords.index = adata_processed.obs_names
    return coords


# ----------------------------
# 6) General pipeline
# ----------------------------
def prepare_train_test_from_samples(
    *,
    paired_train_samples: List[ad.AnnData],
    rna_only_test_samples: List[ad.AnnData],
    cfg: Optional[RNAProteinPrepConfig] = None,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, List[str]]:
    """
    General pipeline:
      - paired_train_samples: list of AnnData (must contain proteins)
      - rna_only_test_samples: list of AnnData (RNA-only ST is allowed)

    Steps:
      1) QC split
      2) Normalize train (RNA+protein) and test (RNA-only)
      3) Intersect genes across ALL train RNA + ALL test RNA
      4) Intersect proteins across train proteins
      5) Concat to get rna_train, prot_train, rna_test
      6) Extract coords and concat
      7) Output X_train_df, Y_train_df, X_test_df, train_coords_df, test_coords_df, protein_names
    """
    cfg = cfg or RNAProteinPrepConfig()

    if len(paired_train_samples) == 0:
        raise ValueError("paired_train_samples must contain at least 1 sample.")
    if len(rna_only_test_samples) == 0:
        raise ValueError("rna_only_test_samples must contain at least 1 sample.")

    # 1) QC split
    train_rna_list, train_prot_list = [], []
    for s in paired_train_samples:
        rna_s, prot_s = split_quality_control(s)
        train_rna_list.append(rna_s)
        train_prot_list.append(prot_s)

    test_rna_list = []
    for s in rna_only_test_samples:
        rna_s, _ = split_quality_control(s)
        test_rna_list.append(rna_s)

    # sanity check: train must have proteins
    for i, prot in enumerate(train_prot_list):
        if prot.n_vars == 0:
            sid = paired_train_samples[i].obs["sample_id"].unique()
            raise ValueError(
                f"Train sample at index {i} has no protein features (n_vars=0). "
                f"Train samples must be paired multi-omics. sample_id={sid}"
            )

    # 2) Normalize
    train_rna_norm, train_prot_norm = [], []
    for rna_s, prot_s in zip(train_rna_list, train_prot_list):
        rna_s, prot_s = normalize_rna_and_protein(rna_s, prot_s, cfg=cfg)
        train_rna_norm.append(rna_s)
        train_prot_norm.append(prot_s)

    test_rna_norm = []
    for rna_s in test_rna_list:
        test_rna_norm.append(normalize_rna(rna_s, cfg=cfg))

    # 3) Intersect genes across ALL RNA (train + test)
    all_rna = train_rna_norm + test_rna_norm
    all_rna, _shared_genes = intersect_genes(all_rna)

    n_train = len(train_rna_norm)
    train_rna_norm = all_rna[:n_train]
    test_rna_norm = all_rna[n_train:]

    # 4) Intersect proteins across train proteins
    train_prot_norm, _shared_prot = intersect_proteins(train_prot_norm)

    # 5) Concat
    rna_train = ad.concat(train_rna_norm, index_unique=None)
    prot_train = ad.concat(train_prot_norm, index_unique=None)
    rna_test = ad.concat(test_rna_norm, index_unique=None)

    # 6) Coords
    train_coords_list = []
    for raw_s, proc_rna in zip(paired_train_samples, train_rna_norm):
        train_coords_list.append(extract_coords_from_raw(raw_s, proc_rna))

    test_coords_list = []
    for raw_s, proc_rna in zip(rna_only_test_samples, test_rna_norm):
        test_coords_list.append(extract_coords_from_raw(raw_s, proc_rna))

    train_coords_df = pd.concat(train_coords_list, axis=0)
    test_coords_df = pd.concat(test_coords_list, axis=0)

    # 7) Matrices
    X_train_df = rna_train.to_df()
    Y_train_df = prot_train.to_df()
    X_test_df = rna_test.to_df()

    protein_names = Y_train_df.columns.tolist()

    return X_train_df, Y_train_df, X_test_df, train_coords_df, test_coords_df, protein_names


def prepare_train_test_from_sample_dict(
    *,
    samples: Dict[str, ad.AnnData],
    train_ids: List[str],
    test_ids: List[str],
    cfg: Optional[RNAProteinPrepConfig] = None,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, List[str]]:
    """
    Convenience wrapper:
      - samples: dict {sample_id: AnnData}
      - train_ids: sample_ids used as paired training samples (must contain proteins)
      - test_ids: sample_ids used as RNA-only test samples (ST RNA-only allowed)
    """
    if len(train_ids) == 0:
        raise ValueError("train_ids must contain at least 1 sample_id.")
    if len(test_ids) == 0:
        raise ValueError("test_ids must contain at least 1 sample_id.")

    missing_train = [sid for sid in train_ids if sid not in samples]
    missing_test = [sid for sid in test_ids if sid not in samples]
    if missing_train:
        raise KeyError(f"train_ids not found in samples: {missing_train}")
    if missing_test:
        raise KeyError(f"test_ids not found in samples: {missing_test}")

    paired_train_samples = [samples[sid] for sid in train_ids]
    rna_only_test_samples = [samples[sid] for sid in test_ids]

    return prepare_train_test_from_samples(
        paired_train_samples=paired_train_samples,
        rna_only_test_samples=rna_only_test_samples,
        cfg=cfg,
    )
