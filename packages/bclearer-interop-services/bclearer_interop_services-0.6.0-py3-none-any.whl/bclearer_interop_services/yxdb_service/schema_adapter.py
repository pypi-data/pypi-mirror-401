"""Helpers that translate `.yxdb` metadata to internal definitions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

try:
    from yxdb._metainfo_field import MetaInfoField  # type: ignore
except ImportError:  # pragma: no cover - runtime import guarded for tooling
    MetaInfoField = Any  # type: ignore

from bclearer_interop_services.yxdb_service.configurations import (
    YxdbFieldDefinition,
    YxdbFieldTypeEnum,
)
from bclearer_interop_services.yxdb_service.exceptions import (
    YxdbSchemaValidationError,
    YxdbUnsupportedTypeError,
)


@dataclass(slots=True)
class _ValidatedField:
    name: str
    data_type: YxdbFieldTypeEnum
    length: int
    scale: int
    metadata: Mapping[str, Any] | None


class YxdbSchemaAdapter:
    """Convert between `yxdb` library metadata and local dataclasses."""

    _YXDB_TO_ENUM: Mapping[str, YxdbFieldTypeEnum] = {
        "Bool": YxdbFieldTypeEnum.BOOL,
        "Byte": YxdbFieldTypeEnum.BYTE,
        "Int16": YxdbFieldTypeEnum.INT16,
        "Int32": YxdbFieldTypeEnum.INT32,
        "Int64": YxdbFieldTypeEnum.INT64,
        "Float": YxdbFieldTypeEnum.FLOAT,
        "Double": YxdbFieldTypeEnum.DOUBLE,
        "FixedDecimal": YxdbFieldTypeEnum.FIXED_DECIMAL,
        "String": YxdbFieldTypeEnum.STRING,
        "WString": YxdbFieldTypeEnum.WSTRING,
        "V_String": YxdbFieldTypeEnum.V_STRING,
        "V_WString": YxdbFieldTypeEnum.V_WSTRING,
        "Date": YxdbFieldTypeEnum.DATE,
        "Time": YxdbFieldTypeEnum.TIME,
        "DateTime": YxdbFieldTypeEnum.DATETIME,
        "Blob": YxdbFieldTypeEnum.BLOB,
        "SpatialObj": YxdbFieldTypeEnum.SPATIAL_OBJECT,
    }

    _ENUM_TO_YXDB: Mapping[YxdbFieldTypeEnum, str] = {
        enum_value: raw_name for raw_name, enum_value in _YXDB_TO_ENUM.items()
    }

    _LENGTH_REQUIRED = {
        YxdbFieldTypeEnum.STRING,
        YxdbFieldTypeEnum.WSTRING,
        YxdbFieldTypeEnum.FIXED_DECIMAL,
    }

    _SCALE_REQUIRED = {YxdbFieldTypeEnum.FIXED_DECIMAL}

    @classmethod
    def from_meta_info(
        cls,
        meta_fields: Sequence[MetaInfoField],
    ) -> list[YxdbFieldDefinition]:
        """Translate `yxdb` meta info into :class:`YxdbFieldDefinition`."""

        definitions: list[YxdbFieldDefinition] = []
        seen_names: set[str] = set()

        for field in meta_fields:
            name = (field.name or "").strip()
            if not name:
                raise YxdbSchemaValidationError("<unknown>", "field name missing")
            if name in seen_names:
                raise YxdbSchemaValidationError(name, "duplicate field name")
            seen_names.add(name)

            mapped_type = cls._YXDB_TO_ENUM.get(field.data_type)
            if mapped_type is None:
                raise YxdbUnsupportedTypeError(name, field.data_type)

            definition = YxdbFieldDefinition(
                name=name,
                field_type=mapped_type,
                length=cls._normalize_number(field.size),
                scale=cls._normalize_number(field.scale),
                metadata={
                    "source_data_type": field.data_type,
                    "raw_size": field.size,
                    "raw_scale": field.scale,
                },
            )
            definitions.append(definition)

        return definitions

    @classmethod
    def to_yxdb_metadata(
        cls,
        definitions: Sequence[YxdbFieldDefinition],
    ) -> list[dict[str, int | str]]:
        """Produce dictionaries ready for `.yxdb` writer metadata."""

        validated = cls._validate_definitions(definitions)
        metadata_rows: list[dict[str, int | str]] = []

        for item in validated:
            metadata_rows.append(
                {
                    "name": item.name,
                    "type": cls._ENUM_TO_YXDB[item.data_type],
                    "size": item.length,
                    "scale": item.scale,
                }
            )

        return metadata_rows

    @classmethod
    def _validate_definitions(
        cls,
        definitions: Sequence[YxdbFieldDefinition],
    ) -> list[_ValidatedField]:
        validated: list[_ValidatedField] = []
        seen_names: set[str] = set()

        for definition in definitions:
            name = (definition.name or "").strip()
            if not name:
                raise YxdbSchemaValidationError("<unknown>", "field name missing")
            if name in seen_names:
                raise YxdbSchemaValidationError(name, "duplicate field name")
            seen_names.add(name)

            raw_type = definition.field_type
            if raw_type not in cls._ENUM_TO_YXDB:
                raise YxdbUnsupportedTypeError(name, str(raw_type))

            length = cls._resolve_length(definition)
            scale = cls._resolve_scale(definition)

            validated.append(
                _ValidatedField(
                    name=name,
                    data_type=raw_type,
                    length=length,
                    scale=scale,
                    metadata=definition.metadata,
                )
            )

        return validated

    @classmethod
    def _resolve_length(cls, definition: YxdbFieldDefinition) -> int:
        length = definition.length
        if definition.field_type in cls._LENGTH_REQUIRED and not length:
            raise YxdbSchemaValidationError(
                definition.name,
                "length must be provided for this type",
            )
        if length is None:
            length = 0
        if length < 0:
            raise YxdbSchemaValidationError(
                definition.name,
                "length must be a positive integer",
            )
        return length

    @classmethod
    def _resolve_scale(cls, definition: YxdbFieldDefinition) -> int:
        scale = definition.scale
        if definition.field_type in cls._SCALE_REQUIRED and scale is None:
            raise YxdbSchemaValidationError(
                definition.name,
                "scale must be provided for this type",
            )
        if scale is None:
            scale = 0
        if scale < 0:
            raise YxdbSchemaValidationError(
                definition.name,
                "scale must be a positive integer",
            )
        return scale

    @staticmethod
    def _normalize_number(value: int | None) -> int | None:
        if value is None:
            return None
        return int(value)
