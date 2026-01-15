import os

from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)

from bclearer_interop_services.graph_services.backends import NetworkXGraphBackend
from bclearer_interop_services.graph_services.interfaces import GraphBackend


class BSimpleGraphs:
    def __init__(
        self,
        graph: object,
        name: str,
        *,
        backend: GraphBackend | None = None,
    ):
        self.graph = graph

        self.name = name
        self.backend: GraphBackend = backend or NetworkXGraphBackend()

    def __enter__(self):
        return self

    def __exit__(
        self,
        exception_type,
        exception_value,
        traceback,
    ):
        pass

    def export_to_graph_ml(
        self,
        output_folder: Folders,
    ) -> None:
        output_file_path = os.path.join(
            output_folder.absolute_path_string,
            self.name + ".graphml",
        )

        self.backend.export_to_graph_ml(
            graph=self.graph,
            output_file_path=output_file_path,
        )
