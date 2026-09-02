import sys

def generate_pyramid(rows: int, pattern: str = "standard") -> str:
    """Generate pyramid pattern string for given row count."""
    if rows <= 0:
        return ""

    lines = []
    pattern_type = pattern.lower().strip()

    if pattern_type == "inverted":
        for i in range(rows, 0, -1):
            spaces = " " * (rows - i)
            stars = "* " * i
            lines.append(spaces + stars.rstrip())
    elif pattern_type == "diamond":
        for i in range(1, rows + 1):
            spaces = " " * (rows - i)
            stars = "* " * i
            lines.append(spaces + stars.rstrip())
        for i in range(rows - 1, 0, -1):
            spaces = " " * (rows - i)
            stars = "* " * i
            lines.append(spaces + stars.rstrip())
    else:  # standard
        for i in range(1, rows + 1):
            spaces = " " * (rows - i)
            stars = "* " * i
            lines.append(spaces + stars.rstrip())

    return "\n".join(lines)

def main():
    print("=== Star Pyramid Pattern Generator ===")
    while True:
        try:
            raw_num = input("\nEnter number of rows (e.g. 5): ").strip()
            if not raw_num:
                break
            num = int(raw_num)
            if num <= 0:
                print("Please enter a positive integer greater than zero.")
                continue

            print("\nSelect Pattern:")
            print("1. Standard Pyramid")
            print("2. Inverted Pyramid")
            print("3. Diamond Pattern")
            p_choice = input("Choice (1-3, default 1): ").strip()

            pattern_map = {"1": "standard", "2": "inverted", "3": "diamond"}
            chosen_pattern = pattern_map.get(p_choice, "standard")

            result = generate_pyramid(num, chosen_pattern)
            print(f"\nResult:\n{result}\n")

            cont = input("Do you want to generate another pyramid? (y/N): ").strip().lower()
            if cont != 'y':
                print("Thanks for using Star Pyramid Generator! Goodbye!")
                break
        except ValueError:
            print("Invalid input! Please enter a valid numeric integer.")
        except (KeyboardInterrupt, EOFError):
            break

if __name__ == '__main__':
    main()