import shutil
from pathlib import Path
from rich.console import Console

console = Console()

def organize_file(file_path: Path, base_dir: Path, folder_name: str, dry_run: bool = False):
    """Move a file into its categorized folder, handling collisions and dry-run mode.

    Args:
        file_path (Path): The original file path.
        base_dir (Path): The base directory where folders are created.
        folder_name (str): The target folder name.
        dry_run (bool): If True, simulate the move without performing it.
    """ 
    target_dir = base_dir / folder_name
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / file_path.name

    # handle name collisions
    counter = 1
    while target_path.exists():
        target_path = target_dir / f"{file_path.stem} {counter}{file_path.suffix}"
        counter += 1

    if dry_run:
        console.print(
            f"[dim yellow][Dry Run][/dim yellow] {file_path.relative_to(base_dir)} → "
            f"[bold cyan]{target_path.relative_to(base_dir)}[/bold cyan]"
        )
    else:
        shutil.move(str(file_path), str(target_path))
        console.print(
            f"[green]✔ Moved[/green] [bold white]{file_path.relative_to(base_dir)}[/bold white] → "
            f"[bold cyan]{target_path.relative_to(base_dir)}[/bold cyan]"
        )
    

