"""Facade for interacting with the yxdb read services."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from bclearer_interop_services.yxdb_service.configurations import (
    YxdbReadConfiguration,
)
from bclearer_interop_services.yxdb_service.read_service import (
    get_yxdb_as_dataframe,
    get_yxdb_as_pyspark,
    get_yxdb_as_universe,
)

UniverseBuilder = Callable[[Any], Any]


@dataclass(slots=True)
class YxdbServiceFacade:
    """High-level entry point for loading `.yxdb` datasets.

    Example
    -------
    ```python
    from bclearer_interop_services.yxdb_service import (
        YxdbReadConfiguration,
        YxdbServiceFacade,
    )

    facade = YxdbServiceFacade(
        YxdbReadConfiguration(source_path="/path/to/file.yxdb"),
    )

    dataframe = facade.get_dataframe()
    ```
    """

    configuration: YxdbReadConfiguration

    def get_dataframe(self):
        """Return the `.yxdb` content as a pandas DataFrame."""

        return get_yxdb_as_dataframe(self.configuration)

    def get_pyspark_dataframe(self, spark_session):
        """Return a PySpark DataFrame for the configured `.yxdb` file."""

        return get_yxdb_as_pyspark(self.configuration, spark_session)

    def get_universe(self, universe_builder: UniverseBuilder):
        """Project the `.yxdb` content into a BORO universe."""

        return get_yxdb_as_universe(self.configuration, universe_builder)

    def write_dataframe(self, *_args, **_kwargs):  # pragma: no cover - explicit limitation
        """Writing `.yxdb` files is not supported (read-only dependency)."""

        raise NotImplementedError(
            "yxdb writing is not supported; export CSV/Parquet and use Alteryx tooling"
        )
