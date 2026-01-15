"""Custom exceptions raised by the yxdb interop services."""

from __future__ import annotations


class YxdbSchemaError(ValueError):
    """Base class for schema related failures."""


class YxdbSchemaValidationError(YxdbSchemaError):
    """Raised when a schema definition violates validation rules."""

    def __init__(self, field_name: str, message: str):
        self.field_name = field_name
        self.detail = message
        super().__init__(f"{field_name}: {message}")


class YxdbUnsupportedTypeError(YxdbSchemaValidationError):
    """Raised when a `.yxdb` column uses an unsupported type."""

    def __init__(self, field_name: str, raw_type: str):
        super().__init__(
            field_name=field_name,
            message=f"unsupported type '{raw_type}'",
        )
        self.raw_type = raw_type
