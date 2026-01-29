"""
Structured logging for SXD platform.

Usage:
    from sxd_core.logging import get_logger

    log = get_logger(__name__)
    log.info("processing video", video_id=video_id, customer_id=customer_id)
"""

import functools
import json
import logging
import os
import sys
from contextvars import ContextVar
from datetime import datetime, timezone
from typing import Any, Callable, TypeVar

T = TypeVar("T")

# global logger for sxd
_root_logger = None

# ContextVar to hold the current contextual logger
_current_logger: ContextVar["StructuredLogger"] = ContextVar("current_logger")


class StructuredFormatter(logging.Formatter):
    """JSON formatter for log records."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add trace context if available
        if hasattr(record, "trace_id"):
            log_entry["trace_id"] = record.trace_id
        if hasattr(record, "job_id"):
            log_entry["job_id"] = record.job_id

        # Add extra fields passed via log.info("msg", extra={...})
        # or via the StructuredLogger wrapper
        if hasattr(record, "structured_data"):
            log_entry.update(record.structured_data)

        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry)


class StructuredLogger:
    """Wrapper that allows keyword arguments for structured fields."""

    def __init__(self, logger: logging.Logger):
        self._logger = logger
        self._context: dict[str, Any] = {}

    def bind(self, **kwargs) -> "StructuredLogger":
        """Return a new logger with bound context fields."""
        new_logger = StructuredLogger(self._logger)
        new_logger._context = {**self._context, **kwargs}
        return new_logger

    def with_workflow(self, workflow_id: str) -> "StructuredLogger":
        """Bind workflow context for correlation."""
        return self.bind(
            workflow_id=workflow_id,
            trace_id=workflow_id,  # Use workflow_id as trace_id
        )

    def bind_activity(self, name: str, **kwargs) -> "StructuredLogger":
        """
        Magic helper for Temporal activities.
        - Automatically extracts workflow_id from activity context
        - Sets sxd_core.audit trace_id
        - Binds activity name and any other kwargs
        """
        trace_id = None
        try:
            from temporalio import activity

            trace_id = activity.info().workflow_id
        except (ImportError, RuntimeError):
            pass

        if trace_id:
            try:
                from sxd_core.audit import set_trace_id

                set_trace_id(trace_id)
            except ImportError:
                pass

        return self.with_workflow(str(trace_id or "")).bind(activity=name, **kwargs)

    def _log(self, level: int, message: str, **kwargs):
        # Capture special logging parameters
        exc_info = kwargs.pop("exc_info", None)
        stack_info = kwargs.pop("stack_info", False)
        stacklevel = kwargs.pop("stacklevel", 1)

        # 1. Standard structured logging
        extra_data = {**self._context, **kwargs}
        extra = {"structured_data": extra_data}

        self._logger.log(
            level,
            message,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel + 1,  # Adjust for this wrapper
            extra=extra,
        )

        # 2. ClickHouse ingestion (Skip during unit tests or if explicitly disabled)
        if os.environ.get("SXD_DISABLE_CLICKHOUSE_LOGS") == "1" or os.environ.get(
            "PYTEST_CURRENT_TEST"
        ):
            return

        try:
            from sxd_core.clickhouse import ClickHouseManager

            # Global singleton-ish access would be better, but for now we'll just be careful
            ch = ClickHouseManager()
            client = ch.client
            if client:
                now = datetime.now(timezone.utc)
                trace_id = extra_data.get("trace_id") or extra_data.get(
                    "workflow_id", ""
                )
                job_id = extra_data.get("job_id", "")
                activity_name = extra_data.get("activity", "")

                # Filter out system fields from details
                details = {
                    k: v
                    for k, v in extra_data.items()
                    if k not in ("trace_id", "workflow_id", "job_id", "activity")
                }

                row = [
                    now,
                    logging.getLevelName(level),
                    self._logger.name,
                    message,
                    str(trace_id),
                    str(job_id),
                    str(activity_name),
                    json.dumps(details),
                ]
                ch.insert_logs([row])
        except Exception:
            # Silent failure for logging to prevent recursion or main logic crashes
            pass

    def debug(self, message: str, **kwargs):
        self._log(logging.DEBUG, message, **kwargs)

    def info(self, message: str, **kwargs):
        self._log(logging.INFO, message, **kwargs)

    def warning(self, message: str, **kwargs):
        self._log(logging.WARNING, message, **kwargs)

    def error(self, message: str, **kwargs):
        self._log(logging.ERROR, message, **kwargs)

    def exception(self, message: str, **kwargs):
        # Handle exception specifically to capture traceback
        if "exc_info" not in kwargs:
            kwargs["exc_info"] = sys.exc_info()
        self._log(logging.ERROR, message, **kwargs)


# Module-level setup (runs once on import)
_initialized = False


def _init_logging(force: bool = False):
    global _initialized, _root_logger
    if _initialized and not force:
        return

    # Configure root logger for sxd namespace
    _root_logger = logging.getLogger("sxd")
    _root_logger.setLevel(logging.INFO)

    # Remove any existing handlers
    # NOTE: Using a list copy to safely remove items while iterating
    for handler in list(_root_logger.handlers):
        _root_logger.removeHandler(handler)

    # Add structured handler to stdout
    # In tests, sys.stdout might be replaced by pytest (capsys)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(StructuredFormatter())
    _root_logger.addHandler(handler)

    # Prevent propagation to root logger (avoids duplicate logs)
    # Most systems (Docker/Systemd) capture stdout directly.
    _root_logger.propagate = False

    _initialized = True


def get_logger(name: str) -> StructuredLogger:
    """
    Get a structured logger for the given module.

    Args:
        name: Usually __name__ from the calling module

    Returns:
        StructuredLogger with JSON output
    """
    _init_logging()

    # Ensure all our loggers are under the sxd namespace
    if not name.startswith("sxd.") and name != "sxd":
        name = f"sxd.{name}"

    return StructuredLogger(logging.getLogger(name))


def _get_current_logger() -> StructuredLogger:
    """Get the context-local logger or return a default one."""
    try:
        return _current_logger.get()
    except LookupError:
        return get_logger("default")


# Global proxy functions for convenience inside @sxd_activity
def debug(message: str, **kwargs):
    _get_current_logger().debug(message, **kwargs)


def info(message: str, **kwargs):
    _get_current_logger().info(message, **kwargs)


def warning(message: str, **kwargs):
    _get_current_logger().warning(message, **kwargs)


def error(message: str, **kwargs):
    _get_current_logger().error(message, **kwargs)


def exception(message: str, **kwargs):
    _get_current_logger().exception(message, **kwargs)


def sxd_activity(func: Callable[..., T]) -> Callable[..., T]:
    """
    Decorator for activities that provides magic logging.
    - Automates bind_activity() using function name
    - Injects job_id if present in kwargs
    - Sets up context-local logger for global info/warning/etc calls
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract job_id from kwargs or args if it exists
        job_id = kwargs.get("job_id")

        # Get a base logger for the module where the function is defined
        logger = get_logger(func.__module__)

        # Bind activity context
        ctx_logger = logger.bind_activity(
            func.__name__, **({"job_id": job_id} if job_id else {})
        )

        # Set the context-local logger
        token = _current_logger.set(ctx_logger)
        try:
            return func(*args, **kwargs)
        finally:
            _current_logger.reset(token)

    # Register the wrapper with sxd-core registry so the worker can find it
    # We delay import to avoid circular dependency if registry imports logging (it doesn't currently)
    try:
        from sxd_core.registry import register_activity

        # We don't know the task queue here, so we register globally (default)
        register_activity(wrapper, name=func.__name__)
    except ImportError:
        pass

    return wrapper
