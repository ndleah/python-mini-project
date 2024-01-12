import os
from pathlib import Path
from win32com.client import Dispatch


def convert_xls_to_xlsx(file_path: str, file_format: int = 51):
    """Convert an Excel file from '.xls' to '.xlsx' format.

    Args:
    - file_path (str): The path to the input '.xls' file.
    - file_format (int, optional): The file format code for '.xlsx'.
    Default is 51.
    """
    excel_app = Dispatch("Excel.Application")
    excel_app.Visible = False
    output_path = str(file_path) + 'x'
    workbook = excel_app.Workbooks.Open(file_path)
    workbook.SaveAs(output_path, FileFormat=file_format)
    workbook.Close()
    excel_app.Quit()


def remove_old_file(file_path: str):
    """Delete the old 'xls' file.

    Args:
    - file_path (str): The path to the old 'xls' file.
    """
    Path(file_path).unlink(missing_ok=False)


def main():
    file_path = str(input("Input the '.xls' file path:\n"))
    convert_xls_to_xlsx(file_path=file_path)

    file_name = os.path.basename(file_path)
    print(f"Successfully converts {file_name}")

    is_delete = str(input(
        f"Do you want to delete the old {file_name} file (y/n)? ")).lower()

    if is_delete == 'y':
        remove_old_file(file_path=file_path)
        print(f"Successfully removes {file_name}")
    else:
        pass


if __name__ == '__main__':
    main()
