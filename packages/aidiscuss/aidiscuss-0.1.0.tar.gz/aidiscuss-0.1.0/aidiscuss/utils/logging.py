"""Structured logging system for AIDiscuss."""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional


def setup_logging(
    log_dir: Path,
    level: str = "INFO",
    console_level: str = "INFO",
    file_level: str = "DEBUG",
) -> logging.Logger:
    """
    Configure structured logging for AIDiscuss.

    Creates two handlers:
    - Console: INFO level by default, clean format for user-facing output
    - File: DEBUG level by default, detailed format with file/line numbers

    Log files are rotated at 10MB with 5 backup files kept.

    Args:
        log_dir: Directory to store log files
        level: Root logger level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        console_level: Console handler level
        file_level: File handler level

    Returns:
        Configured logger instance

    Example:
        >>> from aidiscuss.utils.logging import setup_logging
        >>> from pathlib import Path
        >>> logger = setup_logging(Path.home() / ".aidiscuss" / "logs")
        >>> logger.info("Application started")
    """
    # Create log directory if it doesn't exist
    log_dir.mkdir(parents=True, exist_ok=True)

    # Get or create root logger for aidiscuss
    logger = logging.getLogger("aidiscuss")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Avoid duplicate handlers if called multiple times
    if logger.handlers:
        logger.handlers.clear()

    # Console handler (user-facing, clean output)
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(getattr(logging, console_level.upper(), logging.INFO))
    console_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console.setFormatter(console_formatter)

    # File handler (detailed, for debugging)
    file_handler = RotatingFileHandler(
        log_dir / "aidiscuss.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(getattr(logging, file_level.upper(), logging.DEBUG))
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_formatter)

    # Add handlers
    logger.addHandler(console)
    logger.addHandler(file_handler)

    # Suppress overly verbose third-party loggers
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("chromadb").setLevel(logging.WARNING)
    logging.getLogger("sentence_transformers").setLevel(logging.WARNING)

    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance.

    Args:
        name: Logger name (uses 'aidiscuss' if None)

    Returns:
        Logger instance

    Example:
        >>> from aidiscuss.utils.logging import get_logger
        >>> logger = get_logger(__name__)
        >>> logger.info("Module loaded")
    """
    if name:
        return logging.getLogger(f"aidiscuss.{name}")
    return logging.getLogger("aidiscuss")
