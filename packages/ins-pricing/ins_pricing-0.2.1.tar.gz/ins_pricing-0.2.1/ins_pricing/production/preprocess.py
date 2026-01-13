from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import pandas as pd


def load_preprocess_artifacts(path: str | Path) -> Dict[str, Any]:
    artifact_path = Path(path)
    payload = json.loads(artifact_path.read_text(encoding="utf-8", errors="replace"))
    if not isinstance(payload, dict):
        raise ValueError(f"Invalid preprocess artifact: {artifact_path}")
    return payload


def prepare_raw_features(df: pd.DataFrame, artifacts: Dict[str, Any]) -> pd.DataFrame:
    factor_nmes = list(artifacts.get("factor_nmes") or [])
    cate_list = list(artifacts.get("cate_list") or [])
    num_features = set(artifacts.get("num_features") or [])
    cat_categories = artifacts.get("cat_categories") or {}

    work = df.copy()
    for col in factor_nmes:
        if col not in work.columns:
            work[col] = pd.NA

    for col in factor_nmes:
        if col in num_features:
            work[col] = pd.to_numeric(work[col], errors="coerce").fillna(0)
        else:
            series = work[col].astype("object").fillna("<NA>")
            cats = cat_categories.get(col)
            if isinstance(cats, list) and cats:
                series = pd.Categorical(series, categories=cats)
            work[col] = series

    if factor_nmes:
        work = work[factor_nmes]
    return work


def apply_preprocess_artifacts(df: pd.DataFrame, artifacts: Dict[str, Any]) -> pd.DataFrame:
    cate_list = list(artifacts.get("cate_list") or [])
    num_features = list(artifacts.get("num_features") or [])
    var_nmes = list(artifacts.get("var_nmes") or [])
    numeric_scalers = artifacts.get("numeric_scalers") or {}
    drop_first = bool(artifacts.get("drop_first", True))

    work = prepare_raw_features(df, artifacts)
    oht = pd.get_dummies(
        work,
        columns=cate_list,
        drop_first=drop_first,
        dtype="int8",
    )

    for col in num_features:
        if col not in oht.columns:
            continue
        stats = numeric_scalers.get(col) or {}
        mean = float(stats.get("mean", 0.0))
        scale = float(stats.get("scale", 1.0))
        if scale == 0.0:
            scale = 1.0
        oht[col] = (oht[col] - mean) / scale

    if var_nmes:
        oht = oht.reindex(columns=var_nmes, fill_value=0)
    return oht
