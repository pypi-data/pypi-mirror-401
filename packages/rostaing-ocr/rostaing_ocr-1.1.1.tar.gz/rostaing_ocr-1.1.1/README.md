<p align="center">
  <a href="https://pypi.org/project/rostaing-ocr/"><img src="https://img.shields.io/pypi/v/rostaing-ocr?color=blue&label=PyPI%20version" alt="PyPI version"></a>
  <a href="https://pypi.org/project/rostaing-ocr/"><img src="https://img.shields.io/pypi/pyversions/rostaing-ocr.svg" alt="Python versions"></a>
  <a href="https://github.com/Rostaing/rostaing-ocr/blob/main/LICENSE"><img src="https://img.shields.io/pypi/l/rostaing-ocr.svg" alt="License"></a>
  <a href="https://pepy.tech/project/rostaing-ocr"><img src="https://static.pepy.tech/badge/rostaing-ocr" alt="Downloads"></a>
</p>

# rostaing-ocr

**High-Precision OCR Extraction for LLMs and RAG Systems**

`rostaing-ocr` is a robust Python library designed to extract text from PDFs and images with high visual fidelity. Unlike standard text extraction tools, this library converts every document page into a high-resolution image before processing. This ensures that the layout (columns, tables) is preserved and that text hidden in complex PDF structures is captured correctly.

It is specifically optimized for **Retrieval-Augmented Generation (RAG)** pipelines where maintaining the visual structure of data (like tables) is critical for LLM comprehension.

## Features

- **Universal Image Conversion:** Converts PDF pages to images to bypass encoding errors.
- **Layout Preservation:** Smart algorithms detect columns and tables to insert spacing, keeping data aligned for LLMs.
- **Robust Windows Support:** Handles file permissions and temporary file cleanup gracefully.
- **Auto-Overwrite:** By default, saves to `output.txt` and overwrites it on each run (configurable).
- **Privacy Focused:** Temporary images are generated locally and strictly deleted after extraction.

## Installation

```bash
pip install rostaing-ocr
```

## Dependencies

This package relies on:
- `rostaing-ocr` (OCR engine)
- `pymupdf` (PDF processing)
- `pillow` (Image handling)
- `numpy`

## Usage

### 1. Basic Usage (Default Behavior)
By default, the extractor prints to the console and saves the result to `output.txt`, overwriting any previous content.

```python
from rostaing_ocr import ocr_extractor

# This immediately runs the extraction
extractor = ocr_extractor("documents/invoice.pdf")

# The text is now in 'output.txt' and printed to the console
print(extractor) # Prints the summary (status, time, pages)
```

### 2. Custom Output File
You can specify a different filename. The file will be created or overwritten.

```python
from rostaing_ocr import ocr_extractor

extractor = ocr_extractor(
    "data/report.png",
    output_file="results/report_analysis.txt"
)
```

### 3. Silent Mode (No Console Output)
Useful for batch processing where you only want the text saved to files, not cluttering your terminal.

```python
from rostaing_ocr import ocr_extractor

extractor = ocr_extractor(
    "financial_statement.pdf",
    print_to_console=False,
    save_file=True
)
```

### 4. Direct Text Access
You can access the extracted text directly in your Python code without reading the file.

```python
from rostaing_ocr import ocr_extractor

extractor = ocr_extractor("scan.jpg", print_to_console=False)

if extractor.status == "Success":
    my_text = extractor.extracted_text
    # Send 'my_text' to ChatGPT or your RAG system...
```

## CLI Usage

You can also use it directly from the terminal:

```bash
# Basic
python -m rostaing_ocr path/to/document.pdf

# With arguments (if you implement an entry point in the future)
```

## Architecture

1. **Input:** PDF or Image (PNG, JPG, TIFF, etc.).
2. **Preprocessing:** PDF pages are rendered as high-DPI images into a local temporary folder.
3. **Extraction:** `RostaingOCR` reads the image.
4. **Layout Reconstruction:** The custom algorithm sorts text blocks vertically and horizontally, calculating gaps to simulate table columns with spaces.
5. **Cleanup:** Temporary images are forcibly deleted (with retry logic for Windows).
6. **Output:** Clean text string.