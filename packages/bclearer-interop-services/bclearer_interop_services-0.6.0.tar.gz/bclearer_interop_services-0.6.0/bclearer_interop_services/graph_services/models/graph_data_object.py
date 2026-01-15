from __future__ import annotations

from collections.abc import Iterable, MutableMapping
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from bclearer_interop_services.graph_services.b_simple_graph_service.objects.b_simple_graphs import (
    BSimpleGraphs,
)
from bclearer_interop_services.graph_services.backends import get_graph_backend
from bclearer_interop_services.graph_services.interfaces import GraphBackend


class GraphNodeModel(BaseModel):
    """Representation of a graph node."""

    model_config = ConfigDict(populate_by_name=True)

    identifier: str = Field(alias="id")
    attributes: dict[str, Any] = Field(default_factory=dict)


class GraphEdgeModel(BaseModel):
    """Representation of a graph edge."""

    source: str
    target: str
    attributes: dict[str, Any] = Field(default_factory=dict)


class GraphDataObjectModel(BaseModel):
    """Payload representing a graph data object within a universe."""

    model_config = ConfigDict(populate_by_name=True)

    graph_name: str = Field(alias="graphName")
    nodes: list[GraphNodeModel] = Field(default_factory=list)
    edges: list[GraphEdgeModel] = Field(default_factory=list)
    backend_name: str | None = Field(
        default=None,
        alias="backend",
        description="Optional backend identifier used to materialise the graph.",
    )
    descriptor: dict[str, Any] = Field(default_factory=dict)

    def build_backend_graph(
        self,
        *,
        backend: GraphBackend | None = None,
    ) -> tuple[object, GraphBackend]:
        """Construct a backend-specific graph instance for the payload."""
        graph_backend = backend or get_graph_backend(self.backend_name)
        graph = graph_backend.create_graph()

        for node in self.nodes:
            graph_backend.add_node(graph, node.identifier, node.attributes)
        for edge in self.edges:
            graph_backend.add_edge(graph, edge.source, edge.target, edge.attributes)

        return graph, graph_backend

    def to_bsimple_graph(
        self,
        *,
        backend: GraphBackend | None = None,
    ) -> BSimpleGraphs:
        """Create a :class:`BSimpleGraphs` instance for the payload."""
        graph, graph_backend = self.build_backend_graph(backend=backend)
        return BSimpleGraphs(
            graph=graph,
            name=self.graph_name,
            backend=graph_backend,
        )

    def descriptor_payload(self) -> dict[str, Any]:
        """Return a serialisable descriptor for registration requests."""
        descriptor: MutableMapping[str, Any] = dict(self.descriptor)
        descriptor.setdefault("type", "graph")
        descriptor["graph_name"] = self.graph_name
        if self.backend_name:
            descriptor["backend"] = self.backend_name
        return dict(descriptor)

    def iter_nodes(self) -> Iterable[GraphNodeModel]:
        """Iterate over nodes in the payload."""
        return iter(self.nodes)

    def iter_edges(self) -> Iterable[GraphEdgeModel]:
        """Iterate over edges in the payload."""
        return iter(self.edges)
