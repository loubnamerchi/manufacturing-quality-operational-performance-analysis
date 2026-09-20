

from pathlib import Path
from typing import Union, Dict

import pandas as pd

from src.utils.logger import get_logger

logger = get_logger(__name__)


def load_csv(file_path: Union[str, Path], **kwargs) -> pd.DataFrame:

    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    df = pd.read_csv(path, **kwargs)
    logger.info(f"Loaded CSV '{path.name}' with shape {df.shape}")
    return df


def load_excel(file_path: Union[str, Path], sheet_name=0, **kwargs) -> pd.DataFrame:

    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Excel file not found: {path}")

    df = pd.read_excel(path, sheet_name=sheet_name, **kwargs)
    logger.info(f"Loaded Excel '{path.name}' (sheet={sheet_name}) with shape {df.shape}")
    return df


def load_multiple_csv(file_paths: Dict[str, Union[str, Path]]) -> Dict[str, pd.DataFrame]:

    datasets = {}
    for name, path in file_paths.items():
        datasets[name] = load_csv(path)
    return datasets
