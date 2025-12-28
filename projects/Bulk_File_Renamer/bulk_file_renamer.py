#!/usr/bin/env python3
"""
Bulk File Renamer - Simple CLI tool to rename multiple files using a pattern
"""

import os
from pathlib import Path
from typing import List

def get_files_by_extension(folder: Path, extension: str) -> List[Path]:
    """Get all files with given extension in folder."""
    files = []
    for item in folder.iterdir():
        if item.is_file() and item.suffix.lower() == extension.lower():
            files.append(item)
    return sorted(files)  # Sort for consistent order

def generate_new_names(files: List[Path], base_name: str, start_index: int) -> List[str]:
    """Generate new file names with pattern: base_name_1.jpg, base_name_2.jpg, etc."""
    new_names = []
    for i, file_path in enumerate(files, start=start_index):
        new_names.append(f"{base_name}_{i}{file_path.suffix}")
    return new_names

def preview_rename(files: List[Path], new_names: List[str]) -> None:
    """Show preview of old -> new names."""
    print("\n" + "="*50)
    print("PREVIEW (what will be renamed):")
    print("="*50)
    for old, new in zip(files, new_names):
        print(f"  {old.name:25s} → {new}")
    print("="*50)

def perform_rename(files: List[Path], new_names: List[str]) -> bool:
    """Actually rename the files. Returns True if all succeeded."""
    success_count = 0
    for old_path, new_name in zip(files, new_names):
        new_path = old_path.parent / new_name
        try:
            if new_path.exists():
                print(f"  ⚠️  Skipping {new_name} (already exists)")
                continue
            old_path.rename(new_path)
            print(f"  ✅ {old_path.name} → {new_name}")
            success_count += 1
        except Exception as e:
            print(f"  ❌ Error renaming {old_path.name}: {e}")
    return success_count > 0

def main():
    print("🔄 Bulk File Renamer")
    print("-" * 30)
    
    # Get folder path
    folder_input = input("Enter folder path (or press Enter for current folder): ").strip()
    folder = Path(folder_input) if folder_input else Path(".")
    
    if not folder.exists():
        print("❌ Folder does not exist!")
        return
    
    if not folder.is_dir():
        print("❌ Path is not a folder!")
        return
    
    # Get extension
    extension = input("Enter file extension (e.g., '.jpg', '.png', '.txt'): ").strip()
    if not extension.startswith('.'):
        extension = '.' + extension
    
    # Find files
    files = get_files_by_extension(folder, extension)
    if not files:
        print(f"❌ No files found with extension '{extension}' in '{folder}'")
        return
    
    print(f"📁 Found {len(files)} files:")
    for f in files:
        print(f"  - {f.name}")
    
    # Get rename details
    base_name = input("\nEnter base name (e.g., 'photo', 'note'): ").strip()
    if not base_name:
        base_name = "file"
    
    try:
        start_index = int(input("Starting number (default 1): ").strip() or "1")
    except ValueError:
        start_index = 1
    
    # Generate and show preview
    new_names = generate_new_names(files, base_name, start_index)
    preview_rename(files, new_names)
    
    # Confirm
    confirm = input("\nProceed with rename? [y/N]: ").strip().lower()
    if confirm != 'y':
        print("❌ Cancelled.")
        return
    
    # Do the rename
    if perform_rename(files, new_names):
        print("\n🎉 Rename completed successfully!")
    else:
        print("\n❌ No files were renamed.")

if __name__ == "__main__":
    main()
