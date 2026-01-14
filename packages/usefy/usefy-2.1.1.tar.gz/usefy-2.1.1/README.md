# Usefy Python SDK

Official Python SDK for [Usefy](https://usefy.ai) - AI Cost Control & Budget Management.

## Installation

```bash
pip install usefy
```

Or install from source:
```bash
pip install git+https://github.com/sherlocq61/usefy.git#subdirectory=sdk/python
```

## Quick Start

```python
from usefy import Usefy

# Initialize client
client = Usefy(api_key="us_live_your_key_here")

# Use like OpenAI - model auto-detection included
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response["choices"][0]["message"]["content"])
```

## Features

### OpenAI-Compatible Interface

```python
# GPT-4
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Explain quantum computing"}]
)

# Claude (auto-detected)
response = client.chat.completions.create(
    model="claude-3-opus",
    messages=[{"role": "user", "content": "Write a poem"}]
)

# Gemini
response = client.chat.completions.create(
    model="gemini-2.0-flash",
    provider="google",  # Explicit provider
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Fail-Open Mode

For maximum reliability, enable fail-open mode. If Usefy is temporarily unavailable, the SDK will signal that you should fall back to direct provider calls:

```python
client = Usefy(
    api_key="us_live_xxx",
    fail_open=True,
    fail_open_timeout=2.0  # 2 seconds
)

try:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello!"}]
    )
except UsefyTimeoutError:
    if client.is_fail_open_active:
        # Fall back to direct OpenAI call
        import openai
        response = openai.chat.completions.create(...)
```

### Pre-flight Check

Check if a request would be allowed before making it:

```python
check = client.check(
    provider="openai",
    model="gpt-4",
    estimated_tokens=1000
)

if check["allowed"]:
    # Proceed with request
    response = client.chat.completions.create(...)
else:
    print(f"Request would be blocked: {check['reason']}")
```

### Usage Monitoring

```python
usage = client.get_usage()

print(f"Requests: {usage['monthly_requests']['used']}/{usage['monthly_requests']['limit']}")
print(f"Plan: {usage['plan_name']}")
```

## Configuration

### Environment Variables

```bash
export USEFY_API_KEY="us_live_your_key"
```

Then:
```python
client = Usefy()  # API key from env
```

### Full Configuration

```python
from usefy import Usefy, UsefyConfig

config = UsefyConfig(
    api_key="us_live_xxx",
    base_url="https://api.usefy.ai",
    timeout=30.0,
    max_retries=3,
    retry_delay=1.0,
    fail_open=False,
    fail_open_timeout=2.0,
    log_level="WARNING"
)

client = Usefy(config=config)
```

## Supported Providers

| Provider | Models | Auto-Detection |
|----------|--------|----------------|
| OpenAI | gpt-5, gpt-5-mini, gpt-4.1, o3, o3-mini, o3-pro, o4-mini | ✅ |
| Anthropic | claude-opus-4.5, claude-sonnet-4.5, claude-haiku-4.5, claude-opus-4, claude-sonnet-4 | ✅ |
| Google | gemini-3-pro, gemini-3-flash, gemini-2.5-pro, gemini-2.5-flash, gemini-2.0-flash | ✅ |
| Mistral | mistral-large-2, mistral-medium, mistral-small, mixtral-8x22b | ✅ |
| Cohere | command-r-plus, command-r, command | ✅ |
| DeepSeek | deepseek-chat, deepseek-coder, deepseek-reasoner | ✅ |
| Groq | llama-3.3-70b, llama-3.1-70b, mixtral-8x7b | ✅ |
| Together | llama-3.3-70b, qwen-2.5-coder, various | Manual |
| xAI | grok-3, grok-2, grok-2-mini | ✅ |

## Error Handling

```python
from usefy import (
    Usefy,
    UsefyError,
    UsefyAuthError,
    UsefyBudgetExceeded,
    UsefyRateLimited
)

try:
    response = client.chat.completions.create(...)
except UsefyAuthError:
    print("Invalid API key")
except UsefyBudgetExceeded as e:
    print(f"Budget exceeded: {e.budget_info}")
except UsefyRateLimited as e:
    print(f"Rate limited, retry after {e.retry_after}s")
except UsefyError as e:
    print(f"Error: {e.message}")
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Support

- Documentation: https://usefy.ai/docs
- Email: support@usefy.ai
- Issues: https://github.com/sherlocq61/usefy/issues
