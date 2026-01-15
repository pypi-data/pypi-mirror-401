"""Read helpers for loading `.yxdb` data into common structures."""

from __future__ import annotations

import logging
from contextlib import contextmanager, suppress
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

import pandas
from yxdb.yxdb_reader import YxdbReader

from bclearer_interop_services.yxdb_service.configurations import YxdbReadConfiguration
from bclearer_interop_services.yxdb_service.schema_adapter import (
    YxdbSchemaAdapter,
)

LOGGER = logging.getLogger(__name__)

UniverseBuilder = Callable[[pandas.DataFrame], Any]


def get_yxdb_as_dataframe(
    configuration: YxdbReadConfiguration,
) -> pandas.DataFrame:
    """Return a :class:`pandas.DataFrame` populated from a `.yxdb` file."""

    reader = _YxdbStreamReader(configuration)
    return reader.read_dataframe()


def get_yxdb_as_pyspark(
    configuration: YxdbReadConfiguration,
    spark_session,
):
    """Return a PySpark DataFrame for the provided `.yxdb` file."""

    if spark_session is None:
        raise ValueError("spark_session must be provided")

    pandas_dataframe = get_yxdb_as_dataframe(configuration)

    if configuration.validation_only:
        return spark_session.createDataFrame(
            pandas_dataframe.head(0),
        )

    return spark_session.createDataFrame(pandas_dataframe)


def get_yxdb_as_universe(
    configuration: YxdbReadConfiguration,
    universe_builder: UniverseBuilder,
):
    """Convert the `.yxdb` content into a universe via the provided builder."""

    pandas_dataframe = get_yxdb_as_dataframe(configuration)
    return universe_builder(pandas_dataframe)


class _YxdbStreamReader:
    """Streams `.yxdb` rows into DataFrames while preserving metadata."""

    def __init__(
        self,
        configuration: YxdbReadConfiguration,
    ) -> None:
        self._configuration = configuration
        self._batch_size = max(1, configuration.batch_size)

    def read_dataframe(self) -> pandas.DataFrame:
        path = self._resolve_source_path()
        LOGGER.info("Reading yxdb file", extra={"path": str(path)})

        with _open_reader(path) as reader:
            metadata = self._read_metadata(reader)
            column_names = [field.name for field in reader.list_fields()]

            if self._configuration.validation_only:
                dataframe = pandas.DataFrame(columns=column_names)
            else:
                dataframe = self._stream_rows(reader, column_names)

        self._attach_metadata(dataframe, metadata, path)
        return dataframe

    def _resolve_source_path(self) -> Path:
        path = self._configuration.resolved_source_path()
        if not path.exists():
            raise FileNotFoundError(path)
        return path

    def _read_metadata(
        self,
        reader: YxdbReader,
    ) -> Sequence:
        if not self._configuration.include_metadata:
            return []

        raw_fields = getattr(reader, "_fields", None)
        if not raw_fields:
            return []

        return YxdbSchemaAdapter.from_meta_info(raw_fields)

    def _stream_rows(
        self,
        reader: YxdbReader,
        column_names: Sequence[str],
    ) -> pandas.DataFrame:
        frames: list[pandas.DataFrame] = []
        current_batch: list[dict[str, Any]] = []
        rows_read = 0

        while reader.next():
            row = {
                column_name: reader.read_index(index)
                for index, column_name in enumerate(column_names)
            }
            current_batch.append(row)
            rows_read += 1

            if len(current_batch) >= self._batch_size:
                frames.append(
                    pandas.DataFrame.from_records(
                        current_batch,
                        columns=column_names,
                    ),
                )
                LOGGER.debug(
                    "Read yxdb batch",
                    extra={"batch_rows": len(current_batch), "rows_read": rows_read},
                )
                current_batch.clear()

        if current_batch:
            frames.append(
                pandas.DataFrame.from_records(
                    current_batch,
                    columns=column_names,
                ),
            )

        if not frames:
            return pandas.DataFrame(columns=column_names)

        if len(frames) == 1:
            return frames[0].reset_index(drop=True)

        return pandas.concat(frames, ignore_index=True)

    def _attach_metadata(
        self,
        dataframe: pandas.DataFrame,
        metadata: Sequence,
        path: Path,
    ) -> None:
        dataframe.attrs["yxdb_source_path"] = str(path)
        dataframe.attrs["yxdb_record_count"] = len(dataframe.index)
        if metadata:
            dataframe.attrs["yxdb_field_definitions"] = metadata


@contextmanager
def _open_reader(path: Path) -> Iterable[YxdbReader]:
    reader = YxdbReader(path=str(path))
    try:
        yield reader
    finally:
        with suppress(Exception):
            reader.close()
