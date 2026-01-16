import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional, Union


def _parse_level(level: Optional[Union[int, str]]) -> Optional[int]:
    if level is None:
        return None

    if isinstance(level, int):
        return level

    level_str = str(level).strip().upper()
    if not level_str:
        return None

    return logging._nameToLevel.get(level_str, logging.INFO)


def _truthy_env(name: str) -> Optional[bool]:
    value = os.getenv(name)
    if value is None:
        return None

    value = value.strip().lower()
    if value in {"1", "true", "yes", "y", "on"}:
        return True
    if value in {"0", "false", "no", "n", "off"}:
        return False

    return None


def configure_logging(
    *,
    log_file: Optional[str] = None,
    level: Optional[Union[int, str]] = None,
    propagate: Optional[bool] = None,
) -> logging.Logger:
    """Configure logging for the furs_fiscalization package.

    Intended usage:
    - In Odoo: rely on Odoo's logging config; just set log levels as needed.
    - If you want a separate file: call this once at startup OR set env var.

    Environment variables (optional):
    - FURS_FISCALIZATION_LOG_FILE
    - FURS_FISCALIZATION_LOG_LEVEL (e.g. DEBUG, INFO)
    - FURS_FISCALIZATION_LOG_MAX_BYTES (default 10485760)
    - FURS_FISCALIZATION_LOG_BACKUP_COUNT (default 5)
    - FURS_FISCALIZATION_LOG_PROPAGATE (0/1)
    """

    logger = logging.getLogger("furs_fiscalization")

    env_log_file = os.getenv("FURS_FISCALIZATION_LOG_FILE")
    env_level = os.getenv("FURS_FISCALIZATION_LOG_LEVEL")

    effective_level = _parse_level(level if level is not None else env_level)
    if effective_level is not None:
        logger.setLevel(effective_level)

    effective_propagate = propagate
    if effective_propagate is None:
        effective_propagate = _truthy_env("FURS_FISCALIZATION_LOG_PROPAGATE")
    if effective_propagate is not None:
        logger.propagate = effective_propagate

    effective_log_file = log_file if log_file is not None else env_log_file
    if not effective_log_file:
        return logger

    log_path = Path(effective_log_file).expanduser()
    log_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        max_bytes = int(os.getenv("FURS_FISCALIZATION_LOG_MAX_BYTES", "10485760"))
    except ValueError:
        max_bytes = 10485760

    try:
        backup_count = int(os.getenv("FURS_FISCALIZATION_LOG_BACKUP_COUNT", "5"))
    except ValueError:
        backup_count = 5

    # Avoid duplicate handlers if configure_logging is called multiple times.
    for handler in logger.handlers:
        if isinstance(handler, RotatingFileHandler):
            try:
                if Path(handler.baseFilename) == log_path:
                    return logger
            except Exception:
                pass

    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )

    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(formatter)

    if effective_level is not None:
        file_handler.setLevel(effective_level)

    logger.addHandler(file_handler)
    return logger
