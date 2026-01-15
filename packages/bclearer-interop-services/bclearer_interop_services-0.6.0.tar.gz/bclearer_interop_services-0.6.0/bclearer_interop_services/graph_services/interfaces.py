from __future__ import annotations

from typing import Any, Mapping, Protocol


class GraphBackend(Protocol):
    """Protocol describing a backend capable of storing and exporting graphs."""

    name: str

    def create_graph(self) -> object:
        """Return a new backend-specific graph instance."""

    def add_node(
        self,
        graph: object,
        identifier: str,
        attributes: Mapping[str, Any],
    ) -> None:
        """Add a node with attributes to the graph."""

    def add_edge(
        self,
        graph: object,
        source: str,
        target: str,
        attributes: Mapping[str, Any],
    ) -> None:
        """Add an edge with attributes to the graph."""

    def export_to_graph_ml(self, graph: object, output_file_path: str) -> None:
        """Persist the graph as GraphML at the requested path."""
