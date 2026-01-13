# LLMCacheX

> **Intelligent caching layer for LLM calls with semantic understanding, async deduplication, and cost control**

[![GitHub](https://img.shields.io/badge/github-prabhnoor12/llmcachex-blue?style=flat&logo=github)](https://github.com/prabhnoor12/llmcachex)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

---

## Why LLMCacheX?

LLM calls are **expensive**. A single GPT-4 call costs $0.03+. In production, you:

- Pay for identical requests multiple times
- Have no way to replay production issues locally
- Can't see exactly what you're being charged for
- Lose money on prompt variations ("Explain X" vs "What is X?")

**LLMCacheX solves all of this.**

```
Without LLMCacheX:  10 identical requests → $0.30
With LLMCacheX:     10 identical requests → $0.03 (1 cache hit)
Semantic bonus:     10 similar requests  → $0.03 (semantic match)
```

---

## What It Does

### 🎯 Exact Match Caching
Deterministic hashing prevents duplicate LLM calls. Identical prompts always hit cache.

### 🧠 Semantic Caching
"Explain Python" = "What is Python?" = "Tell me about Python" → **Same cached response**
- 10-30x increase in cache hit rates
- Handles typos, phrasing variations, multilingual
- Configurable similarity threshold (0.85-0.97)

### ⚡ Async Deduplication
10 concurrent identical requests:
- First hits LLM
- Others wait for result
- All get same response
- **You pay once, not 10x**

### 🔄 Replay & Time Travel
Replay production requests locally with zero API usage:
```python
# Record (production)
export LLMCACHEX_MODE=live

# Replay (local development)
export LLMCACHEX_MODE=replay
llmcachex run "same prompt"  # Returns cached response
```

### 🏢 Multi-Tenant Org Scoping
Complete cache isolation per organization:
```bash
curl -H "X-Org-ID: acme" http://localhost:8000/api/v1/cache
curl -H "X-Org-ID: techcorp" http://localhost:8000/api/v1/cache
# Different caches, zero cross-contamination
```

### 📊 Cost Control
See exactly what you're paying for:
```json
{
  "content": "Python is...",
  "cost": 0.0024,
  "cache_type": "semantic",
  "similarity": 0.94
}
```

---

## Quick Start

### Installation

```bash
# Basic (memory storage)
pip install llmcachex

# With gateway
pip install llmcachex[gateway]

# Full (with Redis, dev tools)
pip install llmcachex[all]
```

### Environment Setup

```bash
export OPENAI_API_KEY="sk-..."
export LLMCACHEX_SEMANTIC=true
export LLMCACHEX_SEMANTIC_THRESHOLD=0.92
```

### CLI Usage

```bash
# Simple request
llmcachex run "Explain quantum computing"

# With semantic tolerance
llmcachex run "What is quantum computing?" --threshold 0.90

# With org isolation
llmcachex run "Explain Python" --org acme_corp

# Disable semantic (exact only)
llmcachex run "Explain Python" --no-semantic
```

### HTTP Gateway (SaaS Mode)

```bash
# Start server
llmcachex serve --port 8000

# Make request
curl -X POST http://localhost:8000/api/v1/cache \
  -H "Content-Type: application/json" \
  -H "X-Org-ID: acme" \
  -d '{
    "prompt": "Explain machine learning",
    "model": "gpt-4o-mini",
    "temperature": 0.3
  }'
```

**Response:**
```json
{
  "content": "Machine learning is...",
  "cached": true,
  "cache_type": "semantic",
  "cost": 0.0,
  "similarity": 0.94,
  "org_id": "acme"
}
```

---

## Architecture

```
Request → Hash → Exact Match? ✓ Return
                    ↓ No
              Generate Embedding
                    ↓
              Semantic Match? ✓ Return
                    ↓ No
              Call LLM (with dedup lock)
                    ↓
              Store with Embedding
                    ↓
              Return + Cost
```

### Storage Backends

| Backend | Use Case | Latency | Cost |
|---------|----------|---------|------|
| **Memory** | Development, testing | <1ms | Free |
| **Redis** | Production, shared cache | 5-10ms | $$ |
| **Vector DB** | Large scale (100K+) | 50-100ms | $$$ |

### Providers

- **OpenAI** (default): GPT-4, GPT-3.5, embeddings API
- **Custom**: Implement provider interface

---

## Configuration

### Environment Variables

```bash
# Core
OPENAI_API_KEY=sk-...              # OpenAI API key (required)
LLMCACHEX_MODE=live|replay         # live or replay mode
LLMCACHEX_ORG=default              # Default org ID

# Storage
LLMCACHEX_STORAGE=memory|redis     # Storage backend
REDIS_URL=redis://localhost:6379/0 # Redis connection

# Semantic Caching
LLMCACHEX_SEMANTIC=true|false      # Enable semantic matching
LLMCACHEX_SEMANTIC_THRESHOLD=0.92  # Similarity threshold (0.0-1.0)
LLMCACHEX_EMBEDDING_MODEL=text-embedding-3-small  # Embedding model

# Security
LLMCACHEX_API_KEY=secret           # API key for gateway
```

---

## Python API

### Simple Usage

```python
from llmcachex import LLMCache
from llmcachex.storage.memory import MemoryStorage
from llmcachex.providers.openai_provider import OpenAIProvider
from llmcachex.models import LLMRequest
import asyncio

# Initialize
cache = LLMCache(MemoryStorage(), OpenAIProvider())

# Make request
req = LLMRequest(
    provider="openai",
    model="gpt-4o-mini",
    prompt="Explain Python",
    temperature=0.3,
    org_id="my_org"
)

result = asyncio.run(cache.run_async(req))

print(result.content)         # Response text
print(result.cache_type)      # "exact", "semantic", or "miss"
print(result.cost)            # Dollar cost
print(result.similarity)      # 0.94 for semantic hits
```

### With Redis

```python
from llmcachex.storage.redis import RedisStorage

cache = LLMCache(
    RedisStorage("redis://localhost:6379/0"),
    OpenAIProvider()
)
```

### Custom Threshold

```python
result = await cache.run_async(
    req,
    similarity_threshold=0.95  # More conservative
)
```

---

## Examples

### Example 1: Cost Savings

```python
# Monitor real savings
results = []
for i in range(10):
    result = await cache.run_async(request)
    results.append(result)

misses = sum(1 for r in results if r.cache_type == "miss")
total_cost = sum(r.cost for r in results)

print(f"Cache hits: {10 - misses}")
print(f"Total cost: ${total_cost:.6f}")
```

### Example 2: Replay Production

```bash
# Production (recording)
export LLMCACHEX_MODE=live
export REDIS_URL=redis://prod:6379/0

# Debug locally with zero cost
export LLMCACHEX_MODE=replay
llmcachex run "same prompt"
```

### Example 3: Multi-Tenant SaaS

```python
@app.post("/api/cache")
async def handle_cache(request: CacheRequest, org_id: str = Header()):
    llm_req = LLMRequest(
        prompt=request.prompt,
        org_id=org_id
    )
    return await cache.run_async(llm_req)
```

---

## Benchmarks

### Speed

```
Exact match:    < 1ms
Semantic match: 50-200ms
LLM call:       1000-5000ms

Win: 5-100x faster than LLM
```

### Cost

1000 requests with 30% natural duplication + 20% semantic boost:

```
Exact only:  700 calls = $7.00
With semantic: 500 calls + embeddings = $5.50

Savings: 21% (compounds to $550/month)
```

---

## Documentation

- **[GATEWAY.md](GATEWAY.md)** - HTTP API reference
- **[SEMANTIC.md](SEMANTIC.md)** - Semantic caching guide
- **[API Docs](http://localhost:8000/docs)** - Interactive Swagger UI

---

## Testing

```bash
pip install llmcachex[dev]
pytest tests/ -v
pytest tests/ --cov=llmcachex
mypy llmcachex/
ruff check llmcachex/
black llmcachex/
```

---

## Roadmap

- [x] Exact match caching
- [x] Semantic caching
- [x] Async deduplication
- [x] Org-scoped isolation
- [x] HTTP gateway
- [x] Redis backend
- [ ] Vector database support
- [ ] Advanced analytics
- [ ] Streaming responses
- [ ] Custom providers
- [ ] Rate limiting
- [ ] Usage billing

---

## Production Deployment

### Quick Start

```bash
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  prabhnoor12/llmcachex:latest
```

### With Docker Compose

```bash
docker-compose up -d  # Redis + LLMCacheX
```

---

## Contributing

1. Fork the repo
2. Create feature branch
3. Add tests
4. Format with `black` and `ruff`
5. Submit PR

---

## License

MIT License - see [LICENSE](LICENSE)

---

## Support

- **Issues**: [GitHub Issues](https://github.com/prabhnoor12/llmcachex/issues)
- **Docs**: [SEMANTIC.md](SEMANTIC.md) · [GATEWAY.md](GATEWAY.md)

---

**Made with ❤️ by [prabhnoor12](https://github.com/prabhnoor12)**
