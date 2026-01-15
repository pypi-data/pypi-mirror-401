"""Utility for checking if file system paths exceed maximum length limits."""

from bclearer_core.configurations.datastructure.logging_inspection_level_b_enums import (
    LoggingInspectionLevelBEnums,
)
from bclearer_orchestration_services.reporting_service.reporters.inspection_message_logger import (
    log_inspection_message,
)


def check_is_file_system_object_path_too_long(
    input_file_system_object_path: str,
    max_length: int = 260,
) -> bool:
    """Check if a file system path exceeds the maximum length.

    Args:
        input_file_system_object_path: The path to check
        max_length: Maximum allowed path length (default: 260 for Windows compatibility)

    Returns:
        True if path is too long, False otherwise

    Example:
        >>> path = "/very/long/path/..." * 50
        >>> if check_is_file_system_object_path_too_long(path):
        ...     print("Path exceeds maximum length")

    Note:
        - Default max_length of 260 is based on Windows MAX_PATH limitation
        - Logs a WARNING message if path is too long
        - This is particularly important for cross-platform compatibility
    """
    if (
        len(
            input_file_system_object_path
        )
        >= max_length
    ):
        log_inspection_message(
            message=f"File path is longer than {max_length}: {input_file_system_object_path}",
            logging_inspection_level_b_enum=LoggingInspectionLevelBEnums.WARNING,
        )

        return True

    else:
        return False
