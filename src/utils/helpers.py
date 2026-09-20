
from pathlib import Path
import pandas as pd


def ensure_dir(path) -> Path:

    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def save_dataframe(df: pd.DataFrame, path, index: bool = False) -> None:

    path = Path(path)
    ensure_dir(path.parent)
    df.to_csv(path, index=index)


def percentage(part: float, whole: float, decimals: int = 2) -> float:

    if whole == 0:
        return 0.0
    return round((part / whole) * 100, decimals)


def format_currency(value: float) -> str:

    return f"${value:,.2f}"
