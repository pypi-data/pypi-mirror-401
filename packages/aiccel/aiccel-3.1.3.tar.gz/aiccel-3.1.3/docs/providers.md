# 🧠 LLM Providers

AICCEL supports multiple LLM backends through a unified interface. Switch providers with a single line of code.

---

## 1. Google Gemini (`GeminiProvider`)

**Recommended for**: High speed, Large context, and Multimodal tasks.
**Environment Variable**: `GOOGLE_API_KEY`

```python
from aiccel.providers import GeminiProvider

# Default (Gemini 2.5 Flash)
provider = GeminiProvider(api_key="...")

# Specific Model
provider = GeminiProvider(model="gemini-1.5-pro")
```

---

## 2. Groq (`GroqProvider`)

**Recommended for**: Ultra-low latency inference using open-source models (LLaMA, Mixtral).
**Environment Variable**: `GROQ_API_KEY`

```python
from aiccel.providers import GroqProvider

# Uses LLaMA 3.1 70B by default
provider = GroqProvider(api_key="...")

# Optimized for speed
provider = GroqProvider(model="llama-3.1-8b-instant")
```

---

## 3. OpenAI (`OpenAIProvider`)

**Recommended for**: Industry-standard reasoning and reliability.
**Environment Variable**: `OPENAI_API_KEY`

```python
from aiccel.providers import OpenAIProvider

provider = OpenAIProvider(api_key="...")
```

---

## 4. Shared Configuration

All providers inherit from `LLMProvider` and support these parameters:

| Parameter | Default | Description |
| :--- | :--- | :--- |
| **`temperature`** | `0.0` | Controls randomness (0.0 is deterministic). |
| **`max_tokens`** | `4096` | Max tokens per generation. |
| **`timeout`** | `30.0` | HTTP request timeout in seconds. |
| **`api_key`** | `None` | Optional. If not provided, reads from environment. |

---

## 5. Fallback Strategy

AICCEL can automatically switch to a backup provider if the primary one fails.

```python
from aiccel import Agent

agent = Agent(
    provider=primary_gemini_provider,
    fallback_providers=[backup_groq_provider]
)
```

If the primary provider returns a 429 (Rate Limit) or 500 error, AICCEL will automatically retry using the fallback.
