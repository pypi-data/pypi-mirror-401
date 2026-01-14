"""
rostaing-ocr: High-Precision OCR Extraction Module
Designed for LLMs and RAG systems. 
Features:
- Robust Windows file handling
- Visual Layout Preservation (Table alignment)
- Single output file overwriting

Dependencies:
    pip install pymupdf easyocr pillow numpy
"""

import os
import sys
import time
import shutil
import warnings
import logging
import gc
from pathlib import Path
from typing import List, Optional, Tuple

# ============================================================
# LIBRARY IMPORTS & SETUP
# ============================================================

# Suppress standard warnings
warnings.filterwarnings("ignore")

# Configure logging
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
logging.getLogger("easyocr").setLevel(logging.ERROR)
logging.getLogger("pymupdf").setLevel(logging.ERROR)

# Check Dependencies
try:
    import fitz  # PyMuPDF
    import easyocr
    from PIL import Image
    import numpy as np
except ImportError as e:
    raise ImportError(f"Missing dependency: {e}. Run: pip install pymupdf easyocr pillow numpy")

# ============================================================
# CORE CLASS
# ============================================================

class ocr_extractor:
    """
    Main extraction class.
    Architecture: Doc -> Local Image File -> Layout-Aware OCR -> Delete Image -> Text
    """
    
    def __init__(
        self, 
        file_path: str, 
        output_file: str = "output.txt", 
        print_to_console: bool = True,
        save_file: bool = True,
        languages: List[str] = None,
        gpu: bool = False
    ):
        """
        Initialize and run OCR immediately.

        Args:
            file_path (str): Path to source document.
            output_file (str): Name/Path of the output file. Defaults to "output.txt".
                               Always overwrites this file.
            print_to_console (bool): Print extracted text to stdout. Defaults to True.
            save_file (bool): Save result to file. Defaults to True.
            languages (list): List of languages ['en', 'fr'].
            gpu (bool): Use GPU if available.
        """
        self.file_path = Path(file_path).resolve()
        self.output_path = Path(output_file).resolve()
        self.print_to_console = print_to_console
        self.save_file = save_file
        self.languages = languages if languages else ['en', 'fr']
        self.gpu = gpu
        
        # Local temp directory setup (in project folder)
        self.project_dir = Path.cwd()
        self.temp_dir = self.project_dir / "temp_ocr_pages"
        
        # State
        self.extracted_text = ""
        self.total_pages = 0
        self.processing_time = 0.0
        self.status = "Pending"
        self.error_msg = None

        # Initialize Model
        print(f"Loading OCR model (Languages: {self.languages})...", file=sys.stderr)
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.reader = easyocr.Reader(self.languages, gpu=self.gpu, verbose=False)
        except Exception as e:
            self.status = "Failed"
            self.error_msg = f"EasyOCR Init Error: {str(e)}"
            return

        self._run_extraction()

    def _run_extraction(self):
        start_time = time.time()
        
        if not self.file_path.exists():
            self.status = "Error"
            self.error_msg = f"File not found: {self.file_path}"
            return

        # Create temp folder
        self.temp_dir.mkdir(exist_ok=True)

        try:
            ext = self.file_path.suffix.lower()
            
            if ext == '.pdf':
                self.extracted_text = self._process_pdf()
            elif ext in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.webp']:
                self.extracted_text = self._process_single_image(self.file_path)
            else:
                raise ValueError(f"Unsupported format: {ext}")

            # Save if requested (Overwrite mode)
            if self.save_file:
                self._save_text()

            # Print if requested
            if self.print_to_console:
                print(self.extracted_text)

            self.status = "Success"

        except Exception as e:
            self.status = "Error"
            self.error_msg = str(e)
            print(f"Critical Error: {e}", file=sys.stderr)
        
        finally:
            # Cleanup temp folder completely
            self._cleanup_temp_dir()
            self.processing_time = time.time() - start_time

    def _process_pdf(self) -> str:
        """Convert PDF -> Images -> Text -> Delete Images."""
        full_text = []
        doc = None
        
        try:
            doc = fitz.open(self.file_path)
            self.total_pages = len(doc)
            
            # Zoom = 2 (approx 150 DPI) is a good balance for speed/accuracy
            mat = fitz.Matrix(2, 2)

            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                pix = page.get_pixmap(matrix=mat)
                
                # 1. Create Image in project temp folder
                image_filename = self.temp_dir / f"page_{page_num}.png"
                pix.save(str(image_filename))
                
                # Free PyMuPDF resource immediately
                pix = None 
                
                try:
                    # 2. Extract with Layout Preservation
                    page_text = self._extract_from_image_path(str(image_filename))
                    if page_text.strip():
                        # Add a separator for LLM clarity
                        full_text.append(f"--- Page {page_num + 1} ---\n{page_text}")
                
                finally:
                    # 3. Delete Image (Robust method for Windows)
                    self._safe_remove(image_filename)
            
            return "\n\n".join(full_text)

        except Exception as e:
            raise RuntimeError(f"PDF Processing failed: {e}")
        finally:
            if doc:
                doc.close()

    def _process_single_image(self, original_path: Path) -> str:
        """Process a single existing image file."""
        self.total_pages = 1
        return self._extract_from_image_path(str(original_path))

    def _extract_from_image_path(self, img_path: str) -> str:
        """
        Runs EasyOCR and reconstructs text preserving visual layout (tables).
        """
        try:
            # Read detailed output: List of (bbox, text, confidence)
            results = self.reader.readtext(img_path)
            
            if not results:
                return ""

            # 1. Sort by Vertical Position (Top-Left Y coordinate)
            # This ensures we process the document top-to-bottom
            results.sort(key=lambda x: x[0][0][1])

            lines = []
            current_line = []
            current_y = None
            # Tolerance in pixels to consider text on the "same line"
            y_tolerance = 15  

            for bbox, text, conf in results:
                top_left_y = bbox[0][1]
                
                if current_y is None:
                    current_y = top_left_y
                    current_line.append((bbox, text))
                
                elif abs(top_left_y - current_y) <= y_tolerance:
                    # It's on the same line
                    current_line.append((bbox, text))
                else:
                    # New line started, process the previous one
                    lines.append(self._format_line_layout(current_line))
                    current_line = [(bbox, text)]
                    current_y = top_left_y
            
            # Process the last line
            if current_line:
                lines.append(self._format_line_layout(current_line))

            return "\n".join(lines)

        except Exception as e:
            return f"[OCR Error: {str(e)}]"

    def _format_line_layout(self, line_items: List[Tuple]) -> str:
        """
        Reconstructs a single line of text, inserting spaces to simulate columns.
        """
        # 1. Sort items in the line by Horizontal Position (X coordinate)
        line_items.sort(key=lambda x: x[0][0][0])
        
        formatted_line = ""
        last_x_end = 0
        
        for bbox, text in line_items:
            x_start = bbox[0][0]
            x_end = bbox[1][0]
            
            # Calculate gap from previous word
            gap = x_start - last_x_end
            
            if last_x_end == 0:
                # First word of the line
                formatted_line += text
            else:
                # If gap is significant (> 20px), add padding to simulate table column
                if gap > 20:
                    # Add 1 space roughly per 8 pixels of gap
                    spaces = int(gap / 8)
                    formatted_line += " " * spaces + text
                else:
                    # Standard space between words
                    formatted_line += " " + text
            
            last_x_end = x_end
            
        return formatted_line

    def _safe_remove(self, file_path: Path):
        """
        Robust file deletion for Windows to handle 'Permission denied'.
        """
        if not file_path.exists():
            return

        max_retries = 5
        for i in range(max_retries):
            try:
                os.remove(file_path)
                return
            except PermissionError:
                gc.collect()
                time.sleep(0.2)
            except Exception as e:
                print(f"Warning: Could not delete {file_path.name}: {e}", file=sys.stderr)
                return
        
        print(f"Warning: Failed to delete temp file: {file_path.name}", file=sys.stderr)

    def _cleanup_temp_dir(self):
        """Remove the entire temp directory at the end."""
        if self.temp_dir.exists():
            try:
                shutil.rmtree(self.temp_dir, ignore_errors=True)
            except Exception:
                pass

    def _save_text(self):
        """Saves text to output file (Overwriting mode)."""
        try:
            # Mode 'w' overwrites the file completely
            with open(self.output_path, 'w', encoding='utf-8') as f:
                f.write(self.extracted_text)
        except IOError as e:
            print(f"Warning: Could not save output file: {e}", file=sys.stderr)

    def __str__(self):
        """String representation showing status summary only."""
        if self.status == "Success":
            return (
                f"--- OCR Extraction Summary ---\n"
                f"Source: {self.file_path.name}\n"
                f"Status: {self.status}\n"
                f"Pages: {self.total_pages}\n"
                f"Output: {self.output_path.name}\n"
                f"Time: {self.processing_time:.2f}s"
            )
        else:
            return (
                f"--- OCR Extraction Failed ---\n"
                f"Source: {self.file_path}\n"
                f"Error: {self.error_msg}"
            )

# ============================================================
# CLI USAGE
# ============================================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python rostaing_ocr.py <file_path>")
    else:
        # Defaults defined in __init__ will be used
        extractor = ocr_extractor(sys.argv[1])
        print(str(extractor), file=sys.stderr)

# ------------------------------------------------------------ #

# """
# rostaing-ocr: High-Precision OCR Extraction Module
# Designed for LLMs and RAG systems. 
# Features:
# - Robust Windows file handling
# - Visual Layout Preservation (Table alignment)
# - Single output file overwriting

# Dependencies:
#     pip install pymupdf easyocr pillow numpy
# """

# import os
# import sys
# import time
# import shutil
# import warnings
# import logging
# import gc
# from pathlib import Path
# from typing import List, Optional, Tuple

# # ============================================================
# # LIBRARY IMPORTS & SETUP
# # ============================================================

# # Suppress standard warnings
# warnings.filterwarnings("ignore")

# # Configure logging
# os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
# logging.getLogger("easyocr").setLevel(logging.ERROR)
# logging.getLogger("pymupdf").setLevel(logging.ERROR)

# # Check Dependencies
# try:
#     import fitz  # PyMuPDF
#     import easyocr
#     from PIL import Image
#     import numpy as np
# except ImportError as e:
#     raise ImportError(f"Missing dependency: {e}. Run: pip install pymupdf easyocr pillow numpy")

# # ============================================================
# # CORE CLASS
# # ============================================================

# class ocr_extractor:
#     """
#     Main extraction class.
#     Architecture: Doc -> Local Image File -> Layout-Aware OCR -> Delete Image -> Text
#     """
    
#     def __init__(
#         self, 
#         file_path: str, 
#         output_file: str = "output.txt", # Default fixed to output.txt
#         print_to_console: bool = False,
#         save_file: bool = True,
#         languages: List[str] = None,
#         gpu: bool = False
#     ):
#         """
#         Initialize and run OCR immediately.

#         Args:
#             file_path: Path to source document.
#             output_file: Name/Path of the output file. Defaults to "output.txt".
#                          Always overwrites this file.
#             print_to_console: Print extracted text to stdout.
#             save_file: Save result to file.
#             languages: List of languages ['en', 'fr'].
#             gpu: Use GPU if available.
#         """
#         self.file_path = Path(file_path).resolve()
#         self.print_to_console = print_to_console
#         self.save_file = save_file
#         self.output_path = Path(output_file).resolve()
#         self.languages = languages if languages else ['en', 'fr']
#         self.gpu = gpu
        
#         # Local temp directory setup (in project folder)
#         self.project_dir = Path.cwd()
#         self.temp_dir = self.project_dir / "temp_ocr_pages"
        
#         # State
#         self.extracted_text = ""
#         self.total_pages = 0
#         self.processing_time = 0.0
#         self.status = "Pending"
#         self.error_msg = None

#         # Initialize Model
#         print(f"Loading OCR model (Languages: {self.languages})...", file=sys.stderr)
#         try:
#             with warnings.catch_warnings():
#                 warnings.simplefilter("ignore")
#                 self.reader = easyocr.Reader(self.languages, gpu=self.gpu, verbose=False)
#         except Exception as e:
#             self.status = "Failed"
#             self.error_msg = f"EasyOCR Init Error: {str(e)}"
#             return

#         self._run_extraction()

#     def _run_extraction(self):
#         start_time = time.time()
        
#         if not self.file_path.exists():
#             self.status = "Error"
#             self.error_msg = f"File not found: {self.file_path}"
#             return

#         # Create temp folder
#         self.temp_dir.mkdir(exist_ok=True)

#         try:
#             ext = self.file_path.suffix.lower()
            
#             if ext == '.pdf':
#                 self.extracted_text = self._process_pdf()
#             elif ext in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.webp']:
#                 self.extracted_text = self._process_single_image(self.file_path)
#             else:
#                 raise ValueError(f"Unsupported format: {ext}")

#             # Save if requested (Overwrite mode)
#             if self.save_file:
#                 self._save_text()

#             # Print if requested
#             if self.print_to_console:
#                 print(self.extracted_text)

#             self.status = "Success"

#         except Exception as e:
#             self.status = "Error"
#             self.error_msg = str(e)
#             print(f"Critical Error: {e}", file=sys.stderr)
        
#         finally:
#             # Cleanup temp folder completely
#             self._cleanup_temp_dir()
#             self.processing_time = time.time() - start_time

#     def _process_pdf(self) -> str:
#         """Convert PDF -> Images -> Text -> Delete Images."""
#         full_text = []
#         doc = None
        
#         try:
#             doc = fitz.open(self.file_path)
#             self.total_pages = len(doc)
            
#             # Zoom = 2 (approx 150 DPI) is a good balance for speed/accuracy
#             mat = fitz.Matrix(2, 2)

#             for page_num in range(len(doc)):
#                 page = doc.load_page(page_num)
#                 pix = page.get_pixmap(matrix=mat)
                
#                 # 1. Create Image in project temp folder
#                 image_filename = self.temp_dir / f"page_{page_num}.png"
#                 pix.save(str(image_filename))
                
#                 # Free PyMuPDF resource immediately
#                 pix = None 
                
#                 try:
#                     # 2. Extract with Layout Preservation
#                     page_text = self._extract_from_image_path(str(image_filename))
#                     if page_text.strip():
#                         # Add a separator for LLM clarity
#                         full_text.append(f"--- Page {page_num + 1} ---\n{page_text}")
                
#                 finally:
#                     # 3. Delete Image (Robust method for Windows)
#                     self._safe_remove(image_filename)
            
#             return "\n\n".join(full_text)

#         except Exception as e:
#             raise RuntimeError(f"PDF Processing failed: {e}")
#         finally:
#             if doc:
#                 doc.close()

#     def _process_single_image(self, original_path: Path) -> str:
#         """Process a single existing image file."""
#         self.total_pages = 1
#         return self._extract_from_image_path(str(original_path))

#     def _extract_from_image_path(self, img_path: str) -> str:
#         """
#         Runs EasyOCR and reconstructs text preserving visual layout (tables).
#         """
#         try:
#             # Read detailed output: List of (bbox, text, confidence)
#             results = self.reader.readtext(img_path)
            
#             if not results:
#                 return ""

#             # 1. Sort by Vertical Position (Top-Left Y coordinate)
#             # This ensures we process the document top-to-bottom
#             results.sort(key=lambda x: x[0][0][1])

#             lines = []
#             current_line = []
#             current_y = None
#             # Tolerance in pixels to consider text on the "same line"
#             y_tolerance = 15  

#             for bbox, text, conf in results:
#                 top_left_y = bbox[0][1]
                
#                 if current_y is None:
#                     current_y = top_left_y
#                     current_line.append((bbox, text))
                
#                 elif abs(top_left_y - current_y) <= y_tolerance:
#                     # It's on the same line
#                     current_line.append((bbox, text))
#                 else:
#                     # New line started, process the previous one
#                     lines.append(self._format_line_layout(current_line))
#                     current_line = [(bbox, text)]
#                     current_y = top_left_y
            
#             # Process the last line
#             if current_line:
#                 lines.append(self._format_line_layout(current_line))

#             return "\n".join(lines)

#         except Exception as e:
#             return f"[OCR Error: {str(e)}]"

#     def _format_line_layout(self, line_items: List[Tuple]) -> str:
#         """
#         Reconstructs a single line of text, inserting spaces to simulate columns.
#         """
#         # 1. Sort items in the line by Horizontal Position (X coordinate)
#         line_items.sort(key=lambda x: x[0][0][0])
        
#         formatted_line = ""
#         last_x_end = 0
        
#         for bbox, text in line_items:
#             x_start = bbox[0][0]
#             x_end = bbox[1][0]
            
#             # Calculate gap from previous word
#             gap = x_start - last_x_end
            
#             if last_x_end == 0:
#                 # First word of the line
#                 formatted_line += text
#             else:
#                 # If gap is significant (> 20px), add padding to simulate table column
#                 if gap > 20:
#                     # Add 1 space roughly per 8 pixels of gap
#                     spaces = int(gap / 8)
#                     formatted_line += " " * spaces + text
#                 else:
#                     # Standard space between words
#                     formatted_line += " " + text
            
#             last_x_end = x_end
            
#         return formatted_line

#     def _safe_remove(self, file_path: Path):
#         """
#         Robust file deletion for Windows to handle 'Permission denied'.
#         """
#         if not file_path.exists():
#             return

#         max_retries = 5
#         for i in range(max_retries):
#             try:
#                 os.remove(file_path)
#                 return
#             except PermissionError:
#                 gc.collect()
#                 time.sleep(0.2)
#             except Exception as e:
#                 print(f"Warning: Could not delete {file_path.name}: {e}", file=sys.stderr)
#                 return
        
#         print(f"Warning: Failed to delete temp file: {file_path.name}", file=sys.stderr)

#     def _cleanup_temp_dir(self):
#         """Remove the entire temp directory at the end."""
#         if self.temp_dir.exists():
#             try:
#                 shutil.rmtree(self.temp_dir, ignore_errors=True)
#             except Exception:
#                 pass

#     def _save_text(self):
#         """Saves text to output file (Overwriting mode)."""
#         try:
#             # Mode 'w' overwrites the file completely
#             with open(self.output_path, 'w', encoding='utf-8') as f:
#                 f.write(self.extracted_text)
#         except IOError as e:
#             print(f"Warning: Could not save output file: {e}", file=sys.stderr)

#     def __str__(self):
#         """String representation showing status summary only."""
#         if self.status == "Success":
#             return (
#                 f"--- OCR Extraction Summary ---\n"
#                 f"Source: {self.file_path.name}\n"
#                 f"Status: {self.status}\n"
#                 f"Pages: {self.total_pages}\n"
#                 f"Output: {self.output_path.name}\n"
#                 f"Time: {self.processing_time:.2f}s"
#             )
#         else:
#             return (
#                 f"--- OCR Extraction Failed ---\n"
#                 f"Source: {self.file_path}\n"
#                 f"Error: {self.error_msg}"
#             )

# # ============================================================
# # CLI USAGE
# # ============================================================
# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print("Usage: python rostaing_ocr.py <file_path>")
#     else:
#         # Default usage via CLI
#         extractor = ocr_extractor(
#             sys.argv[1], 
#             output_file="output.txt", 
#             print_to_console=True, 
#             save_file=True
#         )
#         print(str(extractor), file=sys.stderr)