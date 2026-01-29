# Joule SDK for Python

Track AI API usage with automatic monitoring of costs, tokens, and performance. Works with OpenAI and Anthropic SDKs.

## Installation

```bash
pip install joule-sdk

# With OpenAI support
pip install joule-sdk[openai]

# With Anthropic support
pip install joule-sdk[anthropic]

# With both
pip install joule-sdk[all]
```

## Quick Start

### OpenAI

```python
from openai import OpenAI
from joule_sdk import JouleOpenAI

# Create your OpenAI client as usual
client = OpenAI(api_key="sk-...")

# Wrap it with Joule
joule = JouleOpenAI(
    client,
    api_key="your-joule-api-key",
    user_id="user-123",           # optional
    environment="production"       # optional
)

# Use it exactly like the regular OpenAI client
response = joule.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)

# Usage is automatically tracked to Joule
```

### Anthropic

```python
from anthropic import Anthropic
from joule_sdk import JouleAnthropic

# Create your Anthropic client as usual
client = Anthropic(api_key="sk-ant-...")

# Wrap it with Joule
joule = JouleAnthropic(
    client,
    api_key="your-joule-api-key",
    user_id="user-123",
    environment="production"
)

# Use it exactly like the regular Anthropic client
response = joule.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)

# Usage is automatically tracked to Joule
```

### Streaming (Anthropic)

```python
with joule.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

# Usage is tracked when stream completes
```

## What Gets Tracked

The SDK automatically tracks:

- **Tokens**: Input, output, and total tokens
- **Cost**: Calculated from current pricing
- **Performance**: Response time in milliseconds
- **Errors**: Error types and messages
- **Context**: User ID, team ID, environment

**Privacy**: Only metadata is tracked. Your prompts and responses are never sent to Joule.

## Configuration

```python
joule = JouleOpenAI(
    client,
    api_key="your-joule-api-key",      # Required
    base_url="https://api.joule.ai",   # Optional, defaults to production
    user_id="user-123",                 # Optional, default user ID
    team_id="team-456",                 # Optional, default team ID
    application_id="my-app",            # Optional, application identifier
    environment="production",           # Optional, deployment environment
    debug=False                         # Optional, enable debug logging
)
```

## Per-Request Context

Override defaults for specific requests:

```python
response = joule.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}],
    joule_user_id="specific-user",      # Override user ID
    joule_team_id="specific-team",      # Override team ID
    joule_metadata={"feature": "chat"}  # Add custom metadata
)
```

## Context Manager

Use as a context manager to ensure events are flushed:

```python
with JouleOpenAI(client, api_key="...") as joule:
    response = joule.chat.completions.create(...)
# Events are flushed when exiting the context
```

## License

MIT
