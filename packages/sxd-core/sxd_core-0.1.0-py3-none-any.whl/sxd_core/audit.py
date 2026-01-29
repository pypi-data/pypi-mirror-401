"""
Audit logging for SXD platform.

Provides SOC 2 compliant audit trail with:
- User identity tracking
- Customer context
- Action logging with status
- ClickHouse persistence

Usage:
    from sxd_core.audit import log_audit_event

    log_audit_event(
        actor="user:satyam",
        action="job.submit",
        target="video-123",
        status="SUCCESS",
        customer_id="acme_corp",
        details={"video_url": "..."},
    )
"""

import contextvars
import json
import os
from datetime import datetime, timezone
from typing import Optional

from sxd_core.logging import get_logger

audit_logger = get_logger("sxd.audit")

# --- Context Variables ---

_trace_id_ctx: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "sxd_trace_id", default=None
)

_user_id_ctx: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "sxd_user_id", default=None
)

_customer_id_ctx: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "sxd_customer_id", default=None
)


def set_trace_id(trace_id: str):
    """Set the current trace ID for correlation."""
    return _trace_id_ctx.set(trace_id)


def get_trace_id() -> Optional[str]:
    """Get the current trace ID."""
    return _trace_id_ctx.get()


def set_user_context(user_id: str):
    """Set the current user ID for audit logging."""
    return _user_id_ctx.set(user_id)


def get_user_context() -> Optional[str]:
    """Get the current user ID."""
    return _user_id_ctx.get()


def set_customer_context(customer_id: str):
    """Set the current customer ID for audit logging."""
    return _customer_id_ctx.set(customer_id)


def get_customer_context() -> Optional[str]:
    """Get the current customer ID."""
    return _customer_id_ctx.get()


# --- ClickHouse Integration ---

_ch_mgr = None


def get_clickhouse_manager():
    """Get or create the ClickHouse manager instance."""
    global _ch_mgr
    if _ch_mgr is None:
        try:
            from sxd_core.clickhouse import ClickHouseManager

            _ch_mgr = ClickHouseManager()
        except ImportError:
            pass
    return _ch_mgr


# --- Audit Event Logging ---


def log_audit_event(
    actor: str,
    action: str,
    target: str,
    status: str,
    customer_id: Optional[str] = None,
    details: Optional[dict] = None,
    client_ip: Optional[str] = None,
    trace_id: Optional[str] = None,
):
    """
    Log a security-relevant event for SOC 2 audit trail.

    Writes to both standard logging (stdout) and ClickHouse for persistence.

    Args:
        actor: Who performed the action (e.g., "user:satyam", "system:worker").
        action: What action was performed (e.g., "job.submit", "node.ssh").
        target: What resource was affected (e.g., "video-123", "sxd-master").
        status: Result of the action ("SUCCESS", "FAILURE", "DENIED").
        customer_id: Optional customer ID for scoped actions.
        details: Optional additional details as a dictionary.
        client_ip: Optional client IP address.
        trace_id: Optional trace ID for correlation.

    Example:
        log_audit_event(
            actor="user:operator1",
            action="job.submit",
            target="batch-abc123",
            status="SUCCESS",
            customer_id="acme_corp",
            details={"video_count": 10},
        )
    """
    env = os.environ.get("SXD_ENV", "dev")
    t_id = trace_id or get_trace_id()
    c_id = customer_id or get_customer_context()
    now = datetime.now(timezone.utc)

    # Build details with customer_id included
    full_details = details.copy() if details else {}
    if c_id:
        full_details["customer_id"] = c_id

    # 1. Standard structured logging (stdout fallback if ClickHouse unavailable)
    audit_logger.info(
        f"{action} by {actor}",
        event_type="audit",
        actor=actor,
        action=action,
        target=target,
        status=status,
        environment=env,
        # customer_id=c_id,  <-- Removed to avoid collision with **full_details
        client_ip=client_ip,
        trace_id=t_id,
        **full_details,
    )

    # 2. Direct ClickHouse ingestion
    if os.environ.get("SXD_DISABLE_CLICKHOUSE_AUDIT") == "1" or os.environ.get(
        "PYTEST_CURRENT_TEST"
    ):
        return

    ch = get_clickhouse_manager()
    if ch and ch.client:
        try:
            # Row format matches audit_events table schema
            # Note: customer_id is included in details JSON
            row = [
                now,
                actor,
                action,
                str(target),
                status,
                env,
                str(client_ip or ""),
                str(t_id or ""),
                json.dumps(full_details),
            ]
            ch.insert_audit_events([row])
        except Exception as e:
            # Don't let audit logging failure crash the main process
            audit_logger.warning(
                "Failed to write audit event to ClickHouse", error=str(e)
            )


def log_permission_denied(
    user_id: str,
    action: str,
    resource: str,
    customer_id: Optional[str] = None,
    required_permission: Optional[str] = None,
):
    """
    Log a permission denied event.

    Convenience function for logging access denials.

    Args:
        user_id: The user who was denied.
        action: The action they attempted.
        resource: The resource they tried to access.
        customer_id: Optional customer ID.
        required_permission: The permission that was required.
    """
    log_audit_event(
        actor=f"user:{user_id}",
        action=action,
        target=resource,
        status="DENIED",
        customer_id=customer_id,
        details={
            "reason": "permission_denied",
            "required_permission": required_permission,
        },
    )


def log_auth_failure(
    reason: str,
    client_ip: Optional[str] = None,
    details: Optional[dict] = None,
):
    """
    Log an authentication failure.

    Args:
        reason: Why authentication failed (e.g., "invalid_api_key", "user_inactive").
        client_ip: Optional client IP address.
        details: Optional additional details.
    """
    log_audit_event(
        actor="anonymous",
        action="auth.login",
        target="system",
        status="FAILURE",
        details={"reason": reason, **(details or {})},
        client_ip=client_ip,
    )


def log_auth_success(
    user_id: str,
    client_ip: Optional[str] = None,
):
    """
    Log a successful authentication.

    Args:
        user_id: The user who authenticated.
        client_ip: Optional client IP address.
    """
    log_audit_event(
        actor=f"user:{user_id}",
        action="auth.login",
        target="system",
        status="SUCCESS",
        client_ip=client_ip,
    )


# --- Exports ---

__all__ = [
    "log_audit_event",
    "log_permission_denied",
    "log_auth_failure",
    "log_auth_success",
    "set_trace_id",
    "get_trace_id",
    "set_user_context",
    "get_user_context",
    "set_customer_context",
    "get_customer_context",
]


# Example usage during import test
if __name__ == "__main__":
    log_audit_event(
        actor="user:satyam",
        action="test.run",
        target="audit.py",
        status="SUCCESS",
        customer_id="test_customer",
        details={"note": "test event"},
    )
