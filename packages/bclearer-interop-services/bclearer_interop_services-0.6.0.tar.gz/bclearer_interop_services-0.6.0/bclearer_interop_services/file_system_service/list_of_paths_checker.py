"""Utility for validating that a list of paths exist."""

from pathlib import Path

from bclearer_core.configurations.datastructure.logging_inspection_level_b_enums import (
    LoggingInspectionLevelBEnums,
)
from bclearer_orchestration_services.reporting_service.reporters.inspection_message_logger import (
    log_inspection_message,
)


def list_of_paths_exist(
    list_of_paths: list,
) -> bool:
    """Check if all paths in a list exist on the file system.

    Args:
        list_of_paths: List of path strings to validate

    Returns:
        True if all paths exist, False if any path doesn't exist

    Example:
        >>> paths = ["/tmp", "/usr"]
        >>> if list_of_paths_exist(paths):
        ...     print("All paths exist")

    Note:
        Logs an ERROR message for each path that doesn't exist.
    """
    all_paths_exist = True

    for path in list_of_paths:
        if not Path(path).exists():
            all_paths_exist = (
                __log_not_existing_path(
                    path=path
                )
            )

    if not all_paths_exist:
        return False

    return True


def __log_not_existing_path(
    path: str,
) -> bool:
    """Log an error message for a non-existent path.

    Args:
        path: The path that doesn't exist

    Returns:
        Always returns False to indicate path doesn't exist
    """
    log_inspection_message(
        message=f"Path does not exist: {path}",
        logging_inspection_level_b_enum=LoggingInspectionLevelBEnums.ERROR,
    )

    return False
