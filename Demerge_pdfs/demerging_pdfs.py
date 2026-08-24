"""
Demerge PDFs - A versatile PDF splitting and demerging utility.

Features:
- Split PDF by custom page counts per chunk (Interactive Mode)
- Split PDF into equal-sized chunks of N pages (Equal Mode)
- Extract specific page ranges e.g. '1-5, 8, 10-12' (Ranges Mode)
- Burst PDF into individual single-page documents (Burst Mode)
- Fully supports CLI arguments and interactive terminal workflows
- Cross-version compatibility for pypdf and PyPDF2 (v3+ and legacy)
"""

import os
import sys
import re
import argparse
from typing import List, Tuple, Optional

# --- PDF Library Compatibility Layer ---
PDF_LIB = None
try:
    import pypdf
    PDF_LIB = 'pypdf'
except ImportError:
    try:
        import PyPDF2
        PDF_LIB = 'PyPDF2'
    except ImportError:
        PDF_LIB = None


def check_pdf_library():
    """Verify that a compatible PDF library (pypdf or PyPDF2) is installed."""
    if PDF_LIB is None:
        print("Error: Neither 'pypdf' nor 'PyPDF2' is installed.")
        print("Please install pypdf by running:\n  pip install pypdf\nor\n  pip install PyPDF2")
        return False
    return True


class PDFAdapter:
    """Wrapper to provide uniform interface across pypdf and various PyPDF2 versions."""

    @staticmethod
    def get_reader(stream_or_path):
        if PDF_LIB == 'pypdf':
            return pypdf.PdfReader(stream_or_path)
        elif PDF_LIB == 'PyPDF2':
            if hasattr(PyPDF2, 'PdfReader'):
                return PyPDF2.PdfReader(stream_or_path)
            else:
                return PyPDF2.PdfFileReader(stream_or_path)
        else:
            raise ImportError("No compatible PDF library found.")

    @staticmethod
    def get_page_count(reader) -> int:
        if hasattr(reader, 'pages'):
            return len(reader.pages)
        elif hasattr(reader, 'numPages'):
            return reader.numPages
        elif hasattr(reader, 'getNumPages'):
            return reader.getNumPages()
        return 0

    @staticmethod
    def get_page(reader, index: int):
        if hasattr(reader, 'pages'):
            return reader.pages[index]
        elif hasattr(reader, 'getPage'):
            return reader.getPage(index)
        raise AttributeError("Cannot retrieve page from reader.")

    @staticmethod
    def create_writer():
        if PDF_LIB == 'pypdf':
            return pypdf.PdfWriter()
        elif PDF_LIB == 'PyPDF2':
            if hasattr(PyPDF2, 'PdfWriter'):
                return PyPDF2.PdfWriter()
            else:
                return PyPDF2.PdfFileWriter()
        else:
            raise ImportError("No compatible PDF library found.")

    @staticmethod
    def add_page_to_writer(writer, page):
        if hasattr(writer, 'add_page'):
            writer.add_page(page)
        elif hasattr(writer, 'addPage'):
            writer.addPage(page)
        else:
            raise AttributeError("Cannot add page to writer.")

    @staticmethod
    def write_to_file(writer, output_file_obj):
        writer.write(output_file_obj)


def check_valid_filename(filename: str) -> bool:
    """Check if the provided filename contains any illegal characters."""
    invalid_chars = r'[/\\:*?"<>|]'
    if re.search(invalid_chars, filename):
        print('A file name cannot contain any of these characters: / \\ : * ? " < > |')
        return False
    return True


def sanitize_filename(filename: str, default_name: str = "output") -> str:
    """Sanitize filename by stripping illegal characters and ensuring .pdf extension."""
    name = filename.strip()
    if not name:
        name = default_name
    name = re.sub(r'[/\\:*?"<>|]', '_', name)
    if not name.lower().endswith('.pdf'):
        name += '.pdf'
    return name


def parse_page_ranges(range_str: str, total_pages: int) -> List[Tuple[int, int]]:
    """
    Parse a page range string such as '1-5, 8, 10-12' into 0-indexed page tuples [(0, 5), (7, 8), (9, 12)].
    
    Raises:
        ValueError: If range syntax is invalid or page numbers are out of bounds.
    """
    cleaned = range_str.strip()
    if not cleaned:
        raise ValueError("Range string cannot be empty.")

    ranges: List[Tuple[int, int]] = []
    parts = [p.strip() for p in cleaned.split(',') if p.strip()]

    for part in parts:
        if '-' in part:
            bounds = part.split('-')
            if len(bounds) != 2:
                raise ValueError(f"Invalid range segment '{part}'. Format should be start-end (e.g. 1-5).")
            start_str, end_str = bounds[0].strip(), bounds[1].strip()
            if not start_str.isdigit() or not end_str.isdigit():
                raise ValueError(f"Range values must be integers in '{part}'.")
            start, end = int(start_str), int(end_str)
            if start < 1:
                raise ValueError(f"Page numbers must be >= 1. Found {start} in '{part}'.")
            if end > total_pages:
                raise ValueError(f"Page number {end} exceeds total pages ({total_pages}).")
            if start > end:
                raise ValueError(f"Start page {start} cannot be greater than end page {end} in '{part}'.")
            ranges.append((start - 1, end))
        else:
            if not part.isdigit():
                raise ValueError(f"Page value '{part}' must be an integer.")
            page_num = int(part)
            if page_num < 1 or page_num > total_pages:
                raise ValueError(f"Page number {page_num} is out of bounds (1-{total_pages}).")
            ranges.append((page_num - 1, page_num))

    return ranges


def write_pdf_chunk(reader, start_idx: int, end_idx: int, output_path: str):
    """Extract a slice of pages from reader and write to output_path."""
    writer = PDFAdapter.create_writer()
    for page_idx in range(start_idx, end_idx):
        page = PDFAdapter.get_page(reader, page_idx)
        PDFAdapter.add_page_to_writer(writer, page)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, 'wb') as out_f:
        PDFAdapter.write_to_file(writer, out_f)


def split_by_page_counts(input_path: str, chunk_definitions: List[Tuple[str, int]], output_dir: str = ".") -> List[str]:
    """
    Split PDF according to a list of (filename, page_count) definitions.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input PDF file not found: '{input_path}'")

    generated_files = []
    with open(input_path, 'rb') as f:
        reader = PDFAdapter.get_reader(f)
        total_pages = PDFAdapter.get_page_count(reader)

        total_requested = sum(count for _, count in chunk_definitions)
        if total_requested > total_pages:
            raise ValueError(f"Total requested pages ({total_requested}) exceeds document pages ({total_pages}).")

        current_idx = 0
        for name, count in chunk_definitions:
            if count <= 0:
                continue
            out_name = sanitize_filename(name)
            out_path = os.path.join(output_dir, out_name)
            write_pdf_chunk(reader, current_idx, current_idx + count, out_path)
            generated_files.append(out_path)
            current_idx += count

    return generated_files


def split_by_fixed_size(input_path: str, page_size: int, output_dir: str = ".", prefix: Optional[str] = None) -> List[str]:
    """
    Split PDF into equal parts of `page_size` pages each.
    """
    if page_size <= 0:
        raise ValueError("Page size must be a positive integer.")
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input PDF file not found: '{input_path}'")

    base_name = prefix or os.path.splitext(os.path.basename(input_path))[0]
    generated_files = []

    with open(input_path, 'rb') as f:
        reader = PDFAdapter.get_reader(f)
        total_pages = PDFAdapter.get_page_count(reader)

        chunk_idx = 1
        for start_idx in range(0, total_pages, page_size):
            end_idx = min(start_idx + page_size, total_pages)
            num_pages_in_part = end_idx - start_idx
            out_name = f"{base_name}_part{chunk_idx}_{num_pages_in_part}pages.pdf"
            out_path = os.path.join(output_dir, out_name)
            write_pdf_chunk(reader, start_idx, end_idx, out_path)
            generated_files.append(out_path)
            chunk_idx += 1

    return generated_files


def split_by_ranges(input_path: str, range_str: str, output_dir: str = ".", prefix: Optional[str] = None) -> List[str]:
    """
    Split PDF according to page range string (e.g. '1-5, 8, 10-12').
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input PDF file not found: '{input_path}'")

    base_name = prefix or os.path.splitext(os.path.basename(input_path))[0]
    generated_files = []

    with open(input_path, 'rb') as f:
        reader = PDFAdapter.get_reader(f)
        total_pages = PDFAdapter.get_page_count(reader)
        parsed_ranges = parse_page_ranges(range_str, total_pages)

        for i, (start_idx, end_idx) in enumerate(parsed_ranges, 1):
            if start_idx + 1 == end_idx:
                out_name = f"{base_name}_page_{start_idx + 1}.pdf"
            else:
                out_name = f"{base_name}_pages_{start_idx + 1}-{end_idx}.pdf"
            out_path = os.path.join(output_dir, out_name)
            write_pdf_chunk(reader, start_idx, end_idx, out_path)
            generated_files.append(out_path)

    return generated_files


def split_burst_all(input_path: str, output_dir: str = ".", prefix: Optional[str] = None) -> List[str]:
    """
    Burst PDF into single page files (1 page per PDF).
    """
    return split_by_fixed_size(input_path, page_size=1, output_dir=output_dir, prefix=prefix)


def interactive_mode():
    """Run an interactive wizard in the terminal for demerging PDFs."""
    print("=" * 60)
    print("           PDF Demerger - Interactive Assistant           ")
    print("=" * 60)

    # 1. Prompt for input file
    while True:
        input_pdf = input("\nEnter the path of the PDF to demerge: ").strip().strip('"').strip("'")
        if not input_pdf:
            print("File path cannot be empty.")
            continue
        if not os.path.exists(input_pdf):
            print(f"File not found: '{input_pdf}'. Please check the path and try again.")
            continue
        if not input_pdf.lower().endswith('.pdf'):
            print("The specified file does not appear to be a PDF. Please enter a valid .pdf file.")
            continue
        try:
            with open(input_pdf, 'rb') as f:
                reader = PDFAdapter.get_reader(f)
                total_pages = PDFAdapter.get_page_count(reader)
                if total_pages == 0:
                    print("The selected PDF has 0 pages or is corrupted. Please choose another file.")
                    continue
                print(f"\nSuccessfully loaded '{os.path.basename(input_pdf)}' with {total_pages} total pages.")
                break
        except Exception as e:
            print(f"Failed to open PDF: {e}. Please try again.")

    # 2. Output directory
    output_dir = input("\nEnter output directory (leave empty for current folder): ").strip().strip('"').strip("'")
    if not output_dir:
        output_dir = "."
    os.makedirs(output_dir, exist_ok=True)

    # 3. Choose mode
    print("\nSelect Demerging Mode:")
    print("  1. Custom Chunking (interactive name & page counts per piece)")
    print("  2. Equal Page Chunks (e.g. every N pages)")
    print("  3. Custom Page Ranges (e.g. 1-5, 8, 10-15)")
    print("  4. Burst All Pages (1 page per PDF file)")

    while True:
        choice = input("\nEnter choice (1-4): ").strip()
        if choice in ['1', '2', '3', '4']:
            break
        print("Invalid option. Please enter 1, 2, 3, or 4.")

    if choice == '1':
        remaining_pages = total_pages
        chunks = []
        part_num = 1
        print(f"\n--- Custom Chunking ({total_pages} pages total) ---")

        while remaining_pages > 0:
            print(f"\nRemaining pages: {remaining_pages}")
            default_name = f"part_{part_num}"
            while True:
                name_in = input(f"Enter filename for part {part_num} [default: {default_name}]: ").strip()
                if not name_in:
                    name_in = default_name
                if check_valid_filename(name_in):
                    break

            while True:
                pages_in = input(f"Enter number of pages for '{name_in}' (1 to {remaining_pages}): ").strip()
                try:
                    pages_val = int(pages_in)
                    if 1 <= pages_val <= remaining_pages:
                        break
                    print(f"Page number must be between 1 and {remaining_pages}.")
                except ValueError:
                    print("Please enter a valid positive integer.")

            chunks.append((name_in, pages_val))
            remaining_pages -= pages_val
            part_num += 1

            if remaining_pages > 0:
                more = input(f"\n{remaining_pages} pages left. Continue splitting remainder? (y/n) [default: y]: ").strip().lower()
                if more in ['n', 'no']:
                    print(f"Stopping early. Only the first {total_pages - remaining_pages} pages will be extracted.")
                    break

        print("\nProcessing PDF splits...")
        results = split_by_page_counts(input_pdf, chunks, output_dir=output_dir)

    elif choice == '2':
        while True:
            size_in = input(f"\nEnter number of pages per chunk (1-{total_pages}): ").strip()
            try:
                page_size = int(size_in)
                if 1 <= page_size <= total_pages:
                    break
                print(f"Chunk size must be between 1 and {total_pages}.")
            except ValueError:
                print("Please enter a valid positive integer.")

        prefix = input("Enter output filename prefix (leave empty for original filename): ").strip()
        print("\nProcessing PDF splits...")
        results = split_by_fixed_size(input_pdf, page_size, output_dir=output_dir, prefix=prefix or None)

    elif choice == '3':
        while True:
            range_str = input("\nEnter page ranges (e.g. 1-5, 8, 10-12): ").strip()
            try:
                # Validate range
                parse_page_ranges(range_str, total_pages)
                break
            except ValueError as e:
                print(f"Invalid range: {e}. Please try again.")

        prefix = input("Enter output filename prefix (leave empty for original filename): ").strip()
        print("\nProcessing PDF splits...")
        results = split_by_ranges(input_pdf, range_str, output_dir=output_dir, prefix=prefix or None)

    elif choice == '4':
        prefix = input("Enter output filename prefix (leave empty for original filename): ").strip()
        print("\nProcessing PDF splits...")
        results = split_burst_all(input_pdf, output_dir=output_dir, prefix=prefix or None)

    print("\n" + "=" * 60)
    print("🎉 Successfully Demerged PDF!")
    print(f"Generated {len(results)} file(s) in: {os.path.abspath(output_dir)}")
    for file_path in results:
        print(f"  - {os.path.basename(file_path)}")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Demerge PDFs: A versatile utility to split, extract, or burst PDF documents.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Interactive Mode:
    python demerging_pdfs.py

  Split into 10-page chunks:
    python demerging_pdfs.py -i sample.pdf -m equal -p 10 -o ./output

  Extract specific ranges:
    python demerging_pdfs.py -i sample.pdf -m ranges -r "1-5, 8, 12-20" -o ./output

  Burst into single pages:
    python demerging_pdfs.py -i sample.pdf -m burst -o ./single_pages
        """
    )

    parser.add_argument("-i", "--input", help="Path to the input PDF file to demerge.")
    parser.add_argument("-m", "--mode", choices=["interactive", "equal", "ranges", "burst"],
                        help="Splitting mode: 'interactive', 'equal', 'ranges', or 'burst'.")
    parser.add_argument("-p", "--pages", type=int, help="Page chunk size (for 'equal' mode).")
    parser.add_argument("-r", "--ranges", type=str, help="Page ranges e.g. '1-5, 8, 10-15' (for 'ranges' mode).")
    parser.add_argument("-o", "--output-dir", default=".", help="Output directory to save split PDFs (default: current directory).")
    parser.add_argument("--prefix", help="Prefix for generated output PDF filenames.")

    args = parser.parse_args()

    if not check_pdf_library():
        sys.exit(1)

    # If no arguments provided, launch interactive mode
    if len(sys.argv) == 1 or args.mode == "interactive" or (args.input is None and args.mode is None):
        interactive_mode()
        return

    if not args.input:
        parser.error("--input / -i is required when running in command-line mode.")

    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' does not exist.")
        sys.exit(1)

    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)

    try:
        if args.mode == "equal":
            if not args.pages:
                parser.error("--pages / -p is required for 'equal' mode.")
            results = split_by_fixed_size(args.input, args.pages, output_dir=output_dir, prefix=args.prefix)
        elif args.mode == "ranges":
            if not args.ranges:
                parser.error("--ranges / -r is required for 'ranges' mode.")
            results = split_by_ranges(args.input, args.ranges, output_dir=output_dir, prefix=args.prefix)
        elif args.mode == "burst":
            results = split_burst_all(args.input, output_dir=output_dir, prefix=args.prefix)
        else:
            parser.error("Please specify a valid --mode: 'equal', 'ranges', or 'burst'.")

        print("=" * 60)
        print("🎉 Successfully Demerged PDF!")
        print(f"Generated {len(results)} file(s) in: {os.path.abspath(output_dir)}")
        for f in results:
            print(f"  - {os.path.basename(f)}")
        print("=" * 60)

    except Exception as e:
        print(f"Error during demerging: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
