# stacking/base_learner_utils.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Iterable, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from sklearn.model_selection import KFold


ArrayLike = Union[np.ndarray, pd.DataFrame]
IndexLike = Union[pd.Index, List[str]]


@dataclass
class OOFConfig:
    n_splits: int = 5
    shuffle: bool = True
    random_state: int = 42

    # joblib parallelism (for per protein models)
    n_jobs: int = -1

    # if True, also compute mean test predictions by training each fold model on fold train split
    # and averaging fold predictions on test set
    predict_test: bool = True


def _to_numpy(X: ArrayLike) -> np.ndarray:
    if isinstance(X, pd.DataFrame):
        return X.to_numpy()
    return np.asarray(X)


def _to_index(index: Optional[IndexLike], n: int) -> pd.Index:
    if index is None:
        return pd.RangeIndex(n)
    if isinstance(index, pd.Index):
        return index
    return pd.Index(index)


def _check_XY_shapes(X: np.ndarray, Y: np.ndarray) -> None:
    if X.ndim != 2:
        raise ValueError(f"X must be 2D, got shape {X.shape}.")
    if Y.ndim != 2:
        raise ValueError(f"Y must be 2D (n_samples, n_targets), got shape {Y.shape}.")
    if X.shape[0] != Y.shape[0]:
        raise ValueError(f"X and Y must have same n_samples. X={X.shape}, Y={Y.shape}.")


def _default_kfold(cfg: OOFConfig) -> KFold:
    return KFold(n_splits=cfg.n_splits, shuffle=cfg.shuffle, random_state=cfg.random_state)


def _fit_predict_single_target_oof(
    j: int,
    X_tr: np.ndarray,
    y_tr: np.ndarray,
    X_va: np.ndarray,
    model_factory: Callable[[], object],
) -> Tuple[int, np.ndarray]:
    """
    Train ONE model on one target and return predictions for validation rows.
    model_factory must return a sklearn-like regressor with .fit/.predict.
    """
    model = model_factory()
    model.fit(X_tr, y_tr)
    pred_va = model.predict(X_va)
    return j, np.asarray(pred_va)


def _fit_predict_single_target_test(
    j: int,
    X_tr: np.ndarray,
    y_tr: np.ndarray,
    X_test: np.ndarray,
    model_factory: Callable[[], object],
) -> Tuple[int, np.ndarray]:
    """
    Train ONE model on one target and return predictions for test rows.
    """
    model = model_factory()
    model.fit(X_tr, y_tr)
    pred_te = model.predict(X_test)
    return j, np.asarray(pred_te)


def run_oof_per_target(
    *,
    X_train: ArrayLike,
    Y_train: Union[np.ndarray, pd.DataFrame],
    target_names: List[str],
    model_factory: Callable[[], object],
    cfg: Optional[OOFConfig] = None,
    X_test: Optional[ArrayLike] = None,
    train_index: Optional[IndexLike] = None,
    test_index: Optional[IndexLike] = None,
    dtype: np.dtype = np.float32,
) -> Tuple[pd.DataFrame, Optional[pd.DataFrame]]:
    """
    Generic OOF runner for base learners that are trained one target at a time
    (e.g. XGBoost, LightGBM, CatBoost, PLS, most sklearn regressors).

    Returns
    -------
    oof_df:
        (n_train, n_targets) OOF predictions, aligned to train_index
    test_df:
        (n_test, n_targets) mean predictions across folds on X_test, or None if predict_test=False

    Notes
    -----
    - Parallelism is across targets, inside each fold.
    - If cfg.predict_test=True, test prediction is computed by training fold models on each fold train split
      and averaging fold predictions. This matches common stacking practice and your previous PLS strategy.
    - If you prefer "fit on full train then predict test" for some models, that should be a separate helper.
    """
    cfg = cfg or OOFConfig()

    Xtr = _to_numpy(X_train).astype(dtype, copy=False)

    if isinstance(Y_train, pd.DataFrame):
        Ytr = Y_train[target_names].to_numpy().astype(dtype, copy=False)
    else:
        Ytr = np.asarray(Y_train).astype(dtype, copy=False)

    _check_XY_shapes(Xtr, Ytr)

    n_train, n_targets = Ytr.shape
    tr_index = _to_index(train_index, n_train)

    if cfg.predict_test:
        if X_test is None:
            raise ValueError("cfg.predict_test=True but X_test is None.")
        Xte = _to_numpy(X_test).astype(dtype, copy=False)
        n_test = Xte.shape[0]
        te_index = _to_index(test_index, n_test)
        test_accum = np.zeros((n_test, n_targets), dtype=dtype)
    else:
        Xte = None
        te_index = None
        test_accum = None

    oof = np.zeros((n_train, n_targets), dtype=dtype)

    kf = _default_kfold(cfg)

    for fold, (tr_idx, va_idx) in enumerate(kf.split(Xtr), start=1):
        X_tr, X_va = Xtr[tr_idx], Xtr[va_idx]

        # ----- OOF predictions on validation split -----
        tasks_oof = (
            delayed(_fit_predict_single_target_oof)(
                j,
                X_tr,
                Ytr[tr_idx, j],
                X_va,
                model_factory,
            )
            for j in range(n_targets)
        )

        results_oof = Parallel(n_jobs=cfg.n_jobs)(tasks_oof)
        for j, pred_va in results_oof:
            oof[va_idx, j] = pred_va.astype(dtype, copy=False)

        # ----- Test predictions (fold mean) -----
        if cfg.predict_test and Xte is not None and test_accum is not None:
            tasks_te = (
                delayed(_fit_predict_single_target_test)(
                    j,
                    X_tr,
                    Ytr[tr_idx, j],
                    Xte,
                    model_factory,
                )
                for j in range(n_targets)
            )
            results_te = Parallel(n_jobs=cfg.n_jobs)(tasks_te)
            for j, pred_te in results_te:
                test_accum[:, j] += pred_te.astype(dtype, copy=False)

    oof_df = pd.DataFrame(oof, index=tr_index, columns=target_names)

    if cfg.predict_test and test_accum is not None and te_index is not None:
        test_mean = test_accum / float(cfg.n_splits)
        test_df = pd.DataFrame(test_mean, index=te_index, columns=target_names)
    else:
        test_df = None

    return oof_df, test_df


def fit_full_and_predict(
    *,
    X_train: ArrayLike,
    Y_train: Union[np.ndarray, pd.DataFrame],
    X_test: ArrayLike,
    target_names: List[str],
    model_factory: Callable[[], object],
    n_jobs: int = -1,
    train_index: Optional[IndexLike] = None,
    test_index: Optional[IndexLike] = None,
    dtype: np.dtype = np.float32,
) -> pd.DataFrame:
    """
    Train per-target models on FULL train data and predict on test.

    Useful when you do not need OOF, or for final retraining after selecting meta learner.
    """
    Xtr = _to_numpy(X_train).astype(dtype, copy=False)
    Xte = _to_numpy(X_test).astype(dtype, copy=False)

    if isinstance(Y_train, pd.DataFrame):
        Ytr = Y_train[target_names].to_numpy().astype(dtype, copy=False)
    else:
        Ytr = np.asarray(Y_train).astype(dtype, copy=False)

    _check_XY_shapes(Xtr, Ytr)

    n_test = Xte.shape[0]
    te_index = _to_index(test_index, n_test)

    def _fit_pred(j: int) -> Tuple[int, np.ndarray]:
        model = model_factory()
        model.fit(Xtr, Ytr[:, j])
        return j, np.asarray(model.predict(Xte))

    results = Parallel(n_jobs=n_jobs)(delayed(_fit_pred)(j) for j in range(len(target_names)))

    preds = np.zeros((n_test, len(target_names)), dtype=dtype)
    for j, p in results:
        preds[:, j] = p.astype(dtype, copy=False)

    return pd.DataFrame(preds, index=te_index, columns=target_names)


def add_prefix_columns(df: pd.DataFrame, prefix: str) -> pd.DataFrame:
    """
    Add prefix to each column name, e.g. protein columns -> model_protein columns.
    """
    return df.add_prefix(f"{prefix}_")


def concat_meta_features(
    parts: Iterable[Tuple[str, pd.DataFrame]],
    *,
    axis: int = 1,
) -> pd.DataFrame:
    """
    Concatenate multiple (name, dataframe) feature blocks into one meta feature matrix.

    parts: iterable of (prefix, df). Each df is expected to be (n_samples, n_proteins) with same index.
    Returns: DataFrame with prefixed columns.
    """
    blocks = []
    for name, df in parts:
        if not isinstance(df, pd.DataFrame):
            raise TypeError(f"Expected DataFrame for '{name}', got {type(df)}.")
        blocks.append(add_prefix_columns(df, name))
    return pd.concat(blocks, axis=axis)
