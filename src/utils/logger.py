

import logging
from pathlib import Path

from src.utils.config import load_config, resolve_path


def get_logger(name: str) -> logging.Logger:

    config = load_config()
    log_cfg = config.get("logging", {})

    level_name = log_cfg.get("level", "INFO")
    log_file_rel = log_cfg.get("log_file", "logs/pipeline.log")
    use_console = log_cfg.get("console", True)

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level_name, logging.INFO))

    # Prevent duplicate handlers when get_logger() is called multiple times
    # for the same module name (common in Jupyter notebooks).
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # File handler: persists all log messages to logs/pipeline.log
    log_file_abs: Path = resolve_path(log_file_rel)
    log_file_abs.parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_file_abs, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console handler: prints log messages to the terminal/notebook output
    if use_console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
