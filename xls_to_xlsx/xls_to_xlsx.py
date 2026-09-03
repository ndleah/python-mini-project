import os
import sys
from pathlib import Path

def convert_xls_to_xlsx(file_path: str, file_format: int = 51) -> str:
    """Convert an Excel file from '.xls' to '.xlsx' format using COM or pandas/openpyxl fallback.

    Args:
        file_path (str): The path to the input '.xls' file.
        file_format (int, optional): The file format code for '.xlsx'. Default is 51.

    Returns:
        str: Output path to converted '.xlsx' file or empty string if failed.
    """
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return ""

    output_path = str(file_path) + 'x' if not file_path.endswith('x') else file_path

    # Attempt win32com COM conversion (Windows with MS Excel installed)
    try:
        from win32com.client import Dispatch
        excel_app = Dispatch("Excel.Application")
        excel_app.Visible = False
        workbook = excel_app.Workbooks.Open(os.path.abspath(file_path))
        workbook.SaveAs(os.path.abspath(output_path), FileFormat=file_format)
        workbook.Close()
        excel_app.Quit()
        print(f"Successfully converted '{file_path}' to '{output_path}' via Excel COM.")
        return output_path
    except Exception as e:
        print(f"Notice: COM/Excel conversion unavailable ({e}). Attempting pure-Python fallback...")

    # Pure-Python fallback using pandas / openpyxl / xlrd
    try:
        import pandas as pd
        excel_data = pd.read_excel(file_path, sheet_name=None)
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            for sheet_name, df in excel_data.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        print(f"Successfully converted '{file_path}' to '{output_path}' via pandas fallback.")
        return output_path
    except Exception as e_fallback:
        print(f"Error converting '{file_path}' using fallback ({e_fallback}).")
        return ""

def remove_old_file(file_path: str):
    """Delete the old 'xls' file.

    Args:
        file_path (str): The path to the old 'xls' file.
    """
    p = Path(file_path)
    if p.exists():
        p.unlink()
        print(f"Successfully removed '{file_path}'.")

def main():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = str(input("Input the '.xls' file path:\n")).strip()

    if not file_path:
        print("No file path provided.")
        return

    out = convert_xls_to_xlsx(file_path=file_path)
    if out:
        file_name = os.path.basename(file_path)
        is_delete = str(input(f"Do you want to delete the old {file_name} file (y/N)? ")).strip().lower()
        if is_delete == 'y':
            remove_old_file(file_path=file_path)

if __name__ == '__main__':
    main()

