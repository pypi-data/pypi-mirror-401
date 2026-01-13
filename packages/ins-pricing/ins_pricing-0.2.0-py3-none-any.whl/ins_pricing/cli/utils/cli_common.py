from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple, Union

import pandas as pd
from sklearn.model_selection import GroupShuffleSplit, train_test_split


PLOT_MODEL_LABELS: Dict[str, Tuple[str, str]] = {
    "glm": ("GLM", "pred_glm"),
    "xgb": ("Xgboost", "pred_xgb"),
    "resn": ("ResNet", "pred_resn"),
    "ft": ("FTTransformer", "pred_ft"),
    "gnn": ("GNN", "pred_gnn"),
}

PYTORCH_TRAINERS = {"resn", "ft", "gnn"}


def dedupe_preserve_order(items: Iterable[str]) -> List[str]:
    seen = set()
    unique: List[str] = []
    for item in items:
        if item not in seen:
            unique.append(item)
            seen.add(item)
    return unique


def build_model_names(prefixes: Sequence[str], suffixes: Sequence[str]) -> List[str]:
    names: List[str] = []
    for suffix in suffixes:
        names.extend(f"{prefix}_{suffix}" for prefix in prefixes)
    return names


def parse_model_pairs(raw_pairs: List) -> List[Tuple[str, str]]:
    pairs: List[Tuple[str, str]] = []
    for pair in raw_pairs:
        if isinstance(pair, (list, tuple)) and len(pair) == 2:
            pairs.append((str(pair[0]), str(pair[1])))
        elif isinstance(pair, str):
            parts = [p.strip() for p in pair.split(",") if p.strip()]
            if len(parts) == 2:
                pairs.append((parts[0], parts[1]))
    return pairs


def resolve_path(value: Optional[str], base_dir: Path) -> Optional[Path]:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        return None
    p = Path(value)
    if p.is_absolute():
        return p
    return (base_dir / p).resolve()


def resolve_dir_path(
    value: Optional[Union[str, Path]],
    base_dir: Path,
    *,
    create: bool = False,
) -> Optional[Path]:
    if value is None:
        return None
    if isinstance(value, Path):
        path = value if value.is_absolute() else (base_dir / value).resolve()
    else:
        value_str = str(value)
        if not value_str.strip():
            return None
        path = resolve_path(value_str, base_dir)
        if path is None:
            path = Path(value_str)
            if not path.is_absolute():
                path = (base_dir / path).resolve()
    if create:
        path.mkdir(parents=True, exist_ok=True)
    return path


def _infer_format_from_path(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".parquet", ".pq"}:
        return "parquet"
    if suffix in {".feather", ".ft"}:
        return "feather"
    return "csv"


def resolve_data_path(
    data_dir: Path,
    model_name: str,
    *,
    data_format: str = "csv",
    path_template: Optional[str] = None,
) -> Path:
    fmt = str(data_format or "csv").strip().lower()
    template = path_template or "{model_name}.{ext}"
    if fmt == "auto":
        candidates = [
            data_dir / template.format(model_name=model_name, ext="parquet"),
            data_dir / template.format(model_name=model_name, ext="feather"),
            data_dir / template.format(model_name=model_name, ext="csv"),
        ]
        for cand in candidates:
            if cand.exists():
                return cand.resolve()
        return candidates[-1].resolve()
    ext = "csv" if fmt in {"csv"} else fmt
    return (data_dir / template.format(model_name=model_name, ext=ext)).resolve()


def load_dataset(
    path: Path,
    *,
    data_format: str = "auto",
    dtype_map: Optional[Dict[str, Any]] = None,
    low_memory: bool = False,
) -> pd.DataFrame:
    fmt = str(data_format or "auto").strip().lower()
    if fmt == "auto":
        fmt = _infer_format_from_path(path)
    if fmt == "parquet":
        df = pd.read_parquet(path)
    elif fmt == "feather":
        df = pd.read_feather(path)
    elif fmt == "csv":
        df = pd.read_csv(path, low_memory=low_memory, dtype=dtype_map or None)
    else:
        raise ValueError(f"Unsupported data_format: {data_format}")
    if dtype_map:
        for col, dtype in dtype_map.items():
            if col in df.columns:
                df[col] = df[col].astype(dtype)
    return df


def coerce_dataset_types(raw: pd.DataFrame) -> pd.DataFrame:
    data = raw.copy()
    for col in data.columns:
        s = data[col]
        if pd.api.types.is_numeric_dtype(s):
            data[col] = pd.to_numeric(s, errors="coerce").fillna(0)
        else:
            data[col] = s.astype("object").fillna("<NA>")
    return data


def split_train_test(
    df: pd.DataFrame,
    *,
    holdout_ratio: float,
    strategy: str = "random",
    group_col: Optional[str] = None,
    time_col: Optional[str] = None,
    time_ascending: bool = True,
    rand_seed: Optional[int] = None,
    reset_index_mode: str = "none",
    ratio_label: str = "holdout_ratio",
    include_strategy_in_ratio_error: bool = False,
    validate_ratio: bool = True,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    strategy = str(strategy or "random").strip().lower()
    holdout_ratio = float(holdout_ratio)
    if include_strategy_in_ratio_error and strategy in {"time", "timeseries", "temporal", "group", "grouped"}:
        strategy_label = "time" if strategy in {"time", "timeseries", "temporal"} else "group"
        ratio_error = (
            f"{ratio_label} must be in (0, 1) for {strategy_label} split; got {holdout_ratio}."
        )
    else:
        ratio_error = f"{ratio_label} must be in (0, 1); got {holdout_ratio}."

    if strategy in {"time", "timeseries", "temporal"}:
        if not time_col:
            raise ValueError("split_time_col is required for time split_strategy.")
        if time_col not in df.columns:
            raise KeyError(f"split_time_col '{time_col}' not in dataset columns.")
        if validate_ratio and not (0.0 < holdout_ratio < 1.0):
            raise ValueError(ratio_error)
        ordered = df.sort_values(time_col, ascending=bool(time_ascending))
        cutoff = int(len(ordered) * (1.0 - holdout_ratio))
        if cutoff <= 0 or cutoff >= len(ordered):
            raise ValueError(
                f"{ratio_label}={holdout_ratio} leaves no data for train/test split.")
        train_df = ordered.iloc[:cutoff]
        test_df = ordered.iloc[cutoff:]
    elif strategy in {"group", "grouped"}:
        if not group_col:
            raise ValueError("split_group_col is required for group split_strategy.")
        if group_col not in df.columns:
            raise KeyError(f"split_group_col '{group_col}' not in dataset columns.")
        if validate_ratio and not (0.0 < holdout_ratio < 1.0):
            raise ValueError(ratio_error)
        splitter = GroupShuffleSplit(
            n_splits=1,
            test_size=holdout_ratio,
            random_state=rand_seed,
        )
        train_idx, test_idx = next(splitter.split(df, groups=df[group_col]))
        train_df = df.iloc[train_idx]
        test_df = df.iloc[test_idx]
    else:
        train_df, test_df = train_test_split(
            df, test_size=holdout_ratio, random_state=rand_seed
        )

    if reset_index_mode == "always" or (
        reset_index_mode == "time_group"
        and strategy in {"time", "timeseries", "temporal", "group", "grouped"}
    ):
        train_df = train_df.reset_index(drop=True)
        test_df = test_df.reset_index(drop=True)
    return train_df, test_df


def fingerprint_file(path: Path, *, max_bytes: int = 10_485_760) -> Dict[str, Any]:
    path = Path(path)
    stat = path.stat()
    h = hashlib.sha256()
    remaining = int(max_bytes)
    with path.open("rb") as fh:
        while remaining > 0:
            chunk = fh.read(min(1024 * 1024, remaining))
            if not chunk:
                break
            h.update(chunk)
            remaining -= len(chunk)
    return {
        "path": str(path),
        "size": int(stat.st_size),
        "mtime": int(stat.st_mtime),
        "sha256_prefix": h.hexdigest(),
        "max_bytes": int(max_bytes),
    }


def _load_cli_config():
    try:
        from . import cli_config as _cli_config  # type: ignore
    except Exception:  # pragma: no cover
        import cli_config as _cli_config  # type: ignore
    return _cli_config


def resolve_config_path(raw: str, script_dir: Path) -> Path:
    return _load_cli_config().resolve_config_path(raw, script_dir)


def load_config_json(path: Path, required_keys: Sequence[str]) -> Dict[str, Any]:
    return _load_cli_config().load_config_json(path, required_keys)


def set_env(env_overrides: Dict[str, Any]) -> None:
    _load_cli_config().set_env(env_overrides)


def normalize_config_paths(cfg: Dict[str, Any], config_path: Path) -> Dict[str, Any]:
    return _load_cli_config().normalize_config_paths(cfg, config_path)


def resolve_dtype_map(value: Any, base_dir: Path) -> Dict[str, Any]:
    return _load_cli_config().resolve_dtype_map(value, base_dir)


def resolve_data_config(
    cfg: Dict[str, Any],
    config_path: Path,
    *,
    create_data_dir: bool = False,
) -> Tuple[Path, str, Optional[str], Dict[str, Any]]:
    return _load_cli_config().resolve_data_config(
        cfg,
        config_path,
        create_data_dir=create_data_dir,
    )


def resolve_report_config(cfg: Dict[str, Any]) -> Dict[str, Any]:
    return _load_cli_config().resolve_report_config(cfg)


def resolve_split_config(cfg: Dict[str, Any]) -> Dict[str, Any]:
    return _load_cli_config().resolve_split_config(cfg)


def resolve_runtime_config(cfg: Dict[str, Any]) -> Dict[str, Any]:
    return _load_cli_config().resolve_runtime_config(cfg)


def resolve_output_dirs(
    cfg: Dict[str, Any],
    config_path: Path,
    *,
    output_override: Optional[str] = None,
) -> Dict[str, Optional[str]]:
    return _load_cli_config().resolve_output_dirs(
        cfg,
        config_path,
        output_override=output_override,
    )


def resolve_and_load_config(
    raw: str,
    script_dir: Path,
    required_keys: Sequence[str],
    *,
    apply_env: bool = True,
) -> Tuple[Path, Dict[str, Any]]:
    return _load_cli_config().resolve_and_load_config(
        raw,
        script_dir,
        required_keys,
        apply_env=apply_env,
    )
