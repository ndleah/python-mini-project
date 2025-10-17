from pathlib import Path
from typing import Iterator

def scanner(directory: Path, recursive: bool = True) -> Iterator[Path]:
    """Scan the given directory and yield file paths.

    Args:
        directory (Path): The directory to scan.
        recursive (bool): Whether to scan subdirectories recursively.

    Yields:
        Iterator[Path]: An iterator of file paths.
    """

    if not directory.exists() or not directory.is_dir():
        raise ValueError(f"{directory} is not a valid directory")
    
    if recursive:
        yield from (p for p in directory.rglob("*") if p.is_file())
    else:
        yield from (p for p in directory.iterdir() if p.is_file())




