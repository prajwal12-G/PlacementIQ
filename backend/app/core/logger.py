"""
Application logging configuration.

Named `logger.py` (not `logging.py`) to avoid shadowing Python's
standard-library `logging` module.

Import this module once during application startup to configure
application-wide logging.

Each application module should create its own logger:

    import logging

    logger = logging.getLogger(__name__)

This ensures log records correctly identify the module that emitted
them (e.g. `app.api.auth`, `app.services.auth_service`).
"""

import logging
import sys

# ---------------------------------------------------------------------------
# Logging Configuration
# ---------------------------------------------------------------------------

# Default application log level.
LOG_LEVEL = logging.INFO

# Shared log format used across the entire application.
LOG_FORMAT = (
    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
)


def setup_logging() -> None:
    """
    Configure application-wide logging.

    This function should be called exactly once during application
    startup (typically from `app.main`).

    Using `force=True` ensures repeated executions—such as Uvicorn's
    auto-reloader or test runners—replace existing handlers instead
    of creating duplicate log output.
    """
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        stream=sys.stdout,
        force=True,
    )


__all__ = [
    "setup_logging",
    "LOG_LEVEL",
    "LOG_FORMAT",
]