import argparse
import tomllib 
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.progress import track
from bulk_organizer.scanner import scanner
from bulk_organizer.mapper import map_extension_to_folder, DEFAULT_MAP
from bulk_organizer.organizer import organize_file

console = Console()

def get_version():
    toml_path = Path(__file__).resolve().parent.parent / "pyproject.toml"
    with open(toml_path, "rb") as f:
        pyproject = tomllib.load(f)
    return pyproject["project"]["version"]


def main():
    parser = argparse.ArgumentParser()

    organized = {}
    CATEGORIZED_FOLDERS = set(DEFAULT_MAP.keys()) | {"Others"}

    parser.add_argument("--version", action="version", version=f"bulk-organizer {get_version()}")
    parser.add_argument("directory", type=str, help="Path to the directory to organize")
    parser.add_argument("--dry-run", action="store_true", help="Simulate the organization without making changes")
    parser.add_argument("--recursive", action="store_true", default=True, help="Recursively scan subdirectories")
    parser.add_argument("--summary", action="store_true",default=True, help="Show compact summary instead of full paths")


    args = parser.parse_args()
    directory_path = Path(args.directory)
    console.rule(f"[bold cyan]Bulk Organizer v{get_version()}[/bold cyan]")
    console.print(f"Target Directory: [bold yellow]{directory_path}[/bold yellow]\n")


    if args.dry_run:
        console.print("[bold magenta]Dry Run Mode Enabled[/bold magenta] — no files will be moved.\n")

    # Scan and print file paths
    try:
        files = list(scanner(directory_path, recursive=args.recursive))
        first = True
        for file_path in track(files, description="✨ Organizing files..."):
            if first:
                console.print()
                console.print()
                first = False

            folder = map_extension_to_folder(file_path)

            # Skip already-organized files
            if file_path.parent.name in CATEGORIZED_FOLDERS:
                continue

            # Always track for summary
            organized.setdefault(folder, []).append(file_path)

            # Perform move or simulate
            organize_file(file_path, directory_path, folder, dry_run=args.dry_run)
        
        console.print()

        if args.summary:
            console.print("\n📊 [bold underline]Organization Summary[/bold underline]\n")
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("Folder", style="cyan")
            table.add_column("File Count", style="green")
            table.add_column("Example Files", style="yellow")

            for folder, files in organized.items():
                examples = ", ".join(f.name for f in files[:3])
                table.add_row(folder, str(len(files)), examples + (" ..." if len(files) > 3 else ""))

            console.print(table)

        console.rule("[bold green]Operation Complete[/bold green]")

    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    main()
