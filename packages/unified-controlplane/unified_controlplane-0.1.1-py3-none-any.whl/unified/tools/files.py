"""File tools - File operation functions.

These tools allow agents to read and write files.
"""

from pathlib import Path


def read_file(path: str) -> str:
    """Read contents of a file.

    Args:
        path: Path to file

    Returns:
        File contents as string

    Raises:
        FileNotFoundError: If file doesn't exist
    """
    return Path(path).read_text()


def write_file(path: str, content: str) -> None:
    """Write content to a file.

    Args:
        path: Path to file
        content: Content to write

    Creates parent directories if needed.
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)


def list_files(path: str, pattern: str = "*") -> list[str]:
    """List files matching pattern.

    Args:
        path: Directory to search
        pattern: Glob pattern (default "*")

    Returns:
        List of file paths
    """
    return [str(p) for p in Path(path).glob(pattern)]
