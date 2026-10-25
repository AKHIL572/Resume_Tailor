"""
Rotating file logger setup for JobTailor.
"""

import logging
import logging.handlers
from pathlib import Path

from app.core.data_dirs import data_path


def setup_logging() -> None:
    """Configure root logger with a rotating file handler."""
    log_file = data_path("jobtailor.log")
    handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3,
        encoding="utf-8",
    )
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(handler)

    # Also log WARNING+ to stderr so errors surface during development
    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)
    console.setFormatter(formatter)
    root.addHandler(console)
