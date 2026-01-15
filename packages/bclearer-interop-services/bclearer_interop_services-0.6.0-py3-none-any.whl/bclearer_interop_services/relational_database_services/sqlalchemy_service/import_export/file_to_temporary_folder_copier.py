import shutil
from pathlib import Path

from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from bclearer_interop_services.file_system_service.utilities.drive_temporary_folder_getter import (
    get_drive_temporary_folder,
)


def copy_file_to_temporary_folder(
    file: Files,
) -> Files:
    # TODO refactor get_drive_temporary_csv_folder to get_temporary_folder
    # TODO move to Files class
    temporary_folder = (
        get_drive_temporary_folder()
    )

    # TODO replace following code with copy_file_to_new_folder?
    moved_file = Files(
        absolute_path_string=str(
            Path(
                temporary_folder.absolute_path_string
            )
            / file.base_name
        )
    )

    shutil.copy2(
        file.absolute_path_string,
        temporary_folder.absolute_path_string,
    )

    return moved_file
