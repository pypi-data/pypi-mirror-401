import os
import logging
import pytest

from .reporting import build_artifact_path


def setup_logging(config: pytest.Config) -> None:
    """Configure root logger to write to reports/<ts>/framework_<ts>.log."""
    level = logging.DEBUG
    log_path = build_artifact_path(config, "framework", "log")

    logger = logging.getLogger()
    logger.setLevel(level)

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    # Avoid duplicate file handlers for same path
    need_add = True
    for h in logger.handlers:
        try:
            if isinstance(h, logging.FileHandler) and os.path.abspath(getattr(h, "baseFilename", "")) == os.path.abspath(log_path):
                need_add = False
                break
        except Exception:
            continue
    if need_add:
        fh = logging.FileHandler(log_path, encoding="utf-8")
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    setattr(config, "_log_path", log_path)


def get_logger(name: str) -> logging.Logger:
    """Return a named logger using the framework's logging configuration."""
    return logging.getLogger(name)