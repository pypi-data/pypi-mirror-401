"""Configuration primitives for the yxdb interop services."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Mapping, Sequence


class YxdbFieldTypeEnum(str, Enum):
    """Enumeration of the supported `.yxdb` column data types."""

    BOOL = "Bool"
    BYTE = "Byte"
    INT16 = "Int16"
    INT32 = "Int32"
    INT64 = "Int64"
    FLOAT = "Float"
    DOUBLE = "Double"
    FIXED_DECIMAL = "FixedDecimal"
    DATE = "Date"
    TIME = "Time"
    DATETIME = "DateTime"
    STRING = "String"
    WSTRING = "WString"
    V_STRING = "V_String"
    V_WSTRING = "V_WString"
    BLOB = "Blob"
    SPATIAL_OBJECT = "SpatialObj"


@dataclass(slots=True)
class YxdbFieldDefinition:
    """Represents metadata describing a single `.yxdb` column."""

    name: str
    field_type: YxdbFieldTypeEnum
    length: int | None = None
    scale: int | None = None
    description: str | None = None
    nullable: bool = True
    metadata: Mapping[str, Any] | None = None


class YxdbOutputModeEnum(str, Enum):
    """Indicates which structure the read service should return."""

    PANDAS = "pandas"
    PYSPARK = "pyspark"
    UNIVERSE = "universe"
    METADATA_ONLY = "metadata"


@dataclass(slots=True)
class YxdbReadConfiguration:
    """Options required to stream a `.yxdb` file into memory."""

    source_path: str | Path
    batch_size: int = 100_000
    output_mode: YxdbOutputModeEnum = YxdbOutputModeEnum.PANDAS
    validation_only: bool = False
    include_metadata: bool = True
    spark_options: Mapping[str, Any] | None = None
    universe_options: Mapping[str, Any] | None = None

    def resolved_source_path(self) -> Path:
        """Return the source path as a :class:`pathlib.Path`."""

        return Path(self.source_path)


@dataclass(slots=True)
class YxdbWriteConfiguration:
    """Options describing how to serialize datasets into `.yxdb` files."""

    destination_path: str | Path
    schema: Sequence[YxdbFieldDefinition]
    buffer_rows: int = 50_000
    overwrite: bool = True
    create_snapshot: bool = False
    snapshot_name: str | None = None
    snapshot_metadata: Mapping[str, Any] | None = None
    validation_only: bool = False
    extra_metadata: Mapping[str, Any] | None = None

    def resolved_destination_path(self) -> Path:
        """Return the destination path as a :class:`pathlib.Path`."""

        return Path(self.destination_path)


__all__ = [
    "YxdbFieldDefinition",
    "YxdbFieldTypeEnum",
    "YxdbOutputModeEnum",
    "YxdbReadConfiguration",
    "YxdbWriteConfiguration",
]
