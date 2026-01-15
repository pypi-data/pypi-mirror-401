"""Graph backend implementations for interop services."""

from .networkx_backend import NetworkXGraphBackend
from .registry import (
    get_graph_backend,
    list_graph_backends,
    register_graph_backend,
    unregister_graph_backend,
)

# Ensure the default NetworkX backend is always available.
register_graph_backend(
    NetworkXGraphBackend.name,
    NetworkXGraphBackend,
    override=True,
)

__all__ = [
    "NetworkXGraphBackend",
    "get_graph_backend",
    "list_graph_backends",
    "register_graph_backend",
    "unregister_graph_backend",
]
