import logging
from datetime import datetime
from typing import Any


class GelfMessage:
    """GELF message builder for Graylog."""

    @staticmethod
    def create(
        short_message: str,
        full_message: str | None = None,
        level: int = 6,
        host: str = "unknown",
        timestamp: float | None = None,
        **additional_fields
    ) -> dict[str, Any]:
        """Create a properly formatted GELF message.

        Args:
            short_message: Short log description (required)
            full_message: Full log description (optional)
            level: Syslog level (7=debug, 6=info, 4=warning, 3=error, 2=critical)
            host: Host/application name
            timestamp: Unix timestamp (if None - current time)
            **additional_fields: Additional fields (will be prefixed with _)

        Returns:
            dict: GELF message ready to send
        """
        message = {
            "version": "1.1",
            "host": host,
            "short_message": short_message,
            "level": level,
            "timestamp": timestamp or datetime.now().timestamp(),
        }

        if full_message:
            message["full_message"] = full_message

        for key, value in additional_fields.items():
            if not key.startswith("_"):
                key = f"_{key}"
            message[key] = value

        return message

    @staticmethod
    def convert_log_level(python_level: int) -> int:
        """Convert Python logging level to Syslog level for GELF.

        Args:
            python_level: Python logging level (logging.DEBUG, logging.INFO, etc.)

        Returns:
            int: Syslog level (7=debug, 6=info, 4=warning, 3=error, 2=critical)
        """
        level_map = {
            logging.DEBUG: 7,
            logging.INFO: 6,
            logging.WARNING: 4,
            logging.ERROR: 3,
            logging.CRITICAL: 2,
        }
        return level_map.get(python_level, 6)


# Для обратной совместимости
def create_gelf_message(*args, **kwargs) -> dict[str, Any]:
    """Deprecated: Use GelfMessage.create() instead."""
    return GelfMessage.create(*args, **kwargs)


def convert_python_log_level(python_level: int) -> int:
    """Deprecated: Use GelfMessage.convert_log_level() instead."""
    return GelfMessage.convert_log_level(python_level)
