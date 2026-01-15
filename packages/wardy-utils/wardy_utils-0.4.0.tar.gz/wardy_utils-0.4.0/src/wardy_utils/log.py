"""Set up logging using the Loguru library.

Requires the 'log' extra: pip install wardy-utils[log]
"""

from __future__ import annotations

import inspect
import logging
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Final

from pydantic_settings import BaseSettings, SettingsConfigDict

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Callable

try:
    from loguru import logger
except ImportError as e:  # pragma: no cover
    msg = "loguru is required for wardy_utils.log. Install with: pip install wardy-utils[log]"
    raise ImportError(msg) from e

try:
    import logfire
except ImportError:  # pragma: no cover
    logfire = None


# ----- Settings -----


class LogSettings(BaseSettings):
    """Environment-driven settings for logging."""

    logfire_token: str = ""
    logfire_service_name: str = ""
    logfire_env_prefix: str = ""

    model_config = SettingsConfigDict(env_prefix="WARDY_UTILS_LOG_", case_sensitive=False)


# ----- Constants -----

STANDARD: Final = "[{time:HH:mm:ss}] {level} - {message}"
DETAIL: Final = "{time} {file:>25}:{line:<4} {level:<8} {message}"

# ----- Public API -----

__all__ = [
    "DETAIL",
    "STANDARD",
    "LogSettings",
    "configure_logfire",
    "configure_logging",
    "logger",
]


def configure_logging(
    log_filename: str | Path,
    *,
    service_name: str | None = None,
    standard_format: str = STANDARD,
    detail_format: str = DETAIL,
    log_rotation: str = "1 hour",
    log_retention: str = "7 days",
) -> None:
    """Setup Loguru logging for the application.

    Args:
        log_filename: Base name for the log file (will have .log suffix added).
        service_name: Service name for Logfire cloud logging. Required if using Logfire.
        standard_format: Format for stderr output.
        detail_format: Format for file and Logfire output.
        log_rotation: When to rotate log files.
        log_retention: How long to keep old log files.

    Environment variables (prefix WARDY_UTILS_LOG_):
        LOGFIRE_TOKEN: Token for Logfire cloud logging.
    """
    settings = LogSettings()

    # Capture things like Hishel logging
    intercept_logging()

    # Replace the default StdErr handler.
    logger.remove()
    logger.add(sys.stderr, level="WARNING", format=standard_format)

    # Add a rotating file handler.
    log_filename = Path(log_filename).with_suffix(".log")
    logger.add(
        log_filename,
        level="DEBUG",
        format=detail_format,
        rotation=log_rotation,
        retention=log_retention,
    )

    # Set up Logfire if token is configured
    if settings.logfire_token:
        configure_logfire(settings.logfire_token, service_name, detail_format)


def configure_logfire(token: str, service_name: str | None, log_format: str) -> None:
    """Configure Logfire cloud logging with available instrumentations.

    Args:
        token: Logfire API token.
        service_name: Service name for Logfire. Required.
        log_format: Log format string for Logfire handler.

    Raises:
        ImportError: If logfire is not installed.
        ValueError: If service_name is not provided.
    """
    if logfire is None:
        msg = "logfire is required for cloud logging. Install with: pip install logfire"
        raise ImportError(msg)

    if not service_name:
        msg = "service_name is required for Logfire"
        raise ValueError(msg)

    logfire.configure(token=token, service_name=service_name)
    logger.add(logfire.loguru_handler()["sink"], level="TRACE", format=log_format)

    # Instrument available integrations
    _try_instrument("system_metrics", logfire.instrument_system_metrics)
    _try_instrument("psycopg", logfire.instrument_psycopg)
    _try_instrument("httpx", logfire.instrument_httpx)
    _try_instrument("sqlalchemy", logfire.instrument_sqlalchemy)
    _try_instrument("redis", logfire.instrument_redis)
    _try_instrument("asyncpg", logfire.instrument_asyncpg)


def _try_instrument(name: str, func: Callable[[], None]) -> None:
    """Try to instrument a library, logging the result."""
    try:
        func()
    except RuntimeError:
        logger.debug(f"Logfire: {name} not available")
    else:
        logger.debug(f"Logfire: instrumented {name}")


# ----- Interface to the standard logging module -----


class InterceptHandler(logging.Handler):
    """Send logs to Loguru."""

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a log record."""
        # Get corresponding Loguru level if it exists.
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:  # pragma: no cover
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def intercept_logging() -> None:
    """Intercept standard logging and send it to Loguru."""
    # Configure the root logger
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
