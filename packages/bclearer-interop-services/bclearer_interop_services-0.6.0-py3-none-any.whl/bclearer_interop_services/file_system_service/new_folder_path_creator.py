"""Utility for creating folder paths including parent directories."""

from pathlib import Path


def create_new_folder_path(
    folder_path: Path,
) -> None:
    """Create a folder path including all parent directories if they don't exist.

    Args:
        folder_path: Path object representing the folder to create

    Raises:
        OSError: If folder creation fails due to permissions or other OS errors

    Example:
        >>> from pathlib import Path
        >>> create_new_folder_path(Path("/tmp/parent/child/grandchild"))
        >>> assert Path("/tmp/parent/child/grandchild").exists()

    Note:
        This function is idempotent - if the folder already exists, it does nothing.
        Uses exist_ok=True to avoid errors when folder exists.
    """
    if not folder_path.exists():
        folder_path.mkdir(
            parents=True,
            exist_ok=True,
        )
