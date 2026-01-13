# Agent Observability SDK

Python SDK for the Agent Observability platform - structured logging, cost tracking, and compliance audit trails for AI agents.

---

## Try It Now (30 seconds)

**Step 1: Install**
```bash
pip install agent-observability
```

**Step 2: Run this command**
```bash
python -c "from agent_observability import log_event; log_event('decision', {'source': 'readme_test'})"
```

**You'll see:**
```
============================================================
  ✅ Agent Observability - You're Registered!
============================================================

API Key: ao_live_abc123...
Agent ID: your-machine-abc123

💾 Saved to .env - remember to add .env to .gitignore!

📚 Getting Started Guide:
  https://blueskylineassets.github.io/agent-observability/dashboard/getting-started.html

Free Tier: 1,000 logs/month
============================================================
```

That's it! Your logs are now being collected. Follow the [Getting Started guide](https://blueskylineassets.github.io/agent-observability/dashboard/getting-started.html) for next steps.

---

## Get Started in Code

```python
from agent_observability import AgentLogger

logger = AgentLogger()  # Auto-registers on first use!
logger.log("decision", {"model": "gpt-4", "action": "summarize"})
```

**No signup. No API keys to copy. No configuration.**

## Quick Log Function (Even Faster)

```python
from agent_observability import log_event

log_event("api_call", {"provider": "openai", "cost_usd": 0.002})
```

## Installation

```bash
pip install agent-observability
```

## Usage

### Basic Logging

```python
from agent_observability import AgentLogger

# Auto-registers if no API key provided
logger = AgentLogger()

# Or use existing API key
logger = AgentLogger(api_key="ao_live_...")

# Log an API call
logger.log("api_call", {
    "provider": "openai",
    "model": "gpt-4",
    "cost_usd": 0.002,
    "latency_ms": 1200,
    "tokens_used": 1500,
})

# Log a decision
logger.log("decision", {
    "decision_reason": "Chose provider A due to cost optimization",
    "alternatives_considered": ["providerB", "providerC"],
})

# Log an error
logger.log("error", {
    "error_message": "Rate limit exceeded",
    "retry_count": 3,
}, severity="error")
```

### Context Manager (Automatic Timing)

```python
with logger.task("generate_image") as task:
    result = call_dalle_api()
    task.log_cost(0.02)
    task.log_metadata({"model": "dall-e-3"})
# Automatically logs timing and handles errors
```

### Batch Logging (Efficient)

```python
with logger.batch() as batch:
    for i in range(1000):
        batch.log("event", {
            "index": i,
            "cost_usd": 0.0001,
        })
# Sends all logs in a single request
```

### Async Mode

```python
# Fire-and-forget logging (non-blocking)
logger = AgentLogger(async_mode=True)
logger.log("api_call", {"latency_ms": 100})  # Returns immediately
```

## Features

- **Zero-Friction Setup**: Auto-registers on first log (v1.1.0+)
- **Automatic Retries**: Exponential backoff with 3 retries
- **Circuit Breaker**: Prevents cascade failures when API is down
- **Local Fallback**: Logs to `~/.agent_observability/fallback.jsonl` when offline
- **Batch Support**: Send up to 1000 logs per request
- **Async Mode**: Non-blocking logging for high-throughput agents

## Pricing

| Plan | Logs/Month | Price |
|------|------------|-------|
| **Free** | 1,000 | $0/month |
| **Starter** | 10,000 | $29/month |
| **Pro** | 100,000 | $99/month |

**Compare to competitors:**
- LangSmith: ~$39+ per 1K logs
- Datadog: ~$150+ per 1K logs

[View full pricing →](https://blueskylineassets.github.io/agent-observability/dashboard/pricing.html)

See [/pricing](https://api-production-0c55.up.railway.app/pricing) for programmatic access.

## Framework Integrations

| Package | Install |
|---------|---------|
| LangChain | `pip install agent-observability-langchain` |
| AutoGPT | `pip install agent-observability-autogpt` |
| CrewAI | `pip install agent-observability-crewai` |
| MCP (Claude) | `npm install -g agent-observability-mcp` |

## API Reference

### AgentLogger

```python
AgentLogger(
    api_key: str = None,             # API key (auto-registers if not provided)
    base_url: str = None,            # API base URL
    default_agent_id: str = None,    # Default agent ID for all logs
    timeout: float = 10.0,           # Request timeout
    max_retries: int = 3,            # Max retry attempts
    fallback_path: str = None,       # Local fallback file path
    async_mode: bool = False,        # Enable async logging
)
```

### log()

```python
logger.log(
    event_type: str,                 # Any string (e.g., api_call, decision, test, custom_event)
    metadata: dict = None,           # Event metadata
    agent_id: str = None,            # Agent identifier
    severity: str = "info",          # debug, info, warning, error, critical
    request_body: str = None,        # Request body (truncated to 10KB)
    response_body: str = None,       # Response body (truncated to 10KB)
    tags: list[str] = None,          # Tags for filtering
    context_id: UUID = None,         # For grouping related logs
    timestamp: datetime = None,      # Custom timestamp
)
```

### log_event()

```python
from agent_observability import log_event

# Quick one-liner - auto-registers if needed
log_event(
    event_type: str,                 # Event type
    metadata: dict = None,           # Event metadata
    **kwargs                         # Additional logger.log() arguments
)
```

## License

MIT License - See [LICENSE](LICENSE) for details.
