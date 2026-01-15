"""Utilities for managing graph backend registrations."""

from __future__ import annotations

from collections.abc import Callable

from bclearer_interop_services.graph_services.interfaces import GraphBackend

BackendFactory = Callable[[], GraphBackend]

_BACKEND_FACTORIES: dict[str, BackendFactory] = {}


def register_graph_backend(
    name: str,
    factory: BackendFactory,
    *,
    override: bool = False,
) -> None:
    """Register a backend factory under the supplied name."""
    key = name.lower()
    if not override and key in _BACKEND_FACTORIES:
        raise ValueError(f"Graph backend '{name}' is already registered")
    _BACKEND_FACTORIES[key] = factory


def unregister_graph_backend(name: str) -> None:
    """Remove a previously registered backend."""
    _BACKEND_FACTORIES.pop(name.lower(), None)


def list_graph_backends() -> list[str]:
    """Return the list of registered backend names."""
    return sorted(_BACKEND_FACTORIES.keys())


def get_graph_backend(name: str | None = None) -> GraphBackend:
    """Return a backend instance for the requested name."""
    backend_name = (name or "networkx").lower()
    try:
        factory = _BACKEND_FACTORIES[backend_name]
    except KeyError as exc:  # pragma: no cover - defensive guard
        raise ValueError(f"Graph backend '{name}' is not registered") from exc
    backend = factory()
    if getattr(backend, "name", None) is None:  # pragma: no cover - sanity check
        backend.name = backend_name
    return backend

