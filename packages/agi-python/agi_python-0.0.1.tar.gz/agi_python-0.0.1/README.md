<div align="center">

<img src="https://cdn.prod.website-files.com/67be56277f6d514dcad939e2/67e48dd1cdab04c17a311669_logo-agi-white.png" alt="AGI" width="120"/>

<h1>AGI Python SDK</h1>

<p>
  <a href="https://www.theagi.company/">Website</a> •
  <a href="https://docs.agi.tech">Documentation</a> •
  <a href="https://platform.agi.tech">Platform</a> •
  <a href="https://theagi.company/blog">Blog</a>
</p>

---

**AI agent that actually works on the web.**

<br />

</div>

```python
from agi import AGIClient

client = AGIClient()

with client.session("agi-0") as session:
    result = session.run_task(
        "Find three nonstop flights from SFO to JFK next month under $450. "
        "Return flight times, airlines, and booking links."
    )
    print(result)
```

<br />

> Powered by [AGI.tech](https://agi.tech) - the world's most capable computer agent. Trusted by [Visa](https://www.theagi.company/blog/agi-inc-visa) for agentic commerce. Evaluated with [REAL Bench](https://www.theagi.company/blog/introducing-real-bench).

<br />

## Installation

```bash
pip install agi-python
```

Get your API key at [platform.agi.tech](https://platform.agi.tech/api-keys)

```bash
export AGI_API_KEY="your-api-key"
```

## Quick Start

### Simple Task

```python
from agi import AGIClient

client = AGIClient()

with client.session("agi-0") as session:
    result = session.run_task("Find the cheapest iPhone 15 on Amazon")
    print(result)
```

### Real-Time Event Streaming

```python
with client.session("agi-0") as session:
    session.send_message("Research the top 5 AI companies in 2025")

    for event in session.stream_events():
        if event.event == "thought":
            print(f"💭 Agent: {event.data}")
        elif event.event == "done":
            print(f"✅ Result: {event.data}")
            break
```

### Session Control

```python
with client.session("agi-0") as session:
    session.send_message("Long research task...")

    # Control execution
    session.pause()    # Pause the agent
    session.resume()   # Resume later
    session.cancel()   # Or cancel
```

---

## Core Concepts

*Understanding the building blocks of agi*

### Sessions: The Container for Tasks

Every task runs inside a **session** - an isolated browser environment:

```python
# Context manager (recommended) - automatic cleanup
with client.session("agi-0") as session:
    session.run_task("Find flights...")

# Manual management - full control
session = client.sessions.create(agent_name="agi-0")
client.sessions.send_message(session.session_id, "task")
client.sessions.delete(session.session_id)
```

▸ Use context managers for most tasks. Use manual management when you need fine-grained control.

### Available Agents

- **agi-0** - General purpose agent (recommended)
- **agi-0-fast** - Faster agent for simple tasks
- **agi-1** - Advanced agent with enhanced capabilities

See [docs.agi.tech](https://docs.agi.tech) for the full list.

---

## Features

- **Natural Language** - Describe tasks in plain English, no selectors or scraping code
- **Real-Time Streaming** - Watch agent execution live with Server-Sent Events
- **Session Control** - Pause, resume, or cancel long-running tasks
- **Browser Control** - Navigate and screenshot for visual debugging
- **Type-Safe** - Full type hints with Pydantic validation
- **Production-Ready** - Built-in retries, automatic cleanup, comprehensive error handling

---

## Common Use Cases

### Price Monitoring

Monitor product prices and availability across retailers.

```python
with client.session("agi-0") as session:
    result = session.run_task(
        "Go to amazon.com and search for 'Sony WH-1000XM5'. "
        "Get the current price, check if it's in stock, and return the product rating. "
        "Return as JSON with fields: price, in_stock, rating, url."
    )
```

### Lead Generation

Extract structured data from public sources.

```python
with client.session("agi-0") as session:
    result = session.run_task(
        "Go to ycombinator.com/companies, find companies in the 'AI' category "
        "from the latest batch. For the first 10 companies, get their name, "
        "description, and website. Return as a JSON array."
    )
```

### Flight Booking Research

```python
with client.session("agi-0") as session:
    result = session.run_task(
        "Find three nonstop SFO→JFK flights next month under $450. "
        "Compare prices on Google Flights, Kayak, and Expedia. "
        "Return flight details and booking links."
    )
```

<details>
<summary><b>Browser Control</b> – Navigate and take screenshots for visual debugging</summary>

<br />

```python
with client.session("agi-0") as session:
    # Navigate to specific URL
    session.navigate("https://amazon.com")

    # Get screenshot for debugging
    screenshot = session.screenshot()
    print(screenshot.url)    # Current page URL
    print(screenshot.title)  # Page title
    # screenshot.screenshot contains base64 JPEG data
```

</details>

<details>
<summary><b>Session Snapshots</b> – Preserve authentication and browser state</summary>

<br />

```python
# Create session and save environment
session1 = client.sessions.create(agent_name="agi-0")
# ... do some work ...
client.sessions.delete(session1.session_id, save_snapshot_mode="filesystem")

# Later, restore from saved environment
session2 = client.sessions.create(
    agent_name="agi-0",
    restore_from_environment_id=session1.environment_id
)
# Authentication state and cookies preserved!
```

</details>

<details>
<summary><b>Advanced Session Management</b> – Full control over session lifecycle</summary>

<br />

```python
# Create session manually
session = client.sessions.create(
    agent_name="agi-0-fast",
    webhook_url="https://yourapp.com/webhook",
    max_steps=200
)

# Send message
client.sessions.send_message(
    session.session_id,
    "Find flights from SFO to JFK under $450"
)

# Check status
status = client.sessions.get_status(session.session_id)
print(status.status)  # "running", "finished", etc.

# List all sessions
sessions = client.sessions.list()

# Delete when done
client.sessions.delete(session.session_id)
```

</details>

<details>
<summary><b>Webhooks</b> – Get notified when tasks complete</summary>

<br />

```python
session = client.sessions.create(
    agent_name="agi-0",
    webhook_url="https://yourapp.com/webhook"
)

# Your webhook will receive events:
# POST https://yourapp.com/webhook
# {
#   "event": "done",
#   "session_id": "sess_...",
#   "data": {...}
# }
```

</details>

---

## Error Handling

<details>
<summary><b>Robust error handling with detailed debugging</b></summary>

<br />

```python
from agi import (
    AGIClient,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    AgentExecutionError
)

client = AGIClient()

try:
    with client.session("agi-0") as session:
        result = session.run_task("Find flights...")
except AuthenticationError:
    print("Invalid API key")
except NotFoundError:
    print("Session not found")
except RateLimitError:
    print("Rate limit exceeded - please retry")
except AgentExecutionError as e:
    print(f"Task failed: {e}")
    # Debug at VNC URL if available
except AGIError as e:
    print(f"API error: {e}")
```

</details>

---

## Documentation & Resources

**Learn More**
- [API Reference](https://docs.agi.tech) – Complete API documentation
- [Code Examples](./examples) – Working examples for common tasks
- [GitHub Issues](https://github.com/agi-inc/agi-python/issues) – Report bugs or request features

**Get Help**
- [Platform](https://platform.agi.tech) – Manage API keys and monitor usage
- [Documentation](https://docs.agi.tech) – Guides and tutorials

---

## License

MIT License - see [LICENSE](LICENSE) for details.
