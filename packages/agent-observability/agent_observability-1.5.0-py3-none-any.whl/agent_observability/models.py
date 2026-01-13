"""Data models for the Agent Observability SDK."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID


@dataclass
class LogMetadata:
    """Metadata for a log entry."""

    provider: str | None = None
    api_endpoint: str | None = None
    method: str | None = None
    status_code: int | None = None
    latency_ms: int | None = None
    cost_usd: float | None = None
    tokens_used: int | None = None
    model: str | None = None
    decision_reason: str | None = None
    alternatives_considered: list[str] | None = None
    error_message: str | None = None
    retry_count: int | None = None
    custom: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        return {k: v for k, v in self.__dict__.items() if v is not None}


@dataclass
class LogEntry:
    """A log entry to be sent to the API."""

    agent_id: str
    event_type: str
    severity: str = "info"
    metadata: LogMetadata | dict | None = None
    request_body: str | None = None
    response_body: str | None = None
    tags: list[str] = field(default_factory=list)
    context_id: UUID | None = None
    timestamp: datetime | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for API request."""
        data: dict[str, Any] = {
            "agent_id": self.agent_id,
            "event_type": self.event_type,
            "severity": self.severity,
            "tags": self.tags,
        }

        if self.metadata:
            if isinstance(self.metadata, LogMetadata):
                data["metadata"] = self.metadata.to_dict()
            else:
                data["metadata"] = self.metadata

        if self.request_body:
            data["request_body"] = self.request_body

        if self.response_body:
            data["response_body"] = self.response_body

        if self.context_id:
            data["context_id"] = str(self.context_id)

        if self.timestamp:
            data["timestamp"] = self.timestamp.isoformat()

        return data

