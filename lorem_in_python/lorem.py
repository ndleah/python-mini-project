import os
import sys
import random
import string

ALPHA = " abcdefghijklmnopqrstuvwxyz "

def generate_lorem(num_rows: int = 5, output_path: str = None) -> str:
    """Generate random lorem-style text paragraph into output_path."""
    script_dir = os.path.dirname(__file__)
    if output_path is None:
        output_path = os.path.join(script_dir, "text.txt")

    max_idx = len(ALPHA) - 1

    lines = []
    for _ in range(num_rows):
        row_chars = [ALPHA[random.randint(0, max_idx)] for _ in range(70)]
        lines.append("".join(row_chars))

    content = "\n".join(lines) + "\n"

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Lorem text ({num_rows} rows) generated successfully: {output_path}")
        return output_path
    except Exception as e:
        print(f"Error writing lorem text file: {e}")
        return None

def main():
    if len(sys.argv) > 1:
        try:
            num_rows = int(sys.argv[1])
        except ValueError:
            num_rows = 5
    else:
        try:
            raw_input = input("Enter the number of rows for your paragraph: ").strip()
            num_rows = int(raw_input) if raw_input else 5
        except ValueError:
            num_rows = 5

    generate_lorem(num_rows)

if __name__ == '__main__':
    main()