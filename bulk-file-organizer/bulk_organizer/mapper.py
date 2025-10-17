from pathlib import Path
from bulk_organizer.utils import normalize_extension


DEFAULT_MAP = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt"],
    "Archives": [".zip", ".tar", ".gz"],
    "Audio": [".mp3", ".wav"],
}

def map_extension_to_folder(file_path: Path, mapping: dict = DEFAULT_MAP) -> str:
    """Map a file extension to its corresponding folder name.

    Args:
        file_path (Path): The file path to map.
        mapping (dict): A dictionary mapping folder names to lists of extensions.

    Returns:
        str: The folder name corresponding to the file's extension, or "Others" if not found.
    """
    extension = normalize_extension(file_path.suffix)

    for folder , extensions in mapping.items():
        if extension in extensions:
            return folder
    return "Others"