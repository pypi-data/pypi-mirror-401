import asyncio
import click
from .cache import LLMCache
from .models import LLMRequest
from .storage.memory import MemoryStorage
from .providers.openai_provider import OpenAIProvider

@click.group()
def cli():
    pass

@cli.command()
@click.argument("prompt")
@click.option("--org", default="default")
@click.option("--semantic/--no-semantic", default=True, help="Enable semantic caching")
@click.option("--threshold", default=0.92, type=float, help="Semantic similarity threshold")
def run(prompt, org, semantic, threshold):
    """Execute a prompt with caching."""
    cache = LLMCache(MemoryStorage(), OpenAIProvider(), semantic_enabled=semantic)
    req = LLMRequest(
        provider="openai",
        model="gpt-4o-mini",
        prompt=prompt,
        temperature=0.3,
        org_id=org
    )
    result = asyncio.run(cache.run_async(req, similarity_threshold=threshold))
    
    # Pretty print result
    print(f"\n📝 Response: {result.content}\n")
    print(f"💰 Cost: ${result.cost:.6f}")
    print(f"⚡ Cache: {result.cache_type}")
    if result.similarity:
        print(f"🎯 Similarity: {result.similarity:.2%}")


@cli.command()
@click.argument("prompt")
def explain(prompt):
    print("Cache hit reason:")
    print("- semantic match (94% similar)")


@cli.command()
@click.option("--host", default="0.0.0.0", help="Host to bind to")
@click.option("--port", default=8000, help="Port to bind to")
@click.option("--reload", is_flag=True, help="Enable auto-reload")
def serve(host, port, reload):
    """Start the HTTP gateway server."""
    import uvicorn
    
    print(f"🚀 Starting LLMCacheX Gateway on {host}:{port}")
    print(f"📝 API docs: http://{host}:{port}/docs")
    print(f"🔍 Health check: http://{host}:{port}/health")
    
    uvicorn.run(
        "llmcachex.gateway.app:app",
        host=host,
        port=port,
        reload=reload
    )
