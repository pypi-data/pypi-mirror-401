from __future__ import annotations

from typing import Any, Mapping

from networkx import Graph, write_graphml

from ..interfaces import GraphBackend


class NetworkXGraphBackend(GraphBackend):
    """Graph backend backed by :mod:`networkx`."""

    name = "networkx"

    def create_graph(self) -> Graph:
        """Return a new networkx graph instance."""

        return Graph()

    def add_node(
        self,
        graph: Graph,
        identifier: str,
        attributes: Mapping[str, Any],
    ) -> None:
        """Add a node to the graph."""

        graph.add_node(identifier, **dict(attributes))

    def add_edge(
        self,
        graph: Graph,
        source: str,
        target: str,
        attributes: Mapping[str, Any],
    ) -> None:
        """Add an edge to the graph."""

        graph.add_edge(source, target, **dict(attributes))

    def export_to_graph_ml(self, graph: Graph, output_file_path: str) -> None:
        """Export the graph to GraphML using :func:`networkx.write_graphml`."""

        write_graphml(
            G=graph,
            path=output_file_path,
            encoding="utf-8",
            prettyprint=True,
        )
