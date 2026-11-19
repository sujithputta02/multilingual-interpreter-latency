"""Logging utilities for Beyond the Average."""
import logging
import os
import sys
import yaml
from pathlib import Path


def setup_logger(name: str = "beyond_the_average", config_path: str = "config/settings.yaml") -> logging.Logger:
    """Configures and returns a structured logger based on settings.yaml."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    log_level = logging.INFO
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_file = "data/metadata/app.log"

    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                cfg = yaml.safe_load(f)
                if cfg and "logging" in cfg:
                    log_cfg = cfg["logging"]
                    log_level = getattr(logging, log_cfg.get("level", "INFO").upper(), logging.INFO)
                    log_format = log_cfg.get("format", log_format)
                    log_file = log_cfg.get("file", log_file)
        except Exception:
            pass

    logger.setLevel(log_level)
    formatter = logging.Formatter(log_format)

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(log_level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File handler
    try:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setLevel(log_level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    except Exception:
        pass

    return logger
