"""Unified logging that uses logfire when available, falls back to standard logging.

This module provides a simple interface for logging that:
- Uses logfire structured logging when available and configured
- Falls back to standard Python logging when logfire is not installed

Usage:
    from veris_ai.logger import log

    log.info("User logged in", user_id="123")
    log.debug("Processing request", request_id=request_id)
    log.warning("Rate limit approaching", current=90, limit=100)
    log.error("Failed to connect", error=str(e))
"""

import logging
import types

# Standard fallback logger
_std_logger = logging.getLogger("veris_ai")


class _LogfireCache:
    """Cache for logfire module availability."""

    def __init__(self) -> None:
        self._available: bool | None = None
        self._module: types.ModuleType | None = None

    def get_logfire(self) -> types.ModuleType | None:
        """Try to get the logfire module, cache the result."""
        if self._available is None:
            try:
                import logfire  # noqa: PLC0415

                self._available = True
                self._module = logfire
            except ImportError:
                self._available = False
                self._module = None
        return self._module if self._available else None


_cache = _LogfireCache()


def _format_message(message: str, **kwargs: object) -> str:
    """Format message with kwargs for standard logging."""
    if not kwargs:
        return message
    try:
        return message.format(**kwargs)
    except (KeyError, IndexError):
        # If formatting fails, append kwargs to message
        return f"{message} {kwargs}"


def info(message: str, **kwargs: object) -> None:
    """Log info message using logfire if available, else standard logger."""
    lf = _cache.get_logfire()
    if lf:
        lf.info(message, **kwargs)
    else:
        _std_logger.info(_format_message(message, **kwargs))


def debug(message: str, **kwargs: object) -> None:
    """Log debug message using logfire if available, else standard logger."""
    lf = _cache.get_logfire()
    if lf:
        lf.debug(message, **kwargs)
    else:
        _std_logger.debug(_format_message(message, **kwargs))


def warning(message: str, **kwargs: object) -> None:
    """Log warning message using logfire if available, else standard logger."""
    lf = _cache.get_logfire()
    if lf:
        lf.warn(message, **kwargs)
    else:
        _std_logger.warning(_format_message(message, **kwargs))


def error(message: str, exc_info: bool = False, **kwargs: object) -> None:
    """Log error message using logfire if available, else standard logger."""
    lf = _cache.get_logfire()
    if lf:
        lf.error(message, **kwargs)
    else:
        _std_logger.error(_format_message(message, **kwargs), exc_info=exc_info)


class VerisLogger:
    """Logger class that provides a unified interface for logfire/standard logging."""

    info = staticmethod(info)
    debug = staticmethod(debug)
    warning = staticmethod(warning)
    error = staticmethod(error)


# Singleton instance for convenient import
log = VerisLogger()
