"""Exception classes for the Agent Observability SDK."""

from __future__ import annotations

from typing import Optional


class AgentObservabilityError(Exception):
    """Base exception for all Agent Observability errors."""
    pass


class AuthenticationError(AgentObservabilityError):
    """Raised when API key is invalid or missing."""
    pass


class RateLimitError(AgentObservabilityError):
    """Raised when rate limit is exceeded."""
    
    def __init__(self, message: str = "Rate limit exceeded", retry_after: Optional[int] = None):
        super().__init__(message)
        self.retry_after = retry_after


class APIError(AgentObservabilityError):
    """Raised when the API returns an error response."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, response_body: Optional[str] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class ConnectionError(AgentObservabilityError):
    """Raised when unable to connect to the API."""
    pass


class ValidationError(AgentObservabilityError):
    """Raised when request data fails validation."""
    pass

