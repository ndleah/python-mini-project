import csv
import json
import os
import sys

def parse_value(val: str):
    """Parse string value into native Python/JSON data types."""
    if val is None:
        return None
    val_str = val.strip()
    if val_str == "":
        return None
    if val_str.lower() == "true":
        return True
    if val_str.lower() == "false":
        return False

    try:
        return int(val_str)
    except ValueError:
        pass

    try:
        return float(val_str)
    except ValueError:
        pass

    return val

def csv_to_json(input_file: str, output_file: str = None, parse_types: bool = True) -> str:
    """Convert CSV file to JSON format."""
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file '{input_file}' not found.")

    if not output_file:
        base_name, _ = os.path.splitext(input_file)
        output_file = f"{base_name}.json"

    with open(input_file, mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data_list = []
        for row in csv_reader:
            if parse_types:
                parsed_row = {k: parse_value(v) for k, v in row.items()}
                data_list.append(parsed_row)
            else:
                data_list.append(dict(row))

    with open(output_file, mode='w', encoding='utf-8') as json_file:
        json.dump(data_list, json_file, indent=4, ensure_ascii=False)

    return output_file

def main():
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
    else:
        input_file = input("Enter CSV file path: ").strip()
        output_file = None

    if not input_file:
        print("Error: No input CSV file provided.")
        sys.exit(1)

    try:
        out_path = csv_to_json(input_file, output_file)
        print(f"Successfully converted '{input_file}' to '{out_path}'.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()