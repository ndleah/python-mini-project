#!/usr/bin/env python3
import argparse
from pathlib import Path
from sys import stderr, stdout
import os

class CatError(Exception):
    pass

class Logger:
    def __init__(self, verbosity=False):
        self.verbose = verbosity

    def error(self, message):
        print(f'ERROR: {message}', file=stderr)

logger = Logger()

def read_file(src: Path, show_number: bool = False, start_line: int = 1) -> tuple:
    """Read a single file and print contents to stdout. Return (output_text, next_line_number)."""
    if not src.exists():
        raise CatError(f"File '{src}' does not exist.")
    if src.is_dir():
        raise CatError(f"The path '{src}' is a directory.")

    output_lines = []
    line_num = start_line

    try:
        with open(src, 'r', encoding='utf-8', errors='replace') as f:
            for line in f:
                if show_number:
                    formatted_line = f"{line_num:6d}\t{line}"
                else:
                    formatted_line = line
                output_lines.append(formatted_line)
                line_num += 1
    except Exception as e:
        raise CatError(f"Failed to read '{src}': {e}")

    content = "".join(output_lines)
    print(content, end='')
    return content, line_num

def cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog='cat',
        description='cat command implementation in python',
        epilog='Example: cat.py file1.txt file2.txt -n'
    )

    parser.add_argument(
        'sources',
        type=Path,
        nargs='+',
        help='One or more source files to display'
    )

    parser.add_argument(
        '-n', '--number',
        action='store_true',
        help='Number all output lines'
    )

    return parser.parse_args()

def main():
    args = cli()
    current_line = 1

    for src_path in args.sources:
        try:
            _, current_line = read_file(src_path, show_number=args.number, start_line=current_line)
        except CatError as e:
            logger.error(e)
        except KeyboardInterrupt:
            logger.error('\nOperation interrupted.')
            break

if __name__ == '__main__':
    main()

