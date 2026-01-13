"""Agent Observability SDK for Python.

A production-ready SDK for logging agent decisions, API calls, and transactions
with cost tracking and compliance audit trails.

Auto-registration Example (NEW in v1.1.0):
    >>> from agent_observability import log_event
    >>> log_event("decision", {"model": "gpt-4", "action": "summarize"})
    # Auto-registers and displays:
    # ✅ Agent Observability - Auto-registered!
    # 📋 Your API key: ao_live_abc123...

Traditional Example:
    >>> from agent_observability import AgentLogger
    >>> logger = AgentLogger(api_key="ao_live_...")
    >>> logger.log("api_call", {"provider": "openai", "cost_usd": 0.002})
"""
from __future__ import annotations

from typing import Any, Optional
from uuid import UUID

from agent_observability.client import AgentLogger

# Alias for convenience - users expect AgentObservability class from agent_observability package
AgentObservability = AgentLogger
from agent_observability.models import LogEntry, LogMetadata
from agent_observability.exceptions import (
    AgentObservabilityError,
    AuthenticationError,
    RateLimitError,
    APIError,
    ConnectionError,
    ValidationError,
)

__version__ = "1.4.1"

# Module-level logger for convenience function
_default_logger: Optional[AgentLogger] = None


def log_event(
    event_type: str,
    metadata: dict[str, Any] | None = None,
    **kwargs,
) -> Optional[UUID]:
    """
    Quick log function - auto-registers if needed.
    
    This is a convenience function that creates a shared AgentLogger instance
    and logs events with minimal boilerplate.
    
    Args:
        event_type: Type of event (api_call, decision, transaction, error, etc.)
        metadata: Event metadata (provider, cost_usd, latency_ms, etc.)
        **kwargs: Additional arguments passed to logger.log()
    
    Returns:
        Log ID if successful, None if failed
    
    Example:
        >>> from agent_observability import log_event
        >>> log_event("decision", {"model": "gpt-4", "action": "summarize"})
    """
    global _default_logger
    
    if _default_logger is None:
        _default_logger = AgentLogger()
    
    return _default_logger.log(event_type, metadata, **kwargs)


__all__ = [
    "AgentLogger",
    "AgentObservability",  # Alias for AgentLogger
    "LogEntry",
    "LogMetadata",
    "AgentObservabilityError",
    "AuthenticationError",
    "RateLimitError",
    "APIError",
    "ConnectionError",
    "ValidationError",
    "log_event",
]
