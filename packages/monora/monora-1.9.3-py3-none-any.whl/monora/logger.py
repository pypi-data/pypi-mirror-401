"""Structured logging for Monora SDK.

This module provides a configurable logging abstraction that replaces
ad-hoc print statements with proper log levels and formatting.

Usage:
    from monora.logger import logger

    logger.info("Initialized successfully")
    logger.warning("Config file not found")
    logger.error("Failed to connect")
    logger.debug("Processing event: %s", event_id)

Configuration:
    Set MONORA_LOG_LEVEL environment variable to control verbosity:
    - DEBUG: All messages including detailed debugging
    - INFO: Informational messages and above
    - WARNING: Warnings and errors only (default)
    - ERROR: Errors only
    - SILENT: No output
"""
from __future__ import annotations

import logging
import os
import sys
from enum import Enum
from typing import Optional


class LogLevel(str, Enum):
    """Log level enumeration."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    SILENT = "SILENT"


# Module-level logger instance
_logger: Optional[logging.Logger] = None
_initialized: bool = False


def _get_level_from_env() -> int:
    """Get logging level from environment variable."""
    env_level = os.environ.get("MONORA_LOG_LEVEL", "WARNING").upper()

    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "WARN": logging.WARNING,
        "ERROR": logging.ERROR,
        "SILENT": logging.CRITICAL + 10,  # Higher than CRITICAL to suppress all
    }

    return level_map.get(env_level, logging.WARNING)


def get_logger() -> logging.Logger:
    """Get or create the Monora logger instance.

    Returns:
        The configured Monora logger.
    """
    global _logger, _initialized

    if _logger is None:
        _logger = logging.getLogger("monora")
        _logger.propagate = False  # Don't propagate to root logger

    if not _initialized:
        _logger.setLevel(_get_level_from_env())

        # Add stderr handler if none exists
        if not _logger.handlers:
            handler = logging.StreamHandler(sys.stderr)
            handler.setFormatter(logging.Formatter(
                "%(asctime)s [MONORA] %(levelname)s: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            ))
            _logger.addHandler(handler)

        _initialized = True

    return _logger


def set_level(level: str) -> None:
    """Set the log level programmatically.

    Args:
        level: Log level string (DEBUG, INFO, WARNING, ERROR, SILENT)
    """
    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "WARN": logging.WARNING,
        "ERROR": logging.ERROR,
        "SILENT": logging.CRITICAL + 10,
    }

    log_level = level_map.get(level.upper(), logging.WARNING)
    get_logger().setLevel(log_level)


def get_level() -> str:
    """Get the current log level name.

    Returns:
        Current log level as string.
    """
    level = get_logger().level
    level_names = {
        logging.DEBUG: "DEBUG",
        logging.INFO: "INFO",
        logging.WARNING: "WARNING",
        logging.ERROR: "ERROR",
        logging.CRITICAL: "CRITICAL",
    }
    return level_names.get(
        level,
        "SILENT" if level > logging.CRITICAL else "WARNING",
    )


def debug(msg: str, *args, **kwargs) -> None:
    """Log a debug message.

    Args:
        msg: Message format string
        *args: Format arguments
        **kwargs: Additional logging kwargs
    """
    get_logger().debug(msg, *args, **kwargs)


def info(msg: str, *args, **kwargs) -> None:
    """Log an info message.

    Args:
        msg: Message format string
        *args: Format arguments
        **kwargs: Additional logging kwargs
    """
    get_logger().info(msg, *args, **kwargs)


def warning(msg: str, *args, **kwargs) -> None:
    """Log a warning message.

    Args:
        msg: Message format string
        *args: Format arguments
        **kwargs: Additional logging kwargs
    """
    get_logger().warning(msg, *args, **kwargs)


def error(msg: str, *args, **kwargs) -> None:
    """Log an error message.

    Args:
        msg: Message format string
        *args: Format arguments
        **kwargs: Additional logging kwargs
    """
    get_logger().error(msg, *args, **kwargs)


# Logger interface for convenient import
class _LoggerInterface:
    """Logger interface providing method access."""

    debug = staticmethod(debug)
    info = staticmethod(info)
    warning = staticmethod(warning)
    error = staticmethod(error)
    set_level = staticmethod(set_level)
    get_level = staticmethod(get_level)

    @staticmethod
    def get_logger() -> logging.Logger:
        """Get the underlying Python logger."""
        return get_logger()


logger = _LoggerInterface()

__all__ = [
    "logger",
    "get_logger",
    "set_level",
    "get_level",
    "debug",
    "info",
    "warning",
    "error",
    "LogLevel",
]
