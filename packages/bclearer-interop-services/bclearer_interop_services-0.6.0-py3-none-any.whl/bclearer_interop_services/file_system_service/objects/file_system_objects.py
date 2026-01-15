import os
import shutil
from pathlib import Path

from bclearer_interop_services.file_system_service.objects.path_properties import (
    PathProperties,
)
from bclearer_interop_services.file_system_service.objects.wrappers.absolute_path_wrappers import (
    AbsolutePathWrappers,
)
from bclearer_orchestration_services.identification_services.uuid_service.uuid_helpers.uuid_factory import (
    create_new_uuid,
)


class FileSystemObjects:
    def __init__(
        self,
        absolute_path_string: str = None,
        absolute_path: Path = None,
        parent_folder: object = None,
    ):
        # NOTE: Type checking for parent_folder removed to avoid circular import issues
        # The parent_folder parameter is expected to be a Folders instance or None

        # Validate that at least one path parameter is provided
        if (
            absolute_path is None
            and absolute_path_string
            is None
        ):
            raise ValueError(
                "Either absolute_path or absolute_path_string must be provided"
            )

        # TODO: Needs to be replaced by a creation of a bie id??
        self.uuid = create_new_uuid()

        # Support both Path and str initialization
        if absolute_path:
            self.__path = (
                AbsolutePathWrappers(
                    absolute_path
                )
            )
        else:  # NOTE: If the path string is empty, it deals with it inside the PathWrappers class
            self.__path = (
                AbsolutePathWrappers(
                    absolute_path_string
                )
            )

        # Store parent_folder for backward compatibility
        # This allows both stored attribute (old behavior) and dynamic property (new behavior)
        self._stored_parent_folder = (
            parent_folder
        )

        # TODO: temporary location - to be agreed
        if self.__path.exists():
            self.file_system_object_properties = PathProperties(
                input_file_system_object_path=self.__path.absolute_path_string,
            )

    @property
    def parent_folder(self):
        """Property that returns stored parent or creates on-demand.

        This supports both old behavior (stored attribute) and new behavior (dynamic property).
        """
        if (
            self._stored_parent_folder
            is not None
        ):
            return (
                self._stored_parent_folder
            )

        from bclearer_interop_services.file_system_service.objects.folders import (
            Folders,
        )

        return Folders(
            absolute_path_string=self.__path.parent
        )

    @parent_folder.setter
    def parent_folder(self, value):
        """Setter for backward compatibility with code that sets parent_folder."""
        self._stored_parent_folder = (
            value
        )

    @property
    def base_name(self) -> str:
        return self.__path.base_name

    @property
    def file_stem_name(self) -> str:
        """Return the file name without extension."""
        return (
            self.__path.file_stem_name
        )

    @property
    def absolute_path_string(
        self,
    ) -> str:
        return (
            self.__path.absolute_path_string
        )

    @property
    def absolute_path(self) -> Path:
        """Return the absolute path as a Path object."""
        path = self.__path.path

        return path

    @property
    def absolute_level(self) -> int:
        return (
            self.__path.absolute_level
        )

    @property
    def parent_absolute_path_string(
        self,
    ) -> str:
        return str(self.__path.parent)

    @property
    def drive(self) -> str:
        """Return the drive component of the path."""
        return self.absolute_path.drive

    # TODO: should we move this method only to Folders? As Files shouldn't be able to do this
    # TODO: Rename to accurate functionality "get_child_path"
    def extend_path(
        self,
        path_extension: str,
    ) -> Path:
        return self.__path.extend_path(
            path_extension,
        )

    def exists(self) -> bool:
        return self.__path.exists()

    def list_of_components(self):
        return (
            self.__path.list_of_components()
        )

    def item_count(self) -> int:
        return self.__path.item_count()

    def remove_me_from_disk(
        self,
    ) -> None:
        """Remove this file system object from disk.

        For folders, removes the folder and all its contents.
        For files, removes just the file.
        Logs a message if the object doesn't exist.
        """
        if self.exists():
            # Use class name instead of isinstance to avoid circular import issues
            class_name = type(
                self
            ).__name__

            if class_name == "Folders":
                # TODO: Path.rmdir() only deletes the folder if empty. shutil.rmtree() deletes the folder and subfolders
                #  regardless it's empty or not - AGREE ONE OPTION
                # self.absolute_path.rmdir()
                shutil.rmtree(
                    path=self.absolute_path,
                    ignore_errors=False,
                )

            elif class_name == "Files":
                self.absolute_path.unlink()

            else:
                raise TypeError(
                    f"Unexpected file system object type: {class_name}"
                )

        else:
            from bclearer_core.configurations.datastructure.logging_inspection_level_b_enums import (
                LoggingInspectionLevelBEnums,
            )
            from bclearer_orchestration_services.reporting_service.reporters.inspection_message_logger import (
                log_inspection_message,
            )

            log_inspection_message(
                message=f"File system object does not exist on disk: {self.absolute_path}",
                logging_inspection_level_b_enum=LoggingInspectionLevelBEnums.INFO,
            )
