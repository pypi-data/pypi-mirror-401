from typing import Any

__all__ = ["Discovery"]


def __getattr__(name: str) -> Any:
    if name == "Discovery":
        # Lazy import keeps module load lightweight and avoids circular imports.
        from .discovery import Discovery

        return Discovery
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
