"""
rostaing-ocr: Deep Learning Layout-Aware OCR
Features:
- 100% Local (CPU/GPU).
- No .exe dependencies.
- Uses Base64 architecture for image handling.
- Uses DocTR (ResNet+Transformer) for smart block detection.
- **Layout-Aware**: Reconstructs tables by analyzing word geometry.

Dependencies:
    pip install python-doctr[torch] pymupdf
"""

import os
import sys
import time
import base64
import warnings
import json
from pathlib import Path
from typing import List, Any

# ============================================================
# LIBRARY SETUP
# ============================================================
warnings.filterwarnings("ignore")
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

try:
    import fitz  # PyMuPDF
    from doctr.io import DocumentFile
    from doctr.models import ocr_predictor
    import torch
except ImportError as e:
    raise ImportError(f"Missing dependency: {e}. Run: pip install python-doctr[torch] pymupdf")

# ============================================================
# CORE CLASS
# ============================================================

class ocr_extractor:
    def __init__(
        self, 
        file_path: str, 
        output_file: str = "output.txt", 
        print_to_console: bool = False,
        save_file: bool = True
    ):
        self.file_path = Path(file_path).resolve()
        self.output_path = Path(output_file).resolve()
        self.print_to_console = print_to_console
        self.save_file = save_file
        
        self.extracted_text = ""
        self.processing_time = 0.0
        self.status = "Pending"

        # Initialize DocTR Model (Deep Learning)
        print("Loading RostaingOCR (Deep Learning Model)...", file=sys.stderr)
        
        # Check for GPU
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Running on: {self.device}", file=sys.stderr)
        
        try:
            # We use the default model (DBNet + CRNN) which is excellent for documents
            self.model = ocr_predictor(det_arch='db_resnet50', reco_arch='crnn_vgg16_bn', pretrained=True)
            if torch.cuda.is_available():
                self.model.cuda()
        except Exception as e:
            self.status = "Model Load Error"
            print(f"Error loading model: {e}", file=sys.stderr)
            return

        try:
            self._pipeline()
        except Exception as e:
            self.status = "Error"
            print(f"Critical Error: {e}", file=sys.stderr)

    def _pipeline(self):
        start_time = time.time()
        
        if not self.file_path.exists():
            print(f"File not found: {self.file_path}", file=sys.stderr)
            return

        try:
            # 1. Conversion to Base64 (Your requested architecture)
            base64_pages = []
            ext = self.file_path.suffix.lower()
            
            if ext == '.pdf':
                base64_pages = self._pdf_to_base64_list()
            elif ext in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
                base64_pages = [self._image_to_base64(self.file_path)]
            else:
                raise ValueError(f"Unsupported format: {ext}")

            # 2. OCR Processing via DocTR (from Base64 data)
            full_text_pages = []
            
            for i, b64_data in enumerate(base64_pages):
                page_text = self._process_base64_with_doctr(b64_data)
                full_text_pages.append(f"--- Page {i + 1} ---\n{page_text}")

            self.extracted_text = "\n\n".join(full_text_pages)

            # 3. Save
            if self.save_file:
                with open(self.output_path, 'w', encoding='utf-8') as f:
                    f.write(self.extracted_text)

            # 4. Print
            if self.print_to_console:
                print(self.extracted_text)

            self.status = "Success"

        finally:
            self.processing_time = time.time() - start_time

    def _pdf_to_base64_list(self) -> List[str]:
        """Convert PDF pages to High-Res Base64."""
        b64_list = []
        doc = fitz.open(self.file_path)
        try:
            # Zoom x2 is usually enough for DocTR
            mat = fitz.Matrix(2, 2)
            for page in doc:
                pix = page.get_pixmap(matrix=mat, alpha=False)
                img_bytes = pix.tobytes("png")
                b64_str = base64.b64encode(img_bytes).decode('utf-8')
                b64_list.append(b64_str)
        finally:
            doc.close()
        return b64_list

    def _image_to_base64(self, path: Path) -> str:
        """Read image to Base64."""
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode('utf-8')

    def _process_base64_with_doctr(self, b64_string: str) -> str:
        """
        Decodes Base64 and runs Deep Learning OCR.
        
        LAYOUT-AWARE LOGIC:
        Instead of iterating by Blocks (which breaks tables), this function:
        1. Flattens all words.
        2. Sorts them by Y-coordinate.
        3. Clusters them into visual lines based on vertical alignment.
        4. Reconstructs horizontal spacing.
        """
        # Decode Base64 back to bytes
        image_bytes = base64.b64decode(b64_string)
        
        # DocTR expects a list of images (bytes)
        doc = DocumentFile.from_images(image_bytes)
        
        # Inference
        result = self.model(doc)
        
        page = result.pages[0]
        
        # 1. Extract all words with their geometry
        all_words = []
        for block in page.blocks:
            for line in block.lines:
                for word in line.words:
                    # geometry is ((xmin, ymin), (xmax, ymax))
                    xmin, ymin = word.geometry[0]
                    xmax, ymax = word.geometry[1]
                    center_y = (ymin + ymax) / 2
                    height = ymax - ymin
                    
                    all_words.append({
                        'text': word.value,
                        'xmin': xmin,
                        'xmax': xmax,
                        'cy': center_y,
                        'height': height
                    })

        if not all_words:
            return ""

        # 2. Sort all words by vertical position (Top to Bottom)
        all_words.sort(key=lambda w: w['cy'])

        # 3. Cluster words into visual lines
        lines = []
        current_line = []
        
        if all_words:
            current_line = [all_words[0]]

        for word in all_words[1:]:
            last_word = current_line[-1]
            
            # Check vertical distance to see if it's the same line
            # Threshold: 50% of the word height
            dist = abs(word['cy'] - last_word['cy'])
            avg_h = (word['height'] + last_word['height']) / 2
            
            if dist < (avg_h * 0.5):
                current_line.append(word)
            else:
                lines.append(current_line)
                current_line = [word]
        
        if current_line:
            lines.append(current_line)

        # 4. Construct Output String with Table Spacing
        output_str = []
        
        for line in lines:
            # Sort words in line from Left to Right
            line.sort(key=lambda w: w['xmin'])
            
            line_text = ""
            last_x_end = 0
            
            for word in line:
                if last_x_end == 0:
                    line_text += word['text']
                else:
                    gap = word['xmin'] - last_x_end
                    
                    # Logic for spacing:
                    # > 0.1 (10% of page width) -> Big Tab (Column separator)
                    # > 0.02 (2% of page width) -> Space
                    if gap > 0.1:
                        line_text += " \t   " + word['text'] 
                    elif gap > 0.02:
                        line_text += " " + word['text']
                    else:
                        line_text += " " + word['text']

                last_x_end = word['xmax']
            
            output_str.append(line_text)
            
        return "\n".join(output_str)

    def __str__(self):
        return f"RostaingOCR Extraction Complete | Time: {self.processing_time:.2f}s | Output: {self.output_path}"

# ============================================================
# EXECUTION
# ============================================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python rostaing_ocr.py <file_path>")
    else:
        extractor = ocr_extractor(
            sys.argv[1], 
            print_to_console=False, 
            save_file=True
        )
        print(str(extractor), file=sys.stderr)


# -----------------------------------------------------------#
# """
# rostaing-ocr-doctr: Deep Learning Layout-Aware OCR
# Features:
# - 100% Local (CPU/GPU).
# - No .exe dependencies.
# - Uses Base64 architecture for image handling.
# - Uses DocTR (ResNet+Transformer) for smart block detection (preserves columns).

# Dependencies:
#     pip install python-doctr[torch] pymupdf
# """

# import os
# import sys
# import time
# import base64
# import warnings
# import json
# from pathlib import Path
# from typing import List, Any

# # ============================================================
# # LIBRARY SETUP
# # ============================================================
# warnings.filterwarnings("ignore")
# os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# try:
#     import fitz  # PyMuPDF
#     from doctr.io import DocumentFile
#     from doctr.models import ocr_predictor
#     import torch
# except ImportError as e:
#     raise ImportError(f"Missing dependency: {e}. Run: pip install python-doctr[torch] pymupdf")

# # ============================================================
# # CORE CLASS
# # ============================================================

# class ocr_extractor:
#     def __init__(
#         self, 
#         file_path: str, 
#         output_file: str = "output.txt", 
#         print_to_console: bool = False, # Demandé
#         save_file: bool = True          # Demandé
#     ):
#         self.file_path = Path(file_path).resolve()
#         self.output_path = Path(output_file).resolve()
#         self.print_to_console = print_to_console
#         self.save_file = save_file
        
#         self.extracted_text = ""
#         self.processing_time = 0.0
#         self.status = "Pending"

#         # Initialize DocTR Model (Deep Learning)
#         # pretrained=True downloads the models once (~300MB)
#         print("Loading DocTR (Deep Learning Model)...", file=sys.stderr)
        
#         # Check for GPU
#         self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#         print(f"Running on: {self.device}", file=sys.stderr)
        
#         try:
#             # We use the default model (DBNet + CRNN) which is excellent for documents
#             self.model = ocr_predictor(det_arch='db_resnet50', reco_arch='crnn_vgg16_bn', pretrained=True)
#             if torch.cuda.is_available():
#                 self.model.cuda()
#         except Exception as e:
#             self.status = "Model Load Error"
#             print(f"Error loading model: {e}", file=sys.stderr)
#             return

#         try:
#             self._pipeline()
#         except Exception as e:
#             self.status = "Error"
#             print(f"Critical Error: {e}", file=sys.stderr)

#     def _pipeline(self):
#         start_time = time.time()
        
#         if not self.file_path.exists():
#             print(f"File not found: {self.file_path}", file=sys.stderr)
#             return

#         try:
#             # 1. Conversion en Base64 (Architecture demandée)
#             # Cela permet de normaliser l'entrée qu'elle soit PDF ou Image
#             base64_pages = []
#             ext = self.file_path.suffix.lower()
            
#             if ext == '.pdf':
#                 base64_pages = self._pdf_to_base64_list()
#             elif ext in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
#                 base64_pages = [self._image_to_base64(self.file_path)]
#             else:
#                 raise ValueError(f"Unsupported format: {ext}")

#             # 2. Traitement OCR via DocTR (depuis les données Base64)
#             full_text_pages = []
            
#             for i, b64_data in enumerate(base64_pages):
#                 page_text = self._process_base64_with_doctr(b64_data)
#                 full_text_pages.append(f"--- Page {i + 1} ---\n{page_text}")

#             self.extracted_text = "\n\n".join(full_text_pages)

#             # 3. Sauvegarde
#             if self.save_file:
#                 with open(self.output_path, 'w', encoding='utf-8') as f:
#                     f.write(self.extracted_text)

#             # 4. Affichage (Optionnel)
#             if self.print_to_console:
#                 print(self.extracted_text)

#             self.status = "Success"

#         finally:
#             self.processing_time = time.time() - start_time

#     def _pdf_to_base64_list(self) -> List[str]:
#         """Convert PDF pages to High-Res Base64."""
#         b64_list = []
#         doc = fitz.open(self.file_path)
#         try:
#             # Zoom x2 is usually enough for DocTR (it uses ResNet upscaling)
#             mat = fitz.Matrix(2, 2)
#             for page in doc:
#                 pix = page.get_pixmap(matrix=mat, alpha=False)
#                 img_bytes = pix.tobytes("png")
#                 b64_str = base64.b64encode(img_bytes).decode('utf-8')
#                 b64_list.append(b64_str)
#         finally:
#             doc.close()
#         return b64_list

#     def _image_to_base64(self, path: Path) -> str:
#         """Read image to Base64."""
#         with open(path, "rb") as f:
#             return base64.b64encode(f.read()).decode('utf-8')

#     def _process_base64_with_doctr(self, b64_string: str) -> str:
#         """
#         Decodes Base64 and runs Deep Learning OCR.
#         DocTR is 'Block Aware': it separates columns naturally.
#         """
#         # Decode Base64 back to bytes
#         image_bytes = base64.b64decode(b64_string)
        
#         # DocTR expects a list of images (bytes)
#         doc = DocumentFile.from_images(image_bytes)
        
#         # Inference
#         result = self.model(doc)
        
#         # Reconstruction structurée
#         # DocTR Hierarchy: Page -> Block -> Line -> Word
#         # Blocks are typically paragraphs or columns.
        
#         output_lines = []
#         page = result.pages[0] # We process one page at a time here
        
#         # Sort blocks by Y (top to bottom), then X (left to right)
#         # This prevents reading the right column before the left one
#         blocks = page.blocks
#         blocks.sort(key=lambda b: (b.geometry[0][1], b.geometry[0][0]))

#         for block in blocks:
#             for line in block.lines:
#                 line_text = " ".join([word.value for word in line.words])
#                 output_lines.append(line_text)
            
#             # Add a small separator between blocks to simulate layout
#             output_lines.append("") 
            
#         return "\n".join(output_lines)

#     def __str__(self):
#         return f"DocTR Extraction Complete | Time: {self.processing_time:.2f}s | Output: {self.output_path}"

# # ============================================================
# # EXECUTION
# # ============================================================
# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print("Usage: python rostaing_ocr_doctr.py <file_path>")
#     else:
#         extractor = ocr_extractor(
#             sys.argv[1], 
#             print_to_console=False, 
#             save_file=True
#         )
#         print(str(extractor), file=sys.stderr)

# ----------------------------------------------------------- #
# """
# rostaing-ocr: High-Precision Async OCR Extraction Module
# Optimized for Table Preservation and Invoice Details.

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
# import asyncio
# import statistics
# from pathlib import Path
# from typing import List, Optional, Tuple, Dict
# from concurrent.futures import ThreadPoolExecutor

# # ============================================================
# # LIBRARY IMPORTS & SETUP
# # ============================================================

# warnings.filterwarnings("ignore")
# os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
# logging.getLogger("easyocr").setLevel(logging.ERROR)
# logging.getLogger("pymupdf").setLevel(logging.ERROR)

# try:
#     import fitz  # PyMuPDF
#     import easyocr
#     from PIL import Image
#     import numpy as np
# except ImportError as e:
#     raise ImportError(f"Missing dependency: {e}")

# # ============================================================
# # CORE CLASS
# # ============================================================

# class ocr_extractor:
#     """
#     Main extraction class with enhanced layout analysis for invoices/tables.
#     """
    
#     def __init__(
#         self, 
#         file_path: str, 
#         output_file: str = "output.txt", 
#         print_to_console: bool = True,
#         save_file: bool = True,
#         languages: List[str] = None,
#         gpu: bool = False
#     ):
#         self.file_path = Path(file_path).resolve()
#         self.output_path = Path(output_file).resolve()
#         self.print_to_console = print_to_console
#         self.save_file = save_file
#         self.languages = languages if languages else ['fr', 'en'] # French first for invoices
#         self.gpu = gpu
        
#         self.project_dir = Path.cwd()
#         self.temp_dir = self.project_dir / "temp_ocr_pages"
        
#         self.extracted_text = ""
#         self.total_pages = 0
#         self.processing_time = 0.0
#         self.status = "Pending"
#         self.error_msg = None

#         # Increase workers slightly, but keep safe
#         self.executor = ThreadPoolExecutor(max_workers=min(os.cpu_count(), 4))

#         print(f"Loading OCR model (Languages: {self.languages})...", file=sys.stderr)
#         try:
#             with warnings.catch_warnings():
#                 warnings.simplefilter("ignore")
#                 # Loaded once. GPU usage is critical for speed.
#                 self.reader = easyocr.Reader(
#                     self.languages, 
#                     gpu=self.gpu, 
#                     verbose=False,
#                     quantize=False 
#                 )
#         except Exception as e:
#             self.status = "Failed"
#             self.error_msg = f"EasyOCR Init Error: {str(e)}"
#             return

#         try:
#             asyncio.run(self._pipeline())
#         except Exception as e:
#             self.status = "Error"
#             self.error_msg = str(e)
#             print(f"Critical Error: {e}", file=sys.stderr)
#         finally:
#             self.executor.shutdown(wait=False)

#     async def _pipeline(self):
#         start_time = time.time()
        
#         if not self.file_path.exists():
#             print(f"File not found: {self.file_path}", file=sys.stderr)
#             return

#         self.temp_dir.mkdir(exist_ok=True)

#         try:
#             ext = self.file_path.suffix.lower()
            
#             if ext == '.pdf':
#                 self.extracted_text = await self._process_pdf_async()
#             elif ext in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.webp']:
#                 self.extracted_text = await self._process_single_image_async(self.file_path)
#             else:
#                 raise ValueError(f"Unsupported format: {ext}")

#             if self.save_file:
#                 await self._save_text_async()

#             if self.print_to_console:
#                 print(self.extracted_text)

#             self.status = "Success"

#         except Exception as e:
#             self.status = "Error"
#             self.error_msg = str(e)
#             print(f"Pipeline Error: {e}", file=sys.stderr)
        
#         finally:
#             self._cleanup_temp_dir()
#             self.processing_time = time.time() - start_time

#     async def _process_pdf_async(self) -> str:
#         full_text_map = {}
#         doc = None
#         tasks = []
        
#         try:
#             doc = fitz.open(self.file_path)
#             self.total_pages = len(doc)
            
#             # IMPROVEMENT 1: Higher DPI (Zoom 3x) for better small text detection (SIRET, conditions)
#             mat = fitz.Matrix(3, 3) 
            
#             sem = asyncio.Semaphore(2) # Lower concurrency to save RAM with high-res images

#             for page_num in range(len(doc)):
#                 page = doc.load_page(page_num)
#                 pix = page.get_pixmap(matrix=mat, alpha=False) # Alpha False for JPEG/PNG
                
#                 image_filename = self.temp_dir / f"page_{page_num}.png"
#                 pix.save(str(image_filename))
                
#                 tasks.append(
#                     self._process_page_task(sem, page_num, image_filename)
#                 )

#             results = await asyncio.gather(*tasks)
#             valid_results = [res for res in results if res.strip()]
#             return "\n\n".join(valid_results)

#         except Exception as e:
#             raise RuntimeError(f"PDF Processing failed: {e}")
#         finally:
#             if doc: doc.close()

#     async def _process_page_task(self, sem, page_num, image_path: Path):
#         async with sem:
#             loop = asyncio.get_running_loop()
#             text = await loop.run_in_executor(
#                 self.executor, 
#                 self._extract_from_image_path, 
#                 str(image_path)
#             )
#             await loop.run_in_executor(None, self._safe_remove, image_path)
            
#             if text.strip():
#                 return f"--- Page {page_num + 1} ---\n{text}"
#             return ""

#     async def _process_single_image_async(self, original_path: Path) -> str:
#         self.total_pages = 1
#         loop = asyncio.get_running_loop()
#         return await loop.run_in_executor(
#             self.executor, 
#             self._extract_from_image_path, 
#             str(original_path)
#         )

#     def _extract_from_image_path(self, img_path: str) -> str:
#         """
#         Runs EasyOCR with specific tuning for documents/tables.
#         """
#         try:
#             # IMPROVEMENT 2: Document-specific tuning
#             # width_ths=0.1 : Prevents merging separate table columns into one word
#             # contrast_ths : Helps with faint text
#             results = self.reader.readtext(
#                 img_path,
#                 paragraph=False,
#                 width_ths=0.1, 
#                 x_ths=1.0,  # Strict horizontal grouping
#                 contrast_ths=0.3,
#                 adjust_contrast=0.5
#             )
            
#             if not results:
#                 return ""

#             # Sort primarily by Y (top to bottom), secondarily by X (left to right)
#             results.sort(key=lambda x: (x[0][0][1], x[0][0][0]))

#             # IMPROVEMENT 3: Dynamic Line Tolerance
#             # Instead of fixed 15px, calculate based on average text height
#             heights = [abs(bbox[2][1] - bbox[0][1]) for bbox, _, _ in results]
#             avg_height = statistics.median(heights) if heights else 20
#             y_tolerance = avg_height * 0.6  # approx 60% of line height

#             lines = []
#             current_line = []
#             current_y = None

#             for bbox, text, conf in results:
#                 top_left_y = bbox[0][1]
                
#                 if current_y is None:
#                     current_y = top_left_y
#                     current_line.append((bbox, text))
                
#                 elif abs(top_left_y - current_y) <= y_tolerance:
#                     current_line.append((bbox, text))
#                 else:
#                     lines.append(self._format_line_layout(current_line))
#                     current_line = [(bbox, text)]
#                     current_y = top_left_y # Reset baseline
            
#             if current_line:
#                 lines.append(self._format_line_layout(current_line))

#             return "\n".join(lines)

#         except Exception as e:
#             return f"[OCR Error: {str(e)}]"

#     def _format_line_layout(self, line_items: List[Tuple]) -> str:
#         """
#         Reconstructs a single line, simulating visual gaps to keep tables readable.
#         """
#         if not line_items:
#             return ""

#         # Sort by Horizontal Position
#         line_items.sort(key=lambda x: x[0][0][0])
        
#         formatted_line = ""
#         last_x_end = 0
        
#         # Calculate scale factor roughly (based on typical char width ~10-15px)
#         space_width_approx = 12 

#         for bbox, text in line_items:
#             x_start = bbox[0][0]
#             x_end = bbox[1][0]
            
#             if last_x_end == 0:
#                 # First item in line
#                 formatted_line += text
#             else:
#                 gap = x_start - last_x_end
                
#                 # IMPROVEMENT 4: Smarter Spacing / Tabulation
#                 if gap > 50:
#                     # Large gap -> Likely a new column
#                     formatted_line += " \t| " + text 
#                 elif gap > 15:
#                     # Medium gap -> Just spacing
#                     spaces = int(gap / space_width_approx)
#                     formatted_line += " " * spaces + text
#                 else:
#                     # Small gap -> Single space
#                     formatted_line += " " + text
            
#             last_x_end = x_end
            
#         return formatted_line

#     def _safe_remove(self, file_path: Path):
#         if not file_path.exists(): return
#         for i in range(5):
#             try:
#                 os.remove(file_path)
#                 return
#             except Exception:
#                 time.sleep(0.1)

#     def _cleanup_temp_dir(self):
#         if self.temp_dir.exists():
#             shutil.rmtree(self.temp_dir, ignore_errors=True)

#     async def _save_text_async(self):
#         loop = asyncio.get_running_loop()
#         await loop.run_in_executor(None, self._write_file_sync)

#     def _write_file_sync(self):
#         with open(self.output_path, 'w', encoding='utf-8') as f:
#             f.write(self.extracted_text)

#     def __str__(self):
#         return f"OCR Status: {self.status} | Pages: {self.total_pages} | Time: {self.processing_time:.2f}s"

# # ============================================================
# # CLI USAGE
# # ============================================================
# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print("Usage: python rostaing_ocr.py <file_path>")
#     else:
#         extractor = ocr_extractor(sys.argv[1])
#         print(str(extractor), file=sys.stderr)


# ------------------------------------------------------------ #
# """
# rostaing-ocr: High-Precision Async OCR Extraction Module
# Designed for LLMs and RAG systems.
# Features:
# - Asynchronous Processing (Parallel Page OCR)
# - Robust Windows file handling
# - Visual Layout Preservation
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
# import asyncio
# import functools
# from pathlib import Path
# from typing import List, Optional, Tuple
# from concurrent.futures import ThreadPoolExecutor

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
#     Architecture: Doc -> Local Images -> Async OCR -> Delete Images -> Text
#     """
    
#     def __init__(
#         self, 
#         file_path: str, 
#         output_file: str = "output.txt", 
#         print_to_console: bool = True,
#         save_file: bool = True,
#         languages: List[str] = None,
#         gpu: bool = False
#     ):
#         """
#         Initialize and run OCR immediately using AsyncIO.

#         Args:
#             file_path (str): Path to source document.
#             output_file (str): Name/Path of the output file. Defaults to "output.txt".
#             print_to_console (bool): Print extracted text to stdout. Defaults to True.
#             save_file (bool): Save result to file. Defaults to True.
#             languages (list): List of languages ['en', 'fr'].
#             gpu (bool): Use GPU if available.
#         """
#         self.file_path = Path(file_path).resolve()
#         self.output_path = Path(output_file).resolve()
#         self.print_to_console = print_to_console
#         self.save_file = save_file
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

#         # Thread Pool for CPU bound tasks (OCR)
#         # We limit workers to avoid OOM on weak machines
#         self.executor = ThreadPoolExecutor(max_workers=os.cpu_count())

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

#         # ENTRY POINT: Run the Async pipeline synchronously
#         try:
#             asyncio.run(self._pipeline())
#         except Exception as e:
#             self.status = "Error"
#             self.error_msg = str(e)
#             print(f"Critical Error: {e}", file=sys.stderr)
#         finally:
#             self.executor.shutdown(wait=False)

#     async def _pipeline(self):
#         """Main Async Orchestrator."""
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
#                 self.extracted_text = await self._process_pdf_async()
#             elif ext in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.webp']:
#                 self.extracted_text = await self._process_single_image_async(self.file_path)
#             else:
#                 raise ValueError(f"Unsupported format: {ext}")

#             # Save if requested
#             if self.save_file:
#                 await self._save_text_async()

#             # Print if requested
#             if self.print_to_console:
#                 print(self.extracted_text)

#             self.status = "Success"

#         except Exception as e:
#             self.status = "Error"
#             self.error_msg = str(e)
#             print(f"Pipeline Error: {e}", file=sys.stderr)
        
#         finally:
#             self._cleanup_temp_dir()
#             self.processing_time = time.time() - start_time

#     async def _process_pdf_async(self) -> str:
#         """
#         Async PDF Processing:
#         1. Extract all pages to images (Synchronous fitz, fast)
#         2. Process images via OCR in Parallel (Async + Threads)
#         """
#         full_text_map = {} # Store results by page index to maintain order
#         doc = None
#         tasks = []
        
#         try:
#             # Step 1: Rapid Image Extraction
#             doc = fitz.open(self.file_path)
#             self.total_pages = len(doc)
#             mat = fitz.Matrix(2, 2) # Zoom factor for DPI

#             # Semaphore to limit concurrent heavy OCR tasks (prevent OOM)
#             sem = asyncio.Semaphore(4) 

#             for page_num in range(len(doc)):
#                 page = doc.load_page(page_num)
#                 pix = page.get_pixmap(matrix=mat)
                
#                 image_filename = self.temp_dir / f"page_{page_num}.png"
#                 pix.save(str(image_filename))
                
#                 # Create async task for this page
#                 tasks.append(
#                     self._process_page_task(sem, page_num, image_filename)
#                 )

#             # Step 2: Run OCR in parallel
#             # gather returns results in the order of tasks
#             results = await asyncio.gather(*tasks)
            
#             # Step 3: Combine results
#             # Filter out empty pages
#             valid_results = [res for res in results if res.strip()]
#             return "\n\n".join(valid_results)

#         except Exception as e:
#             raise RuntimeError(f"PDF Processing failed: {e}")
#         finally:
#             if doc:
#                 doc.close()

#     async def _process_page_task(self, sem, page_num, image_path: Path):
#         """Worker for a single page: OCR -> Cleanup."""
#         async with sem:
#             # Run OCR in ThreadPool to avoid blocking event loop
#             loop = asyncio.get_running_loop()
#             text = await loop.run_in_executor(
#                 self.executor, 
#                 self._extract_from_image_path, 
#                 str(image_path)
#             )
            
#             # Clean up image immediately after processing
#             await loop.run_in_executor(None, self._safe_remove, image_path)
            
#             if text.strip():
#                 return f"--- Page {page_num + 1} ---\n{text}"
#             return ""

#     async def _process_single_image_async(self, original_path: Path) -> str:
#         """Process a single existing image file asynchronously."""
#         self.total_pages = 1
#         loop = asyncio.get_running_loop()
#         return await loop.run_in_executor(
#             self.executor, 
#             self._extract_from_image_path, 
#             str(original_path)
#         )

#     def _extract_from_image_path(self, img_path: str) -> str:
#         """
#         Runs EasyOCR and reconstructs text preserving visual layout (tables).
#         (This runs inside the ThreadPoolExecutor)
#         """
#         try:
#             # Read detailed output
#             results = self.reader.readtext(img_path)
            
#             if not results:
#                 return ""

#             # Sort by Vertical Position
#             results.sort(key=lambda x: x[0][0][1])

#             lines = []
#             current_line = []
#             current_y = None
#             y_tolerance = 15  

#             for bbox, text, conf in results:
#                 top_left_y = bbox[0][1]
                
#                 if current_y is None:
#                     current_y = top_left_y
#                     current_line.append((bbox, text))
                
#                 elif abs(top_left_y - current_y) <= y_tolerance:
#                     current_line.append((bbox, text))
#                 else:
#                     lines.append(self._format_line_layout(current_line))
#                     current_line = [(bbox, text)]
#                     current_y = top_left_y
            
#             if current_line:
#                 lines.append(self._format_line_layout(current_line))

#             return "\n".join(lines)

#         except Exception as e:
#             return f"[OCR Error: {str(e)}]"

#     def _format_line_layout(self, line_items: List[Tuple]) -> str:
#         """Reconstructs a single line with spacing."""
#         # Sort by Horizontal Position
#         line_items.sort(key=lambda x: x[0][0][0])
        
#         formatted_line = ""
#         last_x_end = 0
        
#         for bbox, text in line_items:
#             x_start = bbox[0][0]
#             x_end = bbox[1][0]
            
#             gap = x_start - last_x_end
            
#             if last_x_end == 0:
#                 formatted_line += text
#             else:
#                 if gap > 20:
#                     spaces = int(gap / 8)
#                     formatted_line += " " * spaces + text
#                 else:
#                     formatted_line += " " + text
            
#             last_x_end = x_end
            
#         return formatted_line

#     def _safe_remove(self, file_path: Path):
#         """Synchronous remove, called within executor."""
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
#         """Remove the entire temp directory."""
#         if self.temp_dir.exists():
#             try:
#                 shutil.rmtree(self.temp_dir, ignore_errors=True)
#             except Exception:
#                 pass

#     async def _save_text_async(self):
#         """Asynchronous file write."""
#         try:
#             loop = asyncio.get_running_loop()
#             await loop.run_in_executor(
#                 None, 
#                 self._write_file_sync
#             )
#         except Exception as e:
#             print(f"Warning: Could not save output file: {e}", file=sys.stderr)

#     def _write_file_sync(self):
#         """Actual write operation."""
#         with open(self.output_path, 'w', encoding='utf-8') as f:
#             f.write(self.extracted_text)

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
#         extractor = ocr_extractor(sys.argv[1])
#         print(str(extractor), file=sys.stderr)


# --------------------------------------------------------------- #
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
#         output_file: str = "output.txt", 
#         print_to_console: bool = True,
#         save_file: bool = True,
#         languages: List[str] = None,
#         gpu: bool = False
#     ):
#         """
#         Initialize and run OCR immediately.

#         Args:
#             file_path (str): Path to source document.
#             output_file (str): Name/Path of the output file. Defaults to "output.txt".
#                                Always overwrites this file.
#             print_to_console (bool): Print extracted text to stdout. Defaults to True.
#             save_file (bool): Save result to file. Defaults to True.
#             languages (list): List of languages ['en', 'fr'].
#             gpu (bool): Use GPU if available.
#         """
#         self.file_path = Path(file_path).resolve()
#         self.output_path = Path(output_file).resolve()
#         self.print_to_console = print_to_console
#         self.save_file = save_file
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
#         # Defaults defined in __init__ will be used
#         extractor = ocr_extractor(sys.argv[1])
#         print(str(extractor), file=sys.stderr)

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