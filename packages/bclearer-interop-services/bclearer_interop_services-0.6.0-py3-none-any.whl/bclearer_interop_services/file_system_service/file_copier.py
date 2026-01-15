"""Utility for copying files using the file system service object model."""

import shutil

from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)


def copy_file(
    source_file: Files,
    target_file: Files,
) -> Files:
    """Copy a file from source to target location.

    Args:
        source_file: Source Files object to copy from
        target_file: Target Files object to copy to

    Returns:
        The target Files object after copying

    Raises:
        TypeError: If either parameter is not a Files instance
        FileNotFoundError: If source file doesn't exist
        PermissionError: If insufficient permissions to copy

    Example:
        >>> source = Files(absolute_path_string="/path/to/source.txt")
        >>> target = Files(absolute_path_string="/path/to/target.txt")
        >>> copied = copy_file(source, target)
        >>> assert copied.exists()
    """
    # Use class name checking to avoid circular import issues
    if (
        type(source_file).__name__
        != "Files"
        or type(target_file).__name__
        != "Files"
    ):
        raise TypeError(
            f"Expected Files objects, got {type(source_file).__name__} and {type(target_file).__name__}"
        )

    shutil.copyfile(
        source_file.absolute_path,
        target_file.absolute_path,
    )

    return target_file
