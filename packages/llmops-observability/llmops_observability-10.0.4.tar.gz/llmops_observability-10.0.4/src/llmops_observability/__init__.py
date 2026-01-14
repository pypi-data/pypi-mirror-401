"""
LLMOps Observability SDK – Public API
Direct Langfuse integration for LLM tracing without SQS/batching.
Enhanced with veriskGO-style features: locals capture, nested spans, instant sending.
"""
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("llmops-observability")
except PackageNotFoundError:
    __version__ = "0.0.0"

# Core components
from .trace_manager import TraceManager, track_function
from .llm import track_llm_call
from .config import get_langfuse_client, configure
from .asgi_middleware import LLMOpsASGIMiddleware
from .models import TraceConfig, SpanContext

__all__ = [
    "TraceManager",
    "track_function",
    "track_llm_call",
    "get_langfuse_client",
    "configure",
    "LLMOpsASGIMiddleware",
    "TraceConfig",
    "SpanContext",
    "__version__",
]
