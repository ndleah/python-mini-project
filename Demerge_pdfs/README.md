![Star Badge](https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20Useful&style=style=flat&color=BC4E99)
![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)

# Demerging PDFs

## 🛠️ Description

A powerful, robust Python utility to split, demerge, and extract pages from large PDF documents without modifying the original source file.

### ✨ Features
- **Interactive Wizard Mode**: Step-by-step assistant that displays remaining page counts, prevents invalid page inputs, and lets you custom-name each output piece.
- **Equal Chunk Splitting**: Automatically split a PDF into equal parts of *N* pages each (e.g. split a 100-page book every 10 pages).
- **Page Ranges Extraction**: Extract specific page ranges and individual pages in one go (e.g. `1-5, 8, 12-20`).
- **Burst Mode**: Split every page into its own individual PDF document.
- **Command-Line Interface (CLI)**: Full support for automated scripts and terminal execution with flags (`-i`, `-m`, `-p`, `-r`, `-o`, `--prefix`).
- **Modern Compatibility**: Supports `pypdf` as well as `PyPDF2` (v3.0+ and legacy).
- **Safe Output Handling**: Direct outputs to any destination folder, creating directories on-the-fly and sanitizing filenames.

---

## ⚙️ Requirements & Installation

Install the required dependencies using pip:

```sh
pip install -r requirements.txt
```
*Alternatively:*
```sh
pip install pypdf
```

---

## 🌟 How to Run

### 1. Interactive Mode
Run the script without arguments to launch the interactive CLI wizard:
```sh
python demerging_pdfs.py
```
You will be prompted for:
1. The path to your PDF file
2. The destination folder
3. The splitting mode (Custom Chunks, Equal Pages, Page Ranges, or Burst)

---

### 2. Command-Line (CLI) Modes

#### A. Equal Size Split
Split `document.pdf` into chunks of 10 pages each:
```sh
python demerging_pdfs.py -i document.pdf -m equal -p 10 -o ./output_folder
```

#### B. Specific Page Ranges
Extract pages 1 through 5, page 8, and pages 12 through 20:
```sh
python demerging_pdfs.py -i document.pdf -m ranges -r "1-5, 8, 12-20" -o ./extracted_pages
```

#### C. Burst Mode (1 Page Per File)
Extract every page into individual PDFs:
```sh
python demerging_pdfs.py -i document.pdf -m burst -o ./burst_pages
```

---

## 🧪 Running Automated Tests

Run the unit test suite to verify filename sanitization, range parsing, and splitting logic:
```sh
python -m unittest test_demerging_pdfs.py -v
```

---

## 🤖 Author & Contributors
- **Original Author**: [Darpan Balar]
- **Improvements & Fixes**: Open Source Contributors
