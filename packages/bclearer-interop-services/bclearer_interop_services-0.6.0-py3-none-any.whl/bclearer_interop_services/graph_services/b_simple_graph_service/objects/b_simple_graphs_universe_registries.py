from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from bclearer_core.objects.registries.nf_universe_registries import (
    NfUniverseRegistries,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)


class BSimpleGraphsUniverseRegistries(
    NfUniverseRegistries
):
    def __init__(
        self,
        owning_b_simple_graphs_universe,
    ):
        super().__init__()
        # Maintain a flat mapping that uniquely identifies each stored graph.
        # The key combines the registry and register names with the graph name
        # so that different registers can safely persist graphs that share the
        # same name without collisions.
        self.b_simple_graphs_keyed_on_generator: dict[
            tuple[str, str, str], Any
        ] = {}
        self._graphs_by_register: dict[tuple[str, str], dict[str, Any]] = {}

        self.owning_b_simple_graphs_universe = owning_b_simple_graphs_universe

    def __enter__(self):
        return self

    def __exit__(
        self,
        exception_type,
        exception_value,
        traceback,
    ):
        pass

    def add_graph(
        self,
        *,
        registry_name: str,
        register_name: str,
        graph_name: str,
        graph_object: Any,
    ) -> None:
        """Store a graph instance for the given registry/register pair."""

        register_key = (registry_name, register_name)
        register_graphs = self._graphs_by_register.setdefault(register_key, {})
        register_graphs[graph_name] = graph_object
        unique_key = (registry_name, register_name, graph_name)
        self.b_simple_graphs_keyed_on_generator[unique_key] = graph_object

    def remove_graph(
        self,
        *,
        registry_name: str,
        register_name: str,
        graph_name: str,
    ) -> Any:
        """Remove a stored graph and return it."""

        register_key = (registry_name, register_name)
        register_graphs = self._graphs_by_register.get(register_key)
        if not register_graphs or graph_name not in register_graphs:
            raise KeyError(graph_name)

        graph_object = register_graphs.pop(graph_name)
        unique_key = (registry_name, register_name, graph_name)
        self.b_simple_graphs_keyed_on_generator.pop(unique_key, None)
        if not register_graphs:
            self._graphs_by_register.pop(register_key, None)
        return graph_object

    def list_graphs(
        self,
        *,
        registry_name: str,
        register_name: str,
    ) -> Mapping[str, Any]:
        """Return a mapping of graph names to graph objects."""

        register_key = (registry_name, register_name)
        graphs = self._graphs_by_register.get(register_key, {})
        return dict(graphs)

    def export_all_b_simple_graphs_to_graph_ml(
        self, output_folder: Folders
    ) -> None:
        for register_graphs in self._graphs_by_register.values():
            for b_simple_graph in register_graphs.values():
                b_simple_graph.export_to_graph_ml(
                    output_folder=output_folder
                )
