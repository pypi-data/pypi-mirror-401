# LLM Providers

AICCEL supports multiple LLM providers out of the box.

## Supported Providers

| Provider | Models | Streaming | Function Calling |
|----------|--------|-----------|------------------|
| **GeminiProvider** | gemini-2.5-flash, gemini-pro | ✅ | ✅ |
| **OpenAIProvider** | gpt-4o, gpt-4, gpt-3.5-turbo | ✅ | ✅ |
| **GroqProvider** | llama3-70b, mixtral | ✅ | ✅ |

---

## GeminiProvider

Google's Gemini models - fast and capable.

```python
from aiccel import GeminiProvider

provider = GeminiProvider(
    api_key="your-google-api-key",
    model="gemini-2.5-flash",  # or "gemini-pro"
    temperature=0.7,
    max_tokens=4096
)

# Simple generation
response = provider.generate("Explain quantum computing")

# Chat completion
messages = [
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hi there!"},
    {"role": "user", "content": "What's 2+2?"}
]
response = provider.chat(messages)
```

### Getting API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Use in your code

---

## OpenAIProvider

OpenAI's GPT models - most capable for complex tasks.

```python
from aiccel import OpenAIProvider

provider = OpenAIProvider(
    api_key="sk-your-openai-key",
    model="gpt-4o",  # or "gpt-4", "gpt-3.5-turbo"
    temperature=0.7,
    max_tokens=4096
)

response = provider.generate("Write a poem about AI")
```

### Getting API Key
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create new secret key
3. Add billing information

---

## GroqProvider

Groq's ultra-fast inference for Llama and Mixtral.

```python
from aiccel import GroqProvider

provider = GroqProvider(
    api_key="gsk-your-groq-key",
    model="llama3-70b-8192",  # or "mixtral-8x7b-32768"
    temperature=0.7
)

response = provider.generate("Explain machine learning")
```

### Getting API Key
1. Go to [Groq Console](https://console.groq.com/)
2. Create API key

---

## Common Parameters

All providers support these parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | str | required | API key for the provider |
| `model` | str | varies | Model name |
| `temperature` | float | 0.7 | Randomness (0.0-1.0) |
| `max_tokens` | int | 4096 | Maximum response tokens |
| `timeout` | float | 60.0 | Request timeout in seconds |

---

## Async Usage

All providers support async operations:

```python
# Async generate
response = await provider.generate_async("Question")

# Async chat
response = await provider.chat_async(messages)
```

---

## Fallback Providers

Use multiple providers for reliability:

```python
from aiccel import Agent, GeminiProvider, OpenAIProvider

primary = GeminiProvider(api_key="...", model="gemini-2.5-flash")
fallback = OpenAIProvider(api_key="...", model="gpt-4o")

agent = Agent(
    provider=primary,
    fallback_providers=[fallback],  # Used if primary fails
    name="ReliableAgent"
)
```

---

## Custom Provider

Create your own provider:

```python
from aiccel.providers import LLMProvider

class MyProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "my-model"):
        super().__init__(api_key=api_key, model=model)
    
    def generate(self, prompt: str, **kwargs) -> str:
        # Your implementation
        return "response"
    
    async def generate_async(self, prompt: str, **kwargs) -> str:
        # Async implementation
        return "response"
    
    def chat(self, messages: list, **kwargs) -> str:
        # Chat implementation
        return "response"
```

---

## Rate Limiting

Handle rate limits gracefully:

```python
from aiccel import create_default_pipeline, RateLimitMiddleware

# Add rate limiting middleware
pipeline = create_default_pipeline()
pipeline.use(RateLimitMiddleware(requests_per_minute=30))
```

---

## Best Practices

1. **Store keys securely** - Use environment variables
   ```python
   import os
   provider = GeminiProvider(api_key=os.environ["GOOGLE_API_KEY"])
   ```

2. **Use fallbacks** - For production reliability

3. **Choose the right model**:
   - **Gemini 2.5 Flash** - Fast, good for most tasks
   - **GPT-4o** - Best quality, complex reasoning
   - **Llama 3 70B (Groq)** - Fast, open source

4. **Monitor costs** - Set max_tokens appropriately

---

## Next Steps

- [Agents](./agents.md) - Create agents with providers
- [Tools](./tools.md) - Add tool capabilities
