

from pathlib import Path
import yaml

# PROJECT_ROOT points to the top-level project folder (two levels above this
# file: src/utils/config.py -> src/utils -> src -> project root).
PROJECT_ROOT = Path(__file__).resolve().parents[2]


def load_config(config_path: str = "config/config.yaml") -> dict:

    full_path = PROJECT_ROOT / config_path
    with open(full_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config


def resolve_path(relative_path: str) -> Path:

    return PROJECT_ROOT / relative_path
