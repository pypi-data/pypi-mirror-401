"""File utility functions."""


from pathlib import PosixPath


def format_file_size(size_bytes: int) -> str:
    """Format file size in bytes to human-readable format.

    Args:
        size_bytes: Size in bytes

    Returns:
        Human-readable string (e.g., "1.5 MB", "500 KB")
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def count_files_in_directory(directory: PosixPath) -> int:
    """Count all files recursively in a directory.

    Args:
        directory: Path to the directory to count files in

    Returns:
        Number of files found in the directory (recursively)
    """
    count = 0
    try:
        for path in directory.rglob("*"):
            if path.is_file():
                count += 1
    except (PermissionError, OSError):
        # If we can't access some files, return what we counted so far
        pass
    return count
