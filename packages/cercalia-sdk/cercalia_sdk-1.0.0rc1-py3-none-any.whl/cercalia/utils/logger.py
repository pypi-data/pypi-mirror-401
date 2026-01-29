"""
Logger utility for Cercalia SDK.

Provides a simple logging interface with debug mode support.
"""

import logging
import sys
from datetime import datetime
from typing import Any

# Create a custom logger for the SDK
_logger = logging.getLogger("cercalia")
_handler = logging.StreamHandler(sys.stdout)
_handler.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s", "%Y-%m-%d %H:%M:%S")
)
_logger.addHandler(_handler)
_logger.setLevel(logging.WARNING)  # Default to WARNING level


class LogService:
    """
    Logging service for Cercalia SDK.

    Provides methods for different log levels and debug mode control.
    """

    def __init__(self) -> None:
        self._debug_enabled: bool = False

    def set_debug(self, enabled: bool) -> None:
        """
        Enable or disable debug logging.

        Args:
            enabled: True to enable debug logs, False to disable
        """
        self._debug_enabled = enabled
        if enabled:
            _logger.setLevel(logging.DEBUG)
        else:
            _logger.setLevel(logging.WARNING)

    def _format_message(self, level: str, message: str) -> str:
        """
        Format log message with timestamp.

        Args:
            level: Log level string (e.g., 'DEBUG', 'INFO', 'ERROR').
            message: The message to format.

        Returns:
            Formatted message string with timestamp and level prefix.

        Example:
            >>> logger._format_message("INFO", "Request started")
            '2024-01-15 10:30:00 [INFO]: Request started'
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"{timestamp} [{level.upper()}]: {message}"

    def info(self, message: str, *meta: Any) -> None:
        """Log an info message."""
        _logger.info(message, *meta) if meta else _logger.info(message)

    def error(self, message: str, *meta: Any) -> None:
        """Log an error message."""
        if meta:
            _logger.error(f"{message} {meta}")
        else:
            _logger.error(message)

    def warn(self, message: str, *meta: Any) -> None:
        """Log a warning message."""
        _logger.warning(message, *meta) if meta else _logger.warning(message)

    def debug(self, message: str, *meta: Any) -> None:
        """Log a debug message (only if debug mode is enabled)."""
        if self._debug_enabled:
            if meta:
                _logger.debug(f"{message} {meta}")
            else:
                _logger.debug(message)


# Singleton logger instance
logger = LogService()
