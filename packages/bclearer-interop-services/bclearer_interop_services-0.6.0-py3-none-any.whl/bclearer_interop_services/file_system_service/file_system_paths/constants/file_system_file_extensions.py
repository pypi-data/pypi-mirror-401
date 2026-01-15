from enum import auto

from bclearer_core.configurations.datastructure.b_enums import (
    BEnums,
)
from bclearer_interop_services.file_system_service.file_system_paths.constants.file_extension_constants import (
    FILE_EXTENSION_DELIMITER,
)


class FileSystemFileExtensions(BEnums):
    NOT_SET = auto()

    ACCDB = auto()

    CSV = auto()

    DB = auto()

    MDB = auto()

    XLSX = auto()

    XLSM = auto()

    XLS = auto()

    TXT = auto()

    LOG = auto()

    JSON = auto()

    PY = auto()

    PNG = auto()

    JPG = auto()

    ZIP = auto()

    # TODO: to rename this property to: delimited_file_extension
    @property
    def delimited_file_extension(
        self,
    ) -> str:
        delimited_file_extension = (
            FILE_EXTENSION_DELIMITER
            + self.b_enum_item_name
        )

        return delimited_file_extension
