import tempfile
from pathlib import Path

from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)


def get_drive_temporary_folder() -> (
    Folders
):
    """Get the system temporary folder as a Folders object."""
    temporary_folder_path_string = (
        tempfile.gettempdir()
    )

    temporary_folder = Folders(
        absolute_path=Path(
            temporary_folder_path_string
        )
    )

    return temporary_folder
