"""Main client for the Agent Observability SDK."""
from __future__ import annotations

import asyncio
import json
import logging
import os
import socket
import time
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Generator, Optional
from uuid import UUID, uuid4

import httpx

from agent_observability.models import LogEntry, LogMetadata
from agent_observability.env_loader import load_from_env, save_to_env

logger = logging.getLogger("agent_observability")

# Module-level cache to prevent duplicate registrations across instances
_REGISTRATION_CACHE: dict[str, str] = {}  # agent_id -> api_key


class CircuitBreaker:
    """Circuit breaker to prevent cascade failures."""

    def __init__(
        self,
        failure_threshold: int = 5,
        reset_timeout: float = 60.0,
    ):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.last_failure_time: float | None = None
        self.state = "closed"  # closed, open, half-open

    def record_success(self):
        """Record a successful call."""
        self.failures = 0
        self.state = "closed"

    def record_failure(self):
        """Record a failed call."""
        self.failures += 1
        self.last_failure_time = time.time()

        if self.failures >= self.failure_threshold:
            self.state = "open"
            logger.warning("Circuit breaker opened")

    def is_open(self) -> bool:
        """Check if the circuit breaker is open."""
        if self.state == "closed":
            return False

        if self.state == "open":
            # Check if reset timeout has passed
            if self.last_failure_time and (time.time() - self.last_failure_time) >= self.reset_timeout:
                self.state = "half-open"
                return False
            return True

        return False  # half-open allows one request


class TaskContext:
    """Context manager for tracking a task with automatic timing."""

    def __init__(self, logger: "AgentLogger", task_name: str, context_id: UUID | None = None):
        self.logger = logger
        self.task_name = task_name
        self.context_id = context_id or uuid4()
        self.start_time: float | None = None
        self.metadata: dict[str, Any] = {}

    def __enter__(self) -> "TaskContext":
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        latency_ms = int((time.time() - self.start_time) * 1000) if self.start_time else 0
        self.metadata["latency_ms"] = latency_ms

        if exc_type:
            # Log error
            self.logger.log(
                "error",
                {
                    **self.metadata,
                    "error_message": str(exc_val),
                },
                agent_id=self.task_name,
                severity="error",
                context_id=self.context_id,
            )
        else:
            # Log success
            self.logger.log(
                "state_change",
                self.metadata,
                agent_id=self.task_name,
                severity="info",
                context_id=self.context_id,
            )

        return False  # Don't suppress exceptions

    def log_cost(self, cost_usd: float):
        """Log cost for this task."""
        self.metadata["cost_usd"] = cost_usd

    def log_metadata(self, data: dict[str, Any]):
        """Add metadata to this task."""
        self.metadata.update(data)


class BatchContext:
    """Context manager for batch logging."""

    def __init__(self, logger: "AgentLogger"):
        self.logger = logger
        self.logs: list[LogEntry] = []

    def __enter__(self) -> "BatchContext":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.logs and not exc_type:
            self.logger._send_batch(self.logs)
        return False

    def log(
        self,
        event_type: str,
        metadata: dict[str, Any] | None = None,
        agent_id: str | None = None,
        severity: str = "info",
        tags: list[str] | None = None,
        context_id: UUID | None = None,
    ):
        """Add a log entry to the batch."""
        entry = LogEntry(
            agent_id=agent_id or self.logger.default_agent_id or "unknown",
            event_type=event_type,
            severity=severity,
            metadata=metadata,
            tags=tags or [],
            context_id=context_id,
        )
        self.logs.append(entry)


class AgentLogger:
    """
    Main client for the Agent Observability API.

    Features:
    - Automatic retries with exponential backoff
    - Circuit breaker to prevent cascade failures
    - Local file fallback when API is unavailable
    - Async mode for non-blocking logs
    - Batch logging for efficiency
    """

    DEFAULT_BASE_URL = "https://api-production-0c55.up.railway.app"
    DEFAULT_TIMEOUT = 10.0
    MAX_RETRIES = 3

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        agent_id: Optional[str] = None,
        default_agent_id: Optional[str] = None,  # Deprecated alias for agent_id
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = MAX_RETRIES,
        fallback_path: Optional[str] = None,
        async_mode: bool = False,
        registration_source: Optional[str] = None,
    ):
        """
        Initialize the Agent Observability logger.

        Args:
            api_key: API key for authentication. If not provided, reads from
                     AGENT_OBS_API_KEY environment variable. If still not found,
                     auto-registers on first log() call.
            base_url: Base URL for the API. Defaults to production Railway URL.
            agent_id: Agent ID for registration and logs. Auto-generated if not provided.
            default_agent_id: Deprecated alias for agent_id.
            timeout: Request timeout in seconds.
            max_retries: Maximum number of retries for failed requests.
            fallback_path: Path for local fallback logs when API is unavailable.
            async_mode: If True, logs are sent asynchronously.
            registration_source: SDK name for tracking (e.g., "agent-observability-langchain").
        """
        # Try to load from .env first to prevent duplicate registrations
        env_api_key, env_agent_id = load_from_env()
        
        self.api_key = api_key or env_api_key or os.environ.get("AGENT_OBS_API_KEY")
        self.base_url = (base_url or os.environ.get("AGENT_OBS_BASE_URL") or self.DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.fallback_path = fallback_path or os.path.expanduser("~/.agent_observability/fallback.jsonl")
        self.async_mode = async_mode
        self.registration_source = registration_source or "agent-observability"
        
        # Auto-registration state
        self._auto_registered = False
        self._registration_shown = False
        self._fallback_mode = False
        
        # Use provided agent ID, or from .env, or generate new one
        # This prevents duplicate registrations
        self.agent_id = agent_id or default_agent_id or env_agent_id or self._generate_agent_id()
        self.default_agent_id = self.agent_id
        
        # If we loaded from .env, mark as already registered
        if env_api_key:
            self._auto_registered = True

        self._circuit_breaker = CircuitBreaker()
        
        # Initialize client - may be re-initialized after auto-registration
        self._init_client()

    def _init_client(self):
        """Initialize or re-initialize the HTTP client."""
        headers = {}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        
        self._client = httpx.Client(
            base_url=self.base_url,
            headers=headers,
            timeout=self.timeout,
        )

    def _generate_agent_id(self) -> str:
        """Generate unique agent ID from hostname + UUID suffix."""
        try:
            hostname = socket.gethostname()[:20]  # Truncate long hostnames
        except Exception:
            hostname = "agent"
        suffix = str(uuid4())[:8]
        return f"{hostname}-{suffix}"

    def _auto_register(self) -> Optional[dict]:
        """
        Auto-register with retry logic and fallbacks.
        
        Returns:
            Registration response dict with api_key, or None if failed.
        """
        global _REGISTRATION_CACHE
        
        # Check module-level cache first
        if self.agent_id in _REGISTRATION_CACHE:
            cached_key = _REGISTRATION_CACHE[self.agent_id]
            logger.debug(f"Using cached API key for agent {self.agent_id}")
            return {"api_key": cached_key, "cached": True}
        
        for attempt in range(3):
            try:
                response = httpx.post(
                    f"{self.base_url}/v1/register",
                    json={
                        "agent_id": self.agent_id, 
                        "auto_registered": True,
                        "registration_source": self.registration_source,
                    },
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()
                
                # Cache the API key
                if data.get("api_key") and not data["api_key"].endswith("...(stored)"):
                    _REGISTRATION_CACHE[self.agent_id] = data["api_key"]
                
                if not self._registration_shown:
                    # Save API key to .env for easy reuse
                    saved_to_env = self._save_to_env(data["api_key"])
                    self._show_registration_message(data["api_key"], saved_to_env=saved_to_env)
                    self._registration_shown = True
                    
                    # Auto-log activation event to ensure user sees something immediately
                    self._auto_log_activation()
                
                return data
                
            except httpx.TimeoutException:
                if attempt < 2:
                    time.sleep(2 ** attempt)  # Exponential backoff: 1s, 2s
                    continue
                # Final attempt failed - enable fallback
                print("⚠️  Registration timed out. Logging to local file.")
                self._fallback_mode = True
                return None
                
            except httpx.HTTPStatusError as e:
                if e.response.status_code >= 500 and attempt < 2:
                    time.sleep(2 ** attempt)
                    continue
                elif e.response.status_code == 409:
                    # Already registered - response contains message about existing key
                    try:
                        data = e.response.json()
                        if not self._registration_shown:
                            print(f"\n✅ Agent '{self.agent_id}' already registered.")
                            print(f"   Use your existing API key from initial registration.\n")
                            self._registration_shown = True
                        return data
                    except Exception:
                        pass
                    return None
                else:
                    print(f"❌ Registration failed: {e.response.text}")
                    self._fallback_mode = True
                    return None
                    
            except httpx.RequestError as e:
                if attempt < 2:
                    time.sleep(2 ** attempt)
                    continue
                print(f"⚠️  Network error. Using local fallback.")
                self._fallback_mode = True
                return None
        
        self._fallback_mode = True
        return None

    def _save_to_env(self, api_key: str) -> bool:
        """Save API key and agent ID to .env file.
        
        Returns True if saved successfully, False otherwise.
        """
        return save_to_env(api_key, self.agent_id)

    def _show_registration_message(self, api_key: str, saved_to_env: bool = False):
        """Display highly visible registration message with colors and next steps."""
        # ANSI color codes for terminal visibility
        GREEN = "\033[1;32m"
        YELLOW = "\033[1;33m"
        CYAN = "\033[1;36m"
        BOLD = "\033[1m"
        RESET = "\033[0m"
        
        print(f"\n{GREEN}{'=' * 60}{RESET}")
        print(f"{GREEN}  ✅ Agent Observability - You're Registered!{RESET}")
        print(f"{GREEN}{'=' * 60}{RESET}")
        
        print(f"\n{BOLD}API Key:{RESET} {api_key}")
        print(f"{BOLD}Agent ID:{RESET} {self.agent_id}")
        
        if saved_to_env:
            print(f"\n{YELLOW}💾 Saved to .env{RESET} - remember to add .env to .gitignore!")
        else:
            print(f"\n{BOLD}Set in your environment:{RESET}")
            print(f"  export AGENT_OBS_API_KEY={api_key}")
        
        print(f"\n{CYAN}🎯 View Your Dashboard:{RESET}")
        print(f"  https://agentobs.manus.space/login")
        print(f"  {YELLOW}(Use your API key above to sign in){RESET}")
        
        print(f"\n{CYAN}📚 Documentation:{RESET}")
        print(f"  https://github.com/blueskylineassets/agent-observability#readme")
        
        print(f"\n{BOLD}Next step:{RESET} Log your first event:")
        print(f"  from agent_observability import log_event")
        print(f"  log_event('api_call', {{'model': 'gpt-4', 'cost_usd': 0.02}})")
        
        print(f"\n{BOLD}Free Tier:{RESET} 1,000 logs/month | {BOLD}Pricing:{RESET} https://blueskylineassets.github.io/agent-observability/dashboard/pricing.html")
        print(f"{GREEN}{'=' * 60}{RESET}\n")

    def _auto_log_activation(self):
        """Automatically log an activation event to confirm SDK is working."""
        try:
            # Log activation event silently (no print output)
            self.log(
                "sdk_activation",
                {
                    "event": "first_install",
                    "agent_id": self.agent_id,
                    "sdk_version": "1.4.1",
                    "auto_logged": True,
                },
                severity="info",
            )
            
            # Show activation success - confirm logging works
            GREEN = "\033[1;32m"
            RESET = "\033[0m"
            
            print(f"{GREEN}🎉 Test log sent successfully!{RESET} Your SDK is working.")
            print(f"   Now log your AI agent events with: log_event('api_call', {{'model': 'gpt-4'}})\n")
            
        except Exception as e:
            # Silently fail - don't interrupt user flow
            logger.debug(f"Auto-activation log failed: {e}")

    def _parse_metadata(self, metadata: dict[str, Any] | LogMetadata | None) -> LogMetadata:
        """
        Parse metadata into LogMetadata, handling arbitrary keys gracefully.
        
        Unknown keys are placed in the 'custom' field.
        """
        if metadata is None:
            return LogMetadata()
        
        if isinstance(metadata, LogMetadata):
            return metadata
        
        # Known LogMetadata fields
        known_fields = {
            'provider', 'api_endpoint', 'method', 'status_code', 'latency_ms',
            'cost_usd', 'tokens_used', 'model', 'decision_reason',
            'alternatives_considered', 'error_message', 'retry_count', 'custom'
        }
        
        # Split known and unknown keys
        known_data = {}
        custom_data = {}
        
        for key, value in metadata.items():
            if key in known_fields:
                known_data[key] = value
            else:
                custom_data[key] = value
        
        # Merge unknown keys into custom field
        if custom_data:
            if 'custom' in known_data and isinstance(known_data['custom'], dict):
                known_data['custom'].update(custom_data)
            else:
                known_data['custom'] = custom_data
        
        return LogMetadata(**known_data)

    def _ensure_registered(self):
        """Ensure we have an API key (auto-register if needed)."""
        if self.api_key:
            return  # Already have key
        
        if self._auto_registered:
            return  # Already tried to register
        
        if self._fallback_mode:
            return  # Already in fallback mode
        
        # Try to auto-register
        result = self._auto_register()
        self._auto_registered = True
        
        if result and result.get("api_key"):
            if result["api_key"].endswith("...(stored)"):
                # Agent was already registered - user needs to use their saved key
                print("\n⚠️  This agent was already registered.")
                print("💾 Set your saved API key: export AGENT_OBS_API_KEY=ao_live_...")
                print("   Or pass it directly: AgentObservability(api_key='ao_live_...')\n")
                self._fallback_mode = True
            else:
                self.api_key = result["api_key"]
                # Reinitialize client with new API key
                self._init_client()

    def log(
        self,
        event_type: str,
        metadata: dict[str, Any] | LogMetadata | None = None,
        agent_id: Optional[str] = None,
        severity: str = "info",
        request_body: Optional[str] = None,
        response_body: Optional[str] = None,
        tags: Optional[list[str]] = None,
        context_id: Optional[UUID] = None,
        timestamp: Optional[datetime] = None,
    ) -> Optional[UUID]:
        """
        Log a single event.

        Args:
            event_type: Type of event (any string, e.g., api_call, decision, test, custom_event)
            metadata: Event metadata (provider, cost_usd, latency_ms, etc.)
            agent_id: Agent identifier (uses default if not provided)
            severity: Log severity (debug, info, warning, error, critical)
            request_body: Request body to log (truncated to 10KB)
            response_body: Response body to log (truncated to 10KB)
            tags: Tags for filtering
            context_id: ID for grouping related logs
            timestamp: Custom timestamp (defaults to now)

        Returns:
            Log ID if successful, None if failed
        """
        # Auto-register on first call if no API key
        self._ensure_registered()
        
        # If in fallback mode, write to local file
        if self._fallback_mode and not self.api_key:
            entry = LogEntry(
                agent_id=agent_id or self.default_agent_id or "unknown",
                event_type=event_type,
                severity=severity,
                metadata=self._parse_metadata(metadata),
                request_body=request_body,
                response_body=response_body,
                tags=tags or [],
                context_id=context_id,
                timestamp=timestamp,
            )
            self._write_fallback(entry)
            return None
        
        entry = LogEntry(
            agent_id=agent_id or self.default_agent_id or "unknown",
            event_type=event_type,
            severity=severity,
            metadata=self._parse_metadata(metadata),
            request_body=request_body,
            response_body=response_body,
            tags=tags or [],
            context_id=context_id,
            timestamp=timestamp,
        )

        if self.async_mode:
            # Fire and forget
            try:
                asyncio.get_event_loop().run_in_executor(None, self._send_log, entry)
            except RuntimeError:
                # No event loop, run synchronously
                self._send_log(entry)
            return None
        else:
            return self._send_log(entry)

    def _send_log(self, entry: LogEntry) -> Optional[UUID]:
        """Send a single log entry with retries."""
        if self._circuit_breaker.is_open():
            logger.warning("Circuit breaker open, using fallback")
            self._write_fallback(entry)
            return None

        for attempt in range(self.max_retries):
            try:
                response = self._client.post(
                    "/v1/logs",
                    json=entry.to_dict(),
                )
                response.raise_for_status()

                self._circuit_breaker.record_success()
                return UUID(response.json()["id"])

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    # Rate limited, wait and retry
                    retry_after = int(e.response.headers.get("Retry-After", 60))
                    time.sleep(min(retry_after, 60))
                elif e.response.status_code >= 500:
                    # Server error, retry with backoff
                    self._circuit_breaker.record_failure()
                    time.sleep(2 ** attempt)
                else:
                    # Client error, don't retry
                    logger.error(f"Log failed: {e.response.text}")
                    return None

            except httpx.RequestError as e:
                self._circuit_breaker.record_failure()
                logger.warning(f"Request error (attempt {attempt + 1}): {e}")
                time.sleep(2 ** attempt)

        # All retries failed, use fallback
        logger.error("All retries failed, using fallback")
        self._write_fallback(entry)
        return None

    def _send_batch(self, entries: list[LogEntry]) -> int:
        """Send a batch of log entries."""
        if self._circuit_breaker.is_open():
            logger.warning("Circuit breaker open, using fallback for batch")
            for entry in entries:
                self._write_fallback(entry)
            return 0

        for attempt in range(self.max_retries):
            try:
                response = self._client.post(
                    "/v1/logs/batch",
                    json={"logs": [e.to_dict() for e in entries]},
                )
                response.raise_for_status()

                self._circuit_breaker.record_success()
                result = response.json()
                return result["accepted"]

            except httpx.HTTPStatusError as e:
                if e.response.status_code >= 500:
                    self._circuit_breaker.record_failure()
                    time.sleep(2 ** attempt)
                else:
                    logger.error(f"Batch log failed: {e.response.text}")
                    return 0

            except httpx.RequestError as e:
                self._circuit_breaker.record_failure()
                logger.warning(f"Batch request error (attempt {attempt + 1}): {e}")
                time.sleep(2 ** attempt)

        # All retries failed
        logger.error("Batch: all retries failed, using fallback")
        for entry in entries:
            self._write_fallback(entry)
        return 0

    def _write_fallback(self, entry: LogEntry):
        """Write log to local fallback file."""
        try:
            path = Path(self.fallback_path)
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, "a") as f:
                data = entry.to_dict()
                data["_fallback_time"] = datetime.utcnow().isoformat()
                f.write(json.dumps(data) + "\n")

        except Exception as e:
            logger.error(f"Failed to write fallback log: {e}")

    def task(self, task_name: str, context_id: UUID | None = None) -> TaskContext:
        """
        Create a task context for automatic timing and logging.

        Example:
            with logger.task("generate_image") as task:
                result = call_api()
                task.log_cost(0.02)
        """
        return TaskContext(self, task_name, context_id)

    def batch(self) -> BatchContext:
        """
        Create a batch context for efficient batch logging.

        Example:
            with logger.batch() as batch:
                for i in range(1000):
                    batch.log("event", {"index": i})
        """
        return BatchContext(self)

    def close(self):
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self) -> "AgentLogger":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

