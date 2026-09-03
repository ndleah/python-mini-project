#!/usr/bin/env python3
import os
import sys

def custom_print(text: str, end: str = "\n"):
    """Fallback print logger removing rich markup when rich is missing."""
    clean_text = text.replace("[bold red]", "").replace("[/bold red]", "")
    clean_text = clean_text.replace("[bold green]", "").replace("[/bold green]", "")
    clean_text = clean_text.replace("[bold green][+]", "[+]").replace("[bold red][-]", "[-]")
    print(clean_text, end=end)

try:
    from rich import print as rich_print
except ImportError:
    rich_print = custom_print

def compare_files(original_path: str, changed_path: str) -> str:
    """Compare two text files line-by-line and display diff additions/deletions."""
    if not os.path.exists(original_path):
        print(f"Error: Original file '{original_path}' does not exist.")
        return ""
    if not os.path.exists(changed_path):
        print(f"Error: Changed file '{changed_path}' does not exist.")
        return ""

    with open(original_path, "r", encoding="utf-8", errors="replace") as f1:
        original_contents = f1.readlines()
    with open(changed_path, "r", encoding="utf-8", errors="replace") as f2:
        changed_contents = f2.readlines()

    if len(changed_contents) <= len(original_contents):
        color = "red"
        symbol = f"[bold {color}][-]"
        smallest_sloc, largest_sloc = changed_contents, original_contents
    else:
        color = "green"
        symbol = f"[bold {color}][+]"
        smallest_sloc, largest_sloc = original_contents, changed_contents

    output_lines = []

    for line in range(0, len(smallest_sloc)):
        if original_contents[line] == changed_contents[line]:
            continue
        else:
            rich_print(f"[bold red][-] Line {line + 1}:[/bold red] {original_contents[line]}", end="")
            rich_print(f"[bold green][+] Line {line + 1}:[/bold green] {changed_contents[line]}", end="")

            if line == len(smallest_sloc) - 1:
                for new_line in range(line + 1, len(largest_sloc)):
                    rich_print(f"{symbol} Line {new_line + 1}:[/bold {color}] {largest_sloc[new_line]}", end="")

def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("\tMust provide two file names as command-line arguments.")
        print("\tdiff.py <original_file> <changed_file>")
        sys.exit(1)

    original_file = sys.argv[1]
    changed_file = sys.argv[2]
    compare_files(original_file, changed_file)

if __name__ == '__main__':
    main()

