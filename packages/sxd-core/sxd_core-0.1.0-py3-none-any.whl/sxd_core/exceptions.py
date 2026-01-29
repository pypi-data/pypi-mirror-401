"""
Custom exception hierarchy for SXD.

Provides structured exceptions with trace_id support for better error tracking,
debugging, and observability.

Usage:
    from sxd_core.exceptions import (
        SXDError,
        StorageError,
    )

    try:
        # ... some operation
    except StorageError as e:
        logger.error("Storage failed", trace_id=e.trace_id, context=e.context)
        raise
"""

import builtins
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Type


@dataclass
class ErrorContext:
    """Structured error context for debugging."""

    trace_id: Optional[str] = None
    job_id: Optional[str] = None
    workflow_id: Optional[str] = None
    activity_name: Optional[str] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for logging/serialization."""
        result = {
            "trace_id": self.trace_id,
            "job_id": self.job_id,
            "workflow_id": self.workflow_id,
            "activity_name": self.activity_name,
            "timestamp": self.timestamp.isoformat(),
        }
        result.update(self.extra)
        return {k: v for k, v in result.items() if v is not None}


class SXDError(Exception):
    """
    Base exception for all SXD errors.

    Provides structured context including trace_id for correlation.

    Attributes:
        message: Human-readable error message.
        trace_id: Optional trace ID for correlation across services.
        context: Additional structured context for debugging.
        cause: Original exception that caused this error.
    """

    def __init__(
        self,
        message: str,
        trace_id: Optional[str] = None,
        cause: Optional[Exception] = None,
        **context,
    ):
        self.message = message
        self.trace_id = trace_id
        self.context = ErrorContext(trace_id=trace_id, extra=context)
        self.cause = cause
        super().__init__(message)

    def __str__(self) -> str:
        parts = [self.message]
        if self.trace_id:
            parts.append(f"[trace_id={self.trace_id}]")
        if self.cause:
            parts.append(f"caused by: {self.cause}")
        return " ".join(parts)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for logging/serialization."""
        return {
            "error_type": self.__class__.__name__,
            "message": self.message,
            "trace_id": self.trace_id,
            "context": self.context.to_dict(),
            "cause": str(self.cause) if self.cause else None,
        }


# =============================================================================
# Configuration Errors
# =============================================================================


class ConfigurationError(SXDError):
    """Error in configuration loading or validation."""

    def __init__(
        self,
        message: str,
        config_key: Optional[str] = None,
        config_file: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(
            message, config_key=config_key, config_file=config_file, **kwargs
        )
        self.config_key = config_key
        self.config_file = config_file


class MissingConfigError(ConfigurationError):
    """Required configuration key is missing."""

    def __init__(self, key: str, config_file: Optional[str] = None, **kwargs):
        super().__init__(
            f"Missing required configuration: {key}",
            config_key=key,
            config_file=config_file,
            **kwargs,
        )


class InvalidConfigError(ConfigurationError):
    """Configuration value is invalid."""

    def __init__(
        self,
        key: str,
        value: Any,
        expected: str,
        config_file: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(
            f"Invalid configuration for '{key}': got {value!r}, expected {expected}",
            config_key=key,
            config_file=config_file,
            invalid_value=value,
            expected_type=expected,
            **kwargs,
        )


# =============================================================================
# Workflow Errors
# =============================================================================


class WorkflowError(SXDError):
    """Base class for workflow-related errors."""

    def __init__(
        self,
        message: str,
        workflow_id: Optional[str] = None,
        workflow_name: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(
            message,
            workflow_id=workflow_id,
            workflow_name=workflow_name,
            **kwargs,
        )
        self.workflow_id = workflow_id
        self.workflow_name = workflow_name


class WorkflowNotFoundError(WorkflowError):
    """Requested workflow does not exist."""

    def __init__(
        self,
        workflow_name: Optional[str] = None,
        workflow_id: Optional[str] = None,
        **kwargs,
    ):
        identifier = workflow_id or workflow_name
        super().__init__(
            f"Workflow not found: {identifier}",
            workflow_id=workflow_id,
            workflow_name=workflow_name,
            **kwargs,
        )


class WorkflowExecutionError(WorkflowError):
    """Workflow execution failed."""

    def __init__(
        self,
        message: str,
        workflow_id: Optional[str] = None,
        cause: Optional[Exception] = None,
        **kwargs,
    ):
        super().__init__(
            message,
            workflow_id=workflow_id,
            cause=cause,
            **kwargs,
        )


# =============================================================================
# Activity Errors
# =============================================================================


class ActivityError(SXDError):
    """Base class for activity-related errors."""

    def __init__(
        self,
        message: str,
        activity_name: Optional[str] = None,
        activity_id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(
            message,
            activity_name=activity_name,
            activity_id=activity_id,
            **kwargs,
        )
        self.activity_name = activity_name
        self.activity_id = activity_id


class ActivityTimeoutError(ActivityError):
    """Activity execution timed out."""

    def __init__(
        self,
        activity_name: str,
        timeout_seconds: float,
        activity_id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(
            f"Activity '{activity_name}' timed out after {timeout_seconds}s",
            activity_name=activity_name,
            activity_id=activity_id,
            timeout_seconds=timeout_seconds,
            **kwargs,
        )
        self.timeout_seconds = timeout_seconds


# =============================================================================
# Storage Errors
# =============================================================================


class StorageError(SXDError):
    """Base class for storage-related errors."""

    def __init__(
        self,
        message: str,
        path: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(message, path=path, **kwargs)
        self.path = path


class StorageAccessError(StorageError):
    """Failed to access storage location."""

    def __init__(
        self,
        path: str,
        operation: str = "access",
        cause: Optional[Exception] = None,
        **kwargs,
    ):
        super().__init__(
            f"Failed to {operation} storage path: {path}",
            path=path,
            operation=operation,
            cause=cause,
            **kwargs,
        )
        self.operation = operation


class StorageNotFoundError(StorageError):
    """Storage path does not exist."""

    def __init__(self, path: str, **kwargs):
        super().__init__(
            f"Storage path not found: {path}",
            path=path,
            **kwargs,
        )


class StorageQuotaError(StorageError):
    """Storage quota exceeded."""

    def __init__(
        self,
        path: str,
        required_bytes: int,
        available_bytes: int,
        **kwargs,
    ):
        super().__init__(
            f"Storage quota exceeded at {path}: need {required_bytes} bytes, "
            f"only {available_bytes} available",
            path=path,
            required_bytes=required_bytes,
            available_bytes=available_bytes,
            **kwargs,
        )
        self.required_bytes = required_bytes
        self.available_bytes = available_bytes


# =============================================================================
# Connection Errors
# =============================================================================


class SXDConnectionError(SXDError):
    """Base class for connection-related errors.

    Note: Named SXDConnectionError to avoid shadowing Python's built-in ConnectionError.
    """

    def __init__(
        self,
        message: str,
        host: Optional[str] = None,
        port: Optional[int] = None,
        **kwargs,
    ):
        super().__init__(message, host=host, port=port, **kwargs)
        self.host = host
        self.port = port


class TemporalConnectionError(SXDConnectionError):
    """Failed to connect to Temporal server."""

    def __init__(
        self,
        host: str,
        port: int,
        cause: Optional[Exception] = None,
        **kwargs,
    ):
        super().__init__(
            f"Failed to connect to Temporal at {host}:{port}",
            host=host,
            port=port,
            cause=cause,
            **kwargs,
        )


class ClickHouseConnectionError(SXDConnectionError):
    """Failed to connect to ClickHouse server."""

    def __init__(
        self,
        host: str,
        port: int,
        cause: Optional[Exception] = None,
        **kwargs,
    ):
        super().__init__(
            f"Failed to connect to ClickHouse at {host}:{port}",
            host=host,
            port=port,
            cause=cause,
            **kwargs,
        )


class SSHConnectionError(SXDConnectionError):
    """Failed to establish SSH connection."""

    def __init__(
        self,
        host: str,
        port: int = 22,
        user: Optional[str] = None,
        cause: Optional[Exception] = None,
        **kwargs,
    ):
        user_str = f"{user}@" if user else ""
        super().__init__(
            f"SSH connection failed to {user_str}{host}:{port}",
            host=host,
            port=port,
            user=user,
            cause=cause,
            **kwargs,
        )
        self.user = user


# =============================================================================
# Service Errors
# =============================================================================


class ServiceError(SXDError):
    """Base class for service-related errors."""

    def __init__(
        self,
        message: str,
        service_name: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(message, service_name=service_name, **kwargs)
        self.service_name = service_name


class ServiceUnavailableError(ServiceError):
    """Service is temporarily unavailable (circuit breaker open)."""

    def __init__(
        self,
        service_name: str,
        retry_after_seconds: Optional[float] = None,
        **kwargs,
    ):
        msg = f"Service '{service_name}' is temporarily unavailable"
        if retry_after_seconds:
            msg += f", retry after {retry_after_seconds}s"
        super().__init__(msg, service_name=service_name, **kwargs)
        self.retry_after_seconds = retry_after_seconds


class ServiceTimeoutError(ServiceError):
    """Service request timed out."""

    def __init__(
        self,
        service_name: str,
        timeout_seconds: float,
        **kwargs,
    ):
        super().__init__(
            f"Service '{service_name}' request timed out after {timeout_seconds}s",
            service_name=service_name,
            timeout_seconds=timeout_seconds,
            **kwargs,
        )
        self.timeout_seconds = timeout_seconds


# =============================================================================
# Data Errors
# =============================================================================


class DataError(SXDError):
    """Base class for data-related errors."""

    pass


class DataIntegrityError(DataError):
    """Data integrity check failed (e.g., checksum mismatch)."""

    def __init__(
        self,
        message: str,
        expected: Optional[str] = None,
        actual: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(message, expected=expected, actual=actual, **kwargs)
        self.expected = expected
        self.actual = actual


# =============================================================================
# Utility Functions
# =============================================================================


def wrap_exception(
    exc: Exception,
    wrapper_class: Type[SXDError] = SXDError,
    message: Optional[str] = None,
    trace_id: Optional[str] = None,
    **context,
) -> SXDError:
    """
    Wrap a generic exception in an SXD exception.

    Args:
        exc: The original exception.
        wrapper_class: The SXD exception class to use.
        message: Optional custom message (defaults to str(exc)).
        trace_id: Optional trace ID for correlation.
        **context: Additional context to include.

    Returns:
        An SXD exception wrapping the original.

    Example:
        try:
            external_library_call()
        except Exception as e:
            raise wrap_exception(e, StorageAccessError, trace_id=ctx.trace_id)
    """
    msg = message or str(exc)
    return wrapper_class(msg, trace_id=trace_id, cause=exc, **context)


def is_retryable(exc: Exception) -> bool:
    """
    Check if an exception is retryable.

    Returns True for transient errors that may succeed on retry:
    - Connection errors
    - Timeout errors
    - Service unavailable errors

    Args:
        exc: The exception to check.

    Returns:
        True if the exception is retryable.
    """
    retryable_types = (
        SXDConnectionError,
        builtins.ConnectionError,  # Python built-in
        ServiceUnavailableError,
        ServiceTimeoutError,
        ActivityTimeoutError,
        TimeoutError,
        OSError,  # Includes network errors
    )
    return isinstance(exc, retryable_types)


__all__ = [
    # Base
    "SXDError",
    "ErrorContext",
    # Configuration
    "ConfigurationError",
    "MissingConfigError",
    "InvalidConfigError",
    # Activity
    "ActivityError",
    "ActivityTimeoutError",
    # Workflow
    "WorkflowError",
    "WorkflowNotFoundError",
    "WorkflowExecutionError",
    # Storage
    "StorageError",
    "StorageAccessError",
    "StorageNotFoundError",
    "StorageQuotaError",
    # Connection
    "SXDConnectionError",
    "TemporalConnectionError",
    "ClickHouseConnectionError",
    "SSHConnectionError",
    # Service
    "ServiceError",
    "ServiceUnavailableError",
    "ServiceTimeoutError",
    # Data
    "DataError",
    "DataIntegrityError",
    # Utilities
    "wrap_exception",
    "is_retryable",
]
