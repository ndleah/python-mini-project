import os
import sys
import re

def get_pdf_reader_writer():
    """Return PyPDF2 or pypdf PdfReader and PdfWriter classes."""
    try:
        from pypdf import PdfReader, PdfWriter
        return PdfReader, PdfWriter
    except ImportError:
        try:
            from PyPDF2 import PdfReader, PdfWriter
            return PdfReader, PdfWriter
        except ImportError:
            try:
                from PyPDF2 import PdfFileReader, PdfFileWriter
                class ReaderAdapter:
                    def __init__(self, stream):
                        self._r = PdfFileReader(stream)
                        self.pages = [self._r.getPage(i) for i in range(self._r.numPages)]
                class WriterAdapter(PdfFileWriter):
                    def add_page(self, page):
                        self.addPage(page)
                return ReaderAdapter, WriterAdapter
            except ImportError:
                return None, None

def check_valid_filename(filename: str) -> bool:
    """Validate output PDF file name against forbidden OS path characters."""
    invalid_chars = r'[/\\:*?"<>|]'
    if re.search(invalid_chars, filename):
        print('A file name cannot contain any of these characters: / \\ : * ? " < > |')
        return False
    return True

def demerge_pdf(pdf_path: str = None, page_splits: list = None, output_dir: str = None) -> list:
    """Demerge/split a multi-page PDF into separate PDF documents."""
    script_dir = os.path.dirname(__file__)
    if pdf_path is None:
        pdf_path = os.path.join(script_dir, "Python.pdf")

    if not os.path.exists(pdf_path):
        print(f"Notice: Source PDF file '{pdf_path}' not found.")
        return []

    ReaderClass, WriterClass = get_pdf_reader_writer()
    if ReaderClass is None:
        print("Notice: PyPDF2 or pypdf library not installed.")
        return []

    output_files = []

    try:
        with open(pdf_path, 'rb') as f:
            reader = ReaderClass(f)
            total_pages = len(reader.pages)
            print(f"Loaded '{pdf_path}' with {total_pages} total pages.")

            if page_splits is None:
                # Default split: 10 pages per file
                chunk_size = 10
                page_splits = []
                for i in range(0, total_pages, chunk_size):
                    end_idx = min(i + chunk_size, total_pages)
                    page_splits.append((f"split_part_{(i // chunk_size) + 1}", end_idx - i))

            current_page = 0
            if output_dir is None:
                output_dir = script_dir

            for name, page_count in page_splits:
                if current_page >= total_pages:
                    break

                writer = WriterClass()
                end_page = min(current_page + page_count, total_pages)

                for p in range(current_page, end_page):
                    page = reader.pages[p]
                    if hasattr(writer, 'add_page'):
                        writer.add_page(page)
                    else:
                        writer.addPage(page)

                out_filename = f"{name}.pdf" if not name.endswith(".pdf") else name
                out_path = os.path.join(output_dir, out_filename)

                with open(out_path, 'wb') as out_f:
                    writer.write(out_f)

                print(f"Created split PDF: '{out_path}' ({end_page - current_page} pages)")
                output_files.append(out_path)
                current_page = end_page

    except Exception as e:
        print(f"Error demerging PDF '{pdf_path}': {e}")

    return output_files

def main():
    target_pdf = sys.argv[1] if len(sys.argv) > 1 else None
    demerge_pdf(pdf_path=target_pdf)

if __name__ == '__main__':
    main()

