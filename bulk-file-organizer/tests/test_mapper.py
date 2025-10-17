import pytest
from pathlib import Path
from bulk_organizer.scanner import scanner
from bulk_organizer.mapper import map_extension_to_folder, DEFAULT_MAP
from bulk_organizer.organizer import organize_file

def test_scanner_non_recursive(tmp_path):
    # Setup: create files and folders
    (tmp_path / "file1.txt").write_text("hello")
    (tmp_path / "subdir").mkdir()
    (tmp_path / "subdir" / "file2.txt").write_text("world")

    # Act
    files = list(scanner(tmp_path, recursive=False))

    # Assert
    assert len(files) == 1
    assert files[0].name == "file1.txt"

def test_scanner_recursive(tmp_path):
    (tmp_path / "file1.txt").write_text("hello")
    (tmp_path / "subdir").mkdir()
    (tmp_path / "subdir" / "file2.txt").write_text("world")

    files = list(scanner(tmp_path, recursive=True))

    assert len(files) == 2
    assert sorted([f.name for f in files]) == ["file1.txt", "file2.txt"]


def test_known_extension():
    assert map_extension_to_folder(Path("photo.JPG"), DEFAULT_MAP) == "Images"
    assert map_extension_to_folder(Path("song.wav"), DEFAULT_MAP) == "Audio"

def test_unknown_extension():
    assert map_extension_to_folder(Path("weird.xyz"), DEFAULT_MAP) == "Others"


def test_organize_file_dry_run(tmp_path, capsys):
    file = tmp_path / "test.txt"
    file.write_text("hello")

    organize_file(file, tmp_path, "Documents", dry_run=True)

    # File should still exist in original location
    assert file.exists()

    # Check printed output
    captured = capsys.readouterr()
    assert "[Dry Run]" in captured.out