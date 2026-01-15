import shutil
from pathlib import Path

from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)


# TODO move to Files class
def move_temporary_file_to_destination_folder(
    temporary_file: Files,
    destination_folder: Folders,
) -> None:
    shutil.copy2(
        temporary_file.absolute_path_string,
        destination_folder.absolute_path_string,
    )

    # TODO move to Files class
    temporary_file_path = Path(
        temporary_file.absolute_path_string
    )

    temporary_file_path.unlink()
