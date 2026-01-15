# Middleware & Pipeline

AICCEL provides an extensible middleware pipeline for cross-cutting concerns.

---

## Overview

Middleware can:
- Log all requests/responses
- Validate inputs
- Rate limit API calls
- Cache responses
- Retry on failure
- Collect metrics

---

## Quick Start

```python
from aiccel import create_default_pipeline, MiddlewarePipeline

# Create default pipeline (logging + validation)
pipeline = create_default_pipeline(verbose=True)

# Or create custom
pipeline = MiddlewarePipeline()
pipeline.use(LoggingMiddleware())
pipeline.use(RateLimitMiddleware(requests_per_minute=30))
pipeline.use(RetryMiddleware(max_retries=3))
```

---

## Built-in Middleware

### LoggingMiddleware

Logs all requests and responses:

```python
from aiccel.pipeline import LoggingMiddleware

middleware = LoggingMiddleware(
    log_inputs=True,
    log_outputs=True,
    log_timing=True,
    max_content_length=500  # Truncate long content
)
```

### ValidationMiddleware

Validates inputs before processing:

```python
from aiccel.pipeline import ValidationMiddleware

middleware = ValidationMiddleware(
    required_fields=["query"],
    validators={
        "query": lambda q: len(q) > 0 and len(q) < 10000
    }
)
```

### RateLimitMiddleware

Prevents API overuse:

```python
from aiccel.pipeline import RateLimitMiddleware

middleware = RateLimitMiddleware(
    requests_per_minute=30,  # Max requests per minute
    requests_per_hour=500,   # Max per hour
    burst_limit=10           # Max burst requests
)

# Check remaining quota
remaining = middleware.get_remaining()
```

### RetryMiddleware

Automatic retry with backoff:

```python
from aiccel.pipeline import RetryMiddleware

middleware = RetryMiddleware(
    max_retries=3,
    initial_delay=1.0,       # First retry delay (seconds)
    backoff_factor=2.0,      # Exponential backoff
    retryable_errors=[       # Errors to retry on
        "rate_limit",
        "timeout",
        "server_error"
    ]
)
```

### CachingMiddleware

Cache responses:

```python
from aiccel.pipeline import CachingMiddleware

middleware = CachingMiddleware(
    ttl=3600,            # Cache for 1 hour
    max_size=1000,       # Max cached items
    cache_key_fn=None    # Custom key function
)

# Clear cache
middleware.clear()

# Get cache stats
stats = middleware.get_stats()
```

### MetricsMiddleware

Collect execution metrics:

```python
from aiccel.pipeline import MetricsMiddleware

middleware = MetricsMiddleware()

# After some usage
metrics = middleware.get_metrics()
print(metrics)
# {
#     "total_requests": 150,
#     "successful_requests": 145,
#     "failed_requests": 5,
#     "avg_latency_ms": 234.5,
#     "p95_latency_ms": 450.0,
#     "requests_per_minute": 12.3
# }

# Reset metrics
middleware.reset()
```

---

## Creating Custom Middleware

```python
from aiccel.pipeline import Middleware
from aiccel.core import Context

class CustomMiddleware(Middleware):
    """Custom middleware example."""
    
    def __init__(self, some_config: str = "default"):
        self.config = some_config
    
    async def __call__(self, context: Context, next_handler):
        """
        Process request.
        
        Args:
            context: Request context with query, metadata, etc.
            next_handler: Next middleware in chain
            
        Returns:
            Response from next handler
        """
        # Pre-processing
        print(f"Before: {context.query}")
        context.metadata["custom_field"] = "value"
        
        # Call next middleware
        response = await next_handler(context)
        
        # Post-processing
        print(f"After: {response}")
        
        return response
```

---

## Pipeline Usage

### Building a Pipeline

```python
from aiccel.pipeline import (
    MiddlewarePipeline,
    LoggingMiddleware,
    RateLimitMiddleware,
    CachingMiddleware,
    MetricsMiddleware
)

pipeline = MiddlewarePipeline()

# Add middleware (order matters!)
pipeline.use(LoggingMiddleware())          # 1. Log all requests
pipeline.use(RateLimitMiddleware(rpm=30))  # 2. Rate limit
pipeline.use(CachingMiddleware(ttl=3600))  # 3. Check cache
pipeline.use(MetricsMiddleware())          # 4. Collect metrics

# The final handler (agent execution) is added last
```

### Executing Through Pipeline

```python
from aiccel.core import Context

context = Context(
    query="What is AI?",
    metadata={"user_id": "123"}
)

# Execute through pipeline
async def agent_handler(ctx):
    return await agent.run_async(ctx.query)

response = await pipeline.execute(context, agent_handler)
```

### Default Pipeline

```python
from aiccel import create_default_pipeline

# Create with common middleware
pipeline = create_default_pipeline(
    verbose=True,        # Enable logging
    rate_limit=True,     # Enable rate limiting
    cache=True,          # Enable caching
    metrics=True         # Enable metrics
)

# Customize
pipeline.use(CustomMiddleware())
```

---

## Middleware Order

Order matters! Middleware executes in order added:

```
Request  →  Logging → RateLimit → Cache → Retry → Agent
Response ←  Logging ← RateLimit ← Cache ← Retry ←
```

Recommended order:
1. **Logging** - Log all requests first
2. **Metrics** - Track before anything can fail
3. **Rate Limiting** - Block excess requests early
4. **Caching** - Return cached before calling agent
5. **Retry** - Handle failures close to agent
6. **Validation** - Validate right before agent

---

## Complete Example

```python
from aiccel import SlimAgent, GeminiProvider
from aiccel.pipeline import (
    MiddlewarePipeline,
    LoggingMiddleware,
    RateLimitMiddleware,
    CachingMiddleware,
    RetryMiddleware,
    MetricsMiddleware
)
from aiccel.core import Context

# Setup agent
provider = GeminiProvider(api_key="...", model="gemini-2.5-flash")
agent = SlimAgent(provider=provider, name="PipelineAgent")

# Create pipeline
pipeline = MiddlewarePipeline()
pipeline.use(LoggingMiddleware(log_timing=True))
pipeline.use(MetricsMiddleware())
pipeline.use(RateLimitMiddleware(requests_per_minute=30))
pipeline.use(CachingMiddleware(ttl=1800))  # 30 min cache
pipeline.use(RetryMiddleware(max_retries=2))

# Agent handler
async def run_agent(context):
    return await agent.run_async(context.query)

# Use pipeline
async def ask(query: str) -> dict:
    context = Context(query=query)
    return await pipeline.execute(context, run_agent)

# Example usage
import asyncio

async def main():
    # These will go through the full pipeline
    result1 = await ask("What is AI?")
    result2 = await ask("What is AI?")  # Cached!
    
    # Get metrics
    metrics_mw = pipeline.get_middleware(MetricsMiddleware)
    print(metrics_mw.get_metrics())

asyncio.run(main())
```

---

## Best Practices

1. **Add logging first** - See all requests
2. **Rate limit early** - Protect APIs
3. **Cache strategically** - Not everything should be cached
4. **Set reasonable retries** - 2-3 is usually enough
5. **Monitor metrics** - Track performance over time

---

## Next Steps

- [Security](./security.md) - Encryption and privacy
- [Agents](./agents.md) - Agent configuration
