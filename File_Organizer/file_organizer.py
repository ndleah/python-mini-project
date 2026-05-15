import os
import shutil
import argparse
from pathlib import Path
from collections import defaultdict

FILE_CATEGORIES = {
    "Images":     {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico", ".tiff"},
    "Videos":     {".mp4", ".mkv", ".mov", ".avi", ".wmv", ".flv", ".webm", ".m4v"},
    "Audio":      {".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a"},
    "Documents":  {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".odt", ".csv"},
    "Archives":   {".zip", ".tar", ".gz", ".rar", ".7z", ".bz2", ".xz"},
    "Code":       {".py", ".js", ".ts", ".html", ".css", ".java", ".c", ".cpp", ".go", ".rb", ".rs", ".sh"},
    "Data":       {".json", ".xml", ".yaml", ".yml", ".sql", ".db", ".sqlite"},
    "Executables":{".exe", ".msi", ".dmg", ".deb", ".rpm", ".apk"},
    "Fonts":      {".ttf", ".otf", ".woff", ".woff2"},
}


def get_category(extension: str) -> str:
    ext = extension.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return "Misc"


def organize(directory: str, dry_run: bool = False) -> None:
    target = Path(directory).resolve()

    if not target.is_dir():
        print(f"Error: '{target}' is not a valid directory.")
        return

    files = [f for f in target.iterdir() if f.is_file()]

    if not files:
        print("No files found to organize.")
        return

    moved = defaultdict(list)
    skipped = []

    for file in files:
        category = get_category(file.suffix)
        dest_folder = target / category

        if not dry_run:
            dest_folder.mkdir(exist_ok=True)

        dest_path = dest_folder / file.name

        # avoid overwriting an existing file
        if dest_path.exists():
            skipped.append(file.name)
            continue

        if dry_run:
            moved[category].append(file.name)
        else:
            shutil.move(str(file), str(dest_path))
            moved[category].append(file.name)

    label = "[DRY RUN] Would move" if dry_run else "Moved"
    total = sum(len(v) for v in moved.values())

    print(f"\n{'=' * 45}")
    print(f"  Directory : {target}")
    print(f"  {label}  : {total} file(s)")
    print(f"{'=' * 45}")

    for category, names in sorted(moved.items()):
        print(f"\n  {category}/ ({len(names)} file(s))")
        for name in sorted(names):
            print(f"    - {name}")

    if skipped:
        print(f"\n  Skipped (already exist in destination): {len(skipped)}")
        for name in skipped:
            print(f"    - {name}")

    print()


def main():
    parser = argparse.ArgumentParser(
        description="Organize files in a directory into categorized subfolders."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Path to the directory to organize (default: current directory)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without moving any files",
    )
    args = parser.parse_args()
    organize(args.directory, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
