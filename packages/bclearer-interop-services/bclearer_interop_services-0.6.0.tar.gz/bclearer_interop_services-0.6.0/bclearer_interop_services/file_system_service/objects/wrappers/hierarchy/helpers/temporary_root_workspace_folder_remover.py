import shutil
from pathlib import Path

from bclearer_core.configurations.datastructure.logging_inspection_level_b_enums import (
    LoggingInspectionLevelBEnums,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_interop_services.file_system_service.zipped_files_services.constants.unzipper_process_constants import (
    PERMANENT_WORK_AREA_NAME_STRING,
    TEMPORARY_WORKSPACE_NAME_STRING,
)
from bclearer_orchestration_services.reporting_service.reporters.inspection_message_logger import (
    log_inspection_message,
)


def remove_temporary_root_workspace_folder(
    remove_temporary_root_folder: bool,
) -> None:
    temporary_root_folder_path = (
        Path.home()
        / PERMANENT_WORK_AREA_NAME_STRING
        / TEMPORARY_WORKSPACE_NAME_STRING
    )

    log_inspection_message(
        message="To deprecate - Removing temporary root folder {}".format(
            temporary_root_folder_path
        ),
        logging_inspection_level_b_enum=LoggingInspectionLevelBEnums.INFO,
    )

    temporary_root_folder_children = list(
        temporary_root_folder_path.glob(
            "**/*"
        )
    )

    if (
        len(
            temporary_root_folder_children
        )
        > 0
    ):
        temporary_root_folder = Folders(
            absolute_path=temporary_root_folder_path
        )

        if remove_temporary_root_folder:
            delete_folder(
                folder=temporary_root_folder
            )


def delete_folder(
    folder: Folders,
) -> None:
    try:
        shutil.rmtree(
            folder.absolute_path_string
        )

        folder.absolute_path.mkdir()

    except Exception as error:
        print(
            "Something went wrong trying to delete the folder: {0}".format(
                error
            )
        )
