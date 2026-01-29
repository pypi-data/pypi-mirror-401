# fika-langwatch

LangChain wrapper with automatic fallback and alert notifications when API keys fail.

**Copyright (c) 2026 FIKA Private Limited. All Rights Reserved.**

## Features

- **Automatic Fallback**: When a model fails, automatically try the next one
- **Alert Notifications**: Get notified via Email, Slack, or Webhooks when keys fail
- **Rate Limiting**: Built-in cooldown to prevent alert spam
- **Tool Binding**: Call `.bind_tools()` once, applies to ALL underlying models
- **Sync & Async**: Supports both `.invoke()` and `.ainvoke()`

## Installation

```bash
pip install fika-langwatch

# With optional dependencies
pip install fika-langwatch[email]      # Email alerts
pip install fika-langwatch[slack]      # Slack alerts
pip install fika-langwatch[webhook]    # Webhook alerts
pip install fika-langwatch[all]        # All alert channels

# Provider-specific
pip install fika-langwatch[google]     # Google Gemini
pip install fika-langwatch[openai]     # OpenAI
pip install fika-langwatch[anthropic]  # Anthropic Claude
pip install fika-langwatch[providers]  # All providers
```

## Quick Start

### Option 1: Config-based (Recommended)

```python
from langwatch import ChatWithFallback
from langwatch.alerts import EmailAlert, SlackAlert
from langchain_core.messages import HumanMessage

# Create with config - models are created automatically
chat = ChatWithFallback.from_config(
    models=[
        {
            "name": "gemini-1",
            "provider": "google",
            "model": "gemini-2.5-flash",
            "api_key": "AIza...",
        },
        {
            "name": "gemini-2",
            "provider": "google",
            "model": "gemini-2.5-flash",
            "api_key": "AIza...",
        },
        {
            "name": "fallback",
            "provider": "openrouter",
            "model": "x-ai/grok-4.1-fast",
            "api_key": "sk-...",
            "is_fallback": True,
        },
    ],
    alerts=[
        EmailAlert(
            smtp_server="smtp.gmail.com",
            smtp_port=587,
            username="alerts@company.com",
            password="app-password",
            to=["ops@company.com"],
        ),
        SlackAlert(webhook_url="https://hooks.slack.com/services/..."),
    ],
    cooldown_seconds=3600,  # 1 alert per hour
)

# Bind tools - applies to ALL models
chat_with_tools = chat.bind_tools([your_tool_1, your_tool_2])

# Use like any LangChain model
response = await chat_with_tools.ainvoke([HumanMessage(content="Hello!")])
```

### Option 2: Manual Models (Full Flexibility)

```python
from langwatch import ChatWithFallback
from langwatch.alerts import EmailAlert
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

# Create your own models
models = [
    ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key="..."),
    ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key="..."),
    ChatOpenAI(model="grok-4.1", base_url="https://openrouter.ai/api/v1", api_key="..."),
]

chat = ChatWithFallback(
    models=models,
    model_names=["gemini-1", "gemini-2", "fallback"],
    alerts=[EmailAlert(...)],
)

# Bind tools and use
chat_with_tools = chat.bind_tools(tools)
response = await chat_with_tools.ainvoke(messages)
```

## Supported Providers

When using `from_config()`, these providers are auto-created:

| Provider | Value | LangChain Class |
|----------|-------|-----------------|
| Google Gemini | `"google"` | `ChatGoogleGenerativeAI` |
| OpenAI | `"openai"` | `ChatOpenAI` |
| Anthropic Claude | `"anthropic"` | `ChatAnthropic` |
| OpenRouter | `"openrouter"` | `ChatOpenAI` with OpenRouter base_url |

For other providers, create the model manually and pass it directly.

## Alert Channels

### Email

```python
from langwatch.alerts import EmailAlert

alert = EmailAlert(
    smtp_server="smtp.gmail.com",
    smtp_port=587,
    username="alerts@company.com",
    password="your-app-password",  # Use Gmail App Password
    to=["ops@company.com"],
    cc=["team@company.com"],       # Optional
    from_name="LangWatch Alerts",  # Optional
)
```

### Slack

```python
from langwatch.alerts import SlackAlert

alert = SlackAlert(
    webhook_url="https://hooks.slack.com/services/T.../B.../xxx",
    channel="#alerts",              # Optional override
    username="LangWatch Bot",       # Optional
)
```

### Webhook

```python
from langwatch.alerts import WebhookAlert

alert = WebhookAlert(
    url="https://your-api.com/alerts",
    headers={"Authorization": "Bearer token"},
    method="POST",
)
```

## Callbacks

```python
def on_key_failure(key_name: str, error: str):
    print(f"Key {key_name} failed: {error}")

def on_fallback_activated(fallback_key: str):
    print(f"Now using fallback: {fallback_key}")

chat = ChatWithFallback.from_config(
    models=[...],
    alerts=[...],
    on_key_failure=on_key_failure,
    on_fallback_activated=on_fallback_activated,
)
```

## Check Status

```python
# Get status of all models
status = chat.get_status()
print(status)
# {
#     "total_keys": 3,
#     "healthy_keys": 2,
#     "failed_keys": 1,
#     "all_primary_failed": False,
#     "keys": [...]
# }
```

## How It Works

1. **Request comes in** → Try first model
2. **Model fails** → Mark as unhealthy, try next model
3. **All primary models fail** → Activate fallback, send alerts
4. **Alerts are rate-limited** → Only 1 alert per hour (configurable)
5. **Model recovers** → Automatically marked as healthy on next success

## License

Copyright (c) 2026 FIKA Private Limited. All Rights Reserved.

This is proprietary software. Unauthorized copying, modification, or distribution is prohibited.

For licensing inquiries, contact: rahul@pupiltree.ai
