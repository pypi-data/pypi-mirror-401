# PdfX API Documentation

Complete documentation for all methods in the PdfX toolkit.

## Table of Contents

1. [Color Utilities](#color-utilities)
   - [parse_color_string](#parse_color_string)
   - [dump_colors](#dump_colors)
2. [Page Range Utilities](#page-range-utilities)
   - [parse_page_ranges](#parse_page_ranges)
3. [PDF Color Filtering](#pdf-color-filtering)
   - [filter_pdf_by_color](#filter_pdf_by_color)
   - [recolor_pdf_text](#recolor_pdf_text)
4. [PDF Image Filters](#pdf-image-filters)
   - [apply_image_filter_to_pdf](#apply_image_filter_to_pdf)
   - [create_scanned_pdf](#create_scanned_pdf)
   - [auto_enhance_pdf](#auto_enhance_pdf)
5. [Image to PDF Conversion](#image-to-pdf-conversion)
   - [images_to_pdf](#images_to_pdf)
   - [images_from_dir_to_pdf](#images_from_dir_to_pdf)
6. [OCR](#ocr)
   - [ocr_make_searchable](#ocr_make_searchable)
7. [PDF Management](#pdf-management)
   - [merge_pdfs](#merge_pdfs)
   - [split_pdf](#split_pdf)

---

## Color Utilities

### parse_color_string

```python
def parse_color_string(color: str) -> Tuple[int, int, int]
```

Parse a color string into an RGB tuple.

**Description:**
Converts various color string formats into a standardized RGB tuple. Supports hexadecimal colors, RGB notation, and 20 predefined color names.

**Args:**
- `color` (str): Color specification in one of the following formats:
  - Hexadecimal: `#RRGGBB` or `RRGGBB` (e.g., `#FF0000`, `00FF00`)
  - RGB notation: `rgb(R, G, B)` or `R,G,B` (e.g., `rgb(255, 0, 0)`, `255,0,0`)
  - Named color: One of 20 predefined colors (see below)

**Returns:**
- `Tuple[int, int, int]`: RGB color tuple with values 0-255.

**Raises:**
- `ValueError`: If the color string format is invalid or unrecognized.

**Supported Named Colors:**
- `red` → (255, 0, 0)
- `green` → (0, 255, 0)
- `blue` → (0, 0, 255)
- `yellow` → (255, 255, 0)
- `cyan` → (0, 255, 255)
- `magenta` → (255, 0, 255)
- `black` → (0, 0, 0)
- `white` → (255, 255, 255)
- `gray` → (128, 128, 128)
- `orange` → (255, 165, 0)
- `purple` → (128, 0, 128)
- `pink` → (255, 192, 203)
- `brown` → (165, 42, 42)
- `navy` → (0, 0, 128)
- `teal` → (0, 128, 128)
- `lime` → (0, 255, 0)
- `maroon` → (128, 0, 0)
- `olive` → (128, 128, 0)
- `silver` → (192, 192, 192)
- `gold` → (255, 215, 0)

**Examples:**
```python
from pdfx import parse_color_string

# Hexadecimal format
color = parse_color_string("#FF0000")
# Returns: (255, 0, 0)

# RGB notation
color = parse_color_string("rgb(0, 255, 0)")
# Returns: (0, 255, 0)

# Named color
color = parse_color_string("blue")
# Returns: (0, 0, 255)

# Comma-separated RGB
color = parse_color_string("255,165,0")
# Returns: (255, 165, 0)
```

---

### dump_colors

```python
def dump_colors(input_path: Path, max_samples: int = 5) -> None
```

Analyze and display all unique text colors found in a PDF document.

**Description:**
This diagnostic function scans all text spans in a PDF and reports the color information, appearance count, and sample text for each unique color found. Useful for understanding what colors are present before filtering or recoloring.

**Args:**
- `input_path` (Path): Path to the PDF file to analyze.
- `max_samples` (int, optional): Maximum number of text samples to display per color. Default: 5.

**Returns:**
- `None`: Prints results to stdout.

**Raises:**
- `ImportError`: If pymupdf is not installed.
- `FileNotFoundError`: If input_path doesn't exist.

**Requirements:**
- `pymupdf` (fitz)

**Output Format:**
```
Color int=0 -> RGB=(0, 0, 0) (count=523)
  sample: This is black text
  sample: Another black sample
Color int=16711680 -> RGB=(255, 0, 0) (count=12)
  sample: Red warning text
```

**Examples:**
```python
from pathlib import Path
from pdfx import dump_colors

# Analyze colors in a PDF
dump_colors(Path("document.pdf"))

# Show more samples per color
dump_colors(Path("document.pdf"), max_samples=10)
```

**Note:**
If no colored text is found, the PDF may contain text embedded as images, or the text may not have color information available via text spans.

---

## Page Range Utilities

### parse_page_ranges

```python
def parse_page_ranges(range_str: Optional[str]) -> Optional[List[int]]
```

Parse a page-range string into a list of 1-based page numbers.

**Description:**
Parses page range specifications commonly used in PDF operations. Supports individual pages, ranges, and comma-separated combinations. Duplicate pages are automatically removed and the result is sorted.

**Args:**
- `range_str` (str, optional): Page range string (e.g., `"1-3,5,7-9"`). Can be None or empty.

**Returns:**
- `List[int]` or `None`: Sorted list of unique 1-based page numbers, or None if input is None/empty.

**Raises:**
- `ValueError`: If range format is invalid or contains non-numeric values.
- `ValueError`: If a range has start > end (e.g., `"5-3"`).

**Examples:**
```python
from pdfx import parse_page_ranges

# Simple range
pages = parse_page_ranges("1-3,5")
# Returns: [1, 2, 3, 5]

# Mixed format
pages = parse_page_ranges("2,4-6,10")
# Returns: [2, 4, 5, 6, 10]

# Duplicates removed automatically
pages = parse_page_ranges("5,3,5,1-3")
# Returns: [1, 2, 3, 5]

# None returns None
pages = parse_page_ranges(None)
# Returns: None
```

---

## PDF Color Filtering

### filter_pdf_by_color

```python
def filter_pdf_by_color(
    input_path: Path,
    output_path: Path,
    target_color: Tuple[int, int, int],
    tolerance: float = 0.0
) -> int
```

Filter PDF text by color, keeping only text that matches the target color within tolerance.

**Description:**
Scans all text in a PDF and creates a new document containing only text that matches the specified color. Useful for extracting highlighted text, annotations, or color-coded content.

**Args:**
- `input_path` (Path): Path to the input PDF file to filter.
- `output_path` (Path): Path where the filtered PDF will be saved.
- `target_color` (Tuple[int, int, int]): RGB color tuple to match, e.g., `(255, 0, 0)` for red. Each value must be in range 0-255.
- `tolerance` (float, optional): Maximum Euclidean color distance to consider a match. Default: 0.0 (exact match). Higher values match more colors. Range: 0 (exact) to ~441 (any color). Typical values: 0-50 for similar colors, 50-100 for color families.

**Returns:**
- `int`: Number of pages written to the output PDF.

**Raises:**
- `ImportError`: If pymupdf is not installed.
- `FileNotFoundError`: If input_path doesn't exist.

**Requirements:**
- `pymupdf` (fitz)

**Examples:**
```python
from pathlib import Path
from pdfx import filter_pdf_by_color

# Extract all red text (exact match)
pages = filter_pdf_by_color(
    Path("document.pdf"),
    Path("red_text.pdf"),
    (255, 0, 0),
    tolerance=0
)
print(f"Processed {pages} pages")

# Extract blue-ish text (fuzzy match)
pages = filter_pdf_by_color(
    Path("document.pdf"),
    Path("blue_text.pdf"),
    (0, 0, 255),
    tolerance=50
)
```

**Note:**
- Text embedded as images will not be filtered
- Font information and sizing are preserved for matched text
- Pages are created with the same dimensions as the original

---

### recolor_pdf_text

```python
def recolor_pdf_text(
    input_path: Path,
    output_path: Path,
    target_color: Tuple[int, int, int],
    new_color: Tuple[int, int, int],
    tolerance: float = 0.0
) -> int
```

Recolor text in a PDF that matches the target color.

**Description:**
Finds all text matching a target color and replaces it with a new color. The original page content is preserved and recolored text is overlaid.

**Args:**
- `input_path` (Path): Path to input PDF file.
- `output_path` (Path): Path to output PDF file.
- `target_color` (Tuple[int, int, int]): RGB tuple (0-255) of color to match.
- `new_color` (Tuple[int, int, int]): RGB tuple (0-255) of replacement color.
- `tolerance` (float, optional): Color distance tolerance for fuzzy matching. Default: 0.0.

**Returns:**
- `int`: Number of pages processed.

**Raises:**
- `ImportError`: If pymupdf is not installed.
- `FileNotFoundError`: If input_path doesn't exist.

**Requirements:**
- `pymupdf` (fitz)

**Examples:**
```python
from pathlib import Path
from pdfx import recolor_pdf_text

# Change red text to blue
pages = recolor_pdf_text(
    Path("document.pdf"),
    Path("recolored.pdf"),
    target_color=(255, 0, 0),
    new_color=(0, 0, 255),
    tolerance=10
)
```

---

## PDF Image Filters

### apply_image_filter_to_pdf

```python
def apply_image_filter_to_pdf(
    input_path: Path,
    output_path: Path,
    filter_name: str,
    strength: float = 1.5
) -> int
```

Apply an image-level filter to each page of a PDF.

**Description:**
Renders each PDF page as an image, applies a visual filter, and reconstructs the PDF. This is useful for applying effects that require image processing rather than text manipulation.

**Args:**
- `input_path` (Path): Path to input PDF file.
- `output_path` (Path): Path to output PDF file.
- `filter_name` (str): Filter to apply. Options:
  - `'enhance'`: Increase contrast (strength = contrast factor, 1.0 = no change)
  - `'bw'`: Convert to black and white (strength = threshold, default 128)
  - `'grayscale'`: Convert to grayscale (strength ignored)
  - `'invert'`: Invert colors (strength ignored)
  - `'auto'`: Apply automatic contrast adjustment (strength ignored)
- `strength` (float, optional): Filter strength/threshold. Meaning depends on filter. Default: 1.5.

**Returns:**
- `int`: Number of pages written.

**Raises:**
- `ImportError`: If pymupdf or Pillow is not installed.
- `ValueError`: If filter_name is unknown.
- `FileNotFoundError`: If input_path doesn't exist.

**Requirements:**
- `pymupdf` (fitz)
- `Pillow` (PIL)

**Examples:**
```python
from pathlib import Path
from pdfx import apply_image_filter_to_pdf

# Enhance contrast
apply_image_filter_to_pdf(
    Path("scan.pdf"),
    Path("enhanced.pdf"),
    filter_name="enhance",
    strength=2.0
)

# Convert to black and white
apply_image_filter_to_pdf(
    Path("scan.pdf"),
    Path("bw.pdf"),
    filter_name="bw",
    strength=150  # threshold
)

# Auto-enhance
apply_image_filter_to_pdf(
    Path("faded.pdf"),
    Path("fixed.pdf"),
    filter_name="auto"
)
```

---

### create_scanned_pdf

```python
def create_scanned_pdf(
    input_path: Path,
    output_path: Path,
    scan_quality: str = "medium",
    add_noise: bool = True,
    slight_skew: bool = False
) -> int
```

Create a scanned-looking copy of a PDF with realistic scan effects.

**Description:**
Transforms a digital PDF to look like it was physically scanned, complete with realistic artifacts like noise, slight skew, and quality degradation. Perfect for creating authentic-looking scanned documents from digital originals.

**Args:**
- `input_path` (Path): Path to input PDF file.
- `output_path` (Path): Path to output PDF file.
- `scan_quality` (str, optional): Quality level. Options:
  - `'low'`: 100 DPI, noticeable artifacts (noise level 15)
  - `'medium'`: 150 DPI, balanced quality (noise level 8) - **Default**
  - `'high'`: 200 DPI, minimal artifacts (noise level 5)
- `add_noise` (bool, optional): Add subtle noise/grain to simulate scanner artifacts. Default: True.
- `slight_skew` (bool, optional): Add very slight rotation (0.2-0.5°) to simulate imperfect scanning. Default: False.

**Returns:**
- `int`: Number of pages written.

**Raises:**
- `ImportError`: If pymupdf, Pillow, or numpy is not installed.
- `FileNotFoundError`: If input_path doesn't exist.

**Requirements:**
- `pymupdf` (fitz)
- `Pillow` (PIL)
- `numpy`

**Quality Settings:**
| Quality | DPI | Contrast | Brightness | Noise Level |
|---------|-----|----------|------------|-------------|
| low     | 100 | 1.1      | 0.95       | 15          |
| medium  | 150 | 1.05     | 0.98       | 8           |
| high    | 200 | 1.02     | 0.99       | 5           |

**Examples:**
```python
from pathlib import Path
from pdfx import create_scanned_pdf

# Create realistic scanned copy
create_scanned_pdf(
    Path("digital.pdf"),
    Path("scanned.pdf"),
    scan_quality="medium",
    add_noise=True,
    slight_skew=True
)

# High quality scan
create_scanned_pdf(
    Path("digital.pdf"),
    Path("clean_scan.pdf"),
    scan_quality="high",
    add_noise=False,
    slight_skew=False
)
```

**Effects Applied:**
1. Resolution adjustment based on quality setting
2. Optional rotation for skew effect (0.2-0.5 degrees)
3. Contrast and brightness adjustment
4. Gaussian noise addition (if enabled)
5. Slight blur to simulate scanner optics
6. Sharpening to compensate for blur

---

### auto_enhance_pdf

```python
def auto_enhance_pdf(
    input_path: Path,
    output_path: Path,
    auto_mode: str = "smart"
) -> int
```

Automatically enhance a PDF with smart defaults for scanned documents.

**Description:**
Applies automatic enhancements to improve the readability and appearance of PDF documents, especially useful for scanned or low-quality PDFs. Uses intelligent image processing to boost contrast and clarity.

**Args:**
- `input_path` (Path): Path to input PDF file.
- `output_path` (Path): Path to output PDF file.
- `auto_mode` (str, optional): Enhancement mode. Options:
  - `'smart'`: Contrast enhancement (1.5x) + autocontrast - **Recommended, Default**
  - `'contrast'`: Moderate contrast enhancement (1.5x)
  - `'strong'`: Strong contrast enhancement (2.0x) for heavily faded documents
  - `'auto'`: Autocontrast only

**Returns:**
- `int`: Number of pages processed.

**Raises:**
- `ImportError`: If pymupdf or Pillow is not installed.
- `ValueError`: If auto_mode is unknown.
- `FileNotFoundError`: If input_path doesn't exist.

**Requirements:**
- `pymupdf` (fitz)
- `Pillow` (PIL)

**Mode Details:**
| Mode     | Enhancement Applied                    | Best For                          |
|----------|----------------------------------------|-----------------------------------|
| smart    | 1.5x contrast + autocontrast          | Most scanned documents (default)  |
| contrast | 1.5x contrast only                    | Documents needing moderate boost  |
| strong   | 2.0x contrast only                    | Heavily faded or poor scans       |
| auto     | Autocontrast only                     | Already decent quality documents  |

**Examples:**
```python
from pathlib import Path
from pdfx import auto_enhance_pdf

# Smart enhancement (recommended)
auto_enhance_pdf(
    Path("scanned.pdf"),
    Path("enhanced.pdf"),
    auto_mode="smart"
)

# Strong enhancement for faded documents
auto_enhance_pdf(
    Path("old_scan.pdf"),
    Path("restored.pdf"),
    auto_mode="strong"
)

# Gentle auto-contrast only
auto_enhance_pdf(
    Path("decent.pdf"),
    Path("improved.pdf"),
    auto_mode="auto"
)
```

**Technical Details:**
- Pages are rendered at 2x resolution (matrix 2.0) for better quality
- Images are processed in RGB color space
- Results are saved as PNG-embedded PDF pages

---

## Image to PDF Conversion

### images_to_pdf

```python
def images_to_pdf(
    image_paths: List[Path],
    output_path: Path,
    enhance_type: Optional[str] = None,
    enhance_strength: float = 1.5
) -> int
```

Convert one or more image files to a PDF with optional color enhancement.

**Description:**
Creates a PDF from multiple images, with each image becoming one page. Supports various image formats and optional visual enhancements.

**Args:**
- `image_paths` (List[Path]): List of image file paths to convert.
- `output_path` (Path): Path where the PDF will be saved.
- `enhance_type` (str, optional): Enhancement to apply. Options:
  - `'enhance'`: Increase contrast (strength = factor, 1.0 = no change)
  - `'brightness'`: Adjust brightness (strength = factor, 1.0 = no change)
  - `'color'`: Adjust color saturation (strength = factor, 1.0 = no change)
  - `'sharpness'`: Adjust sharpness (strength = factor, 1.0 = no change)
  - `'auto'`: Apply autocontrast
  - `None`: No enhancement (default)
- `enhance_strength` (float, optional): Enhancement strength factor. Default: 1.5.

**Returns:**
- `int`: Number of images successfully added to the PDF.

**Raises:**
- `ImportError`: If pymupdf or Pillow is not installed.
- `ValueError`: If no image files are provided or none were successfully processed.
- `ValueError`: If enhance_type is unknown.

**Requirements:**
- `pymupdf` (fitz)
- `Pillow` (PIL)

**Supported Formats:**
JPEG, PNG, BMP, GIF, TIFF, WEBP, and any other format Pillow supports.

**Examples:**
```python
from pathlib import Path
from pdfx import images_to_pdf

# Basic conversion
images = [Path("page1.jpg"), Path("page2.jpg"), Path("page3.jpg")]
count = images_to_pdf(images, Path("output.pdf"))
print(f"Added {count} images")

# With contrast enhancement
images_to_pdf(
    [Path("scan1.png"), Path("scan2.png")],
    Path("enhanced.pdf"),
    enhance_type="enhance",
    enhance_strength=2.0
)

# Increase brightness
images_to_pdf(
    [Path("dark.jpg")],
    Path("brightened.pdf"),
    enhance_type="brightness",
    enhance_strength=1.3
)

# Auto-enhance
images_to_pdf(
    [Path("photo.jpg")],
    Path("auto.pdf"),
    enhance_type="auto"
)
```

**Note:**
- Images with RGBA or other non-RGB modes are automatically converted to RGB
- Output directory is created automatically if it doesn't exist
- Failed images are skipped with a warning, processing continues
- Each image becomes one PDF page with matching dimensions

---

### images_from_dir_to_pdf

```python
def images_from_dir_to_pdf(
    image_dir: Path,
    output_path: Path,
    enhance_type: Optional[str] = None,
    enhance_strength: float = 1.5
) -> int
```

Convert all image files from a directory into a single PDF with optional color enhancement.

**Description:**
Scans a directory for all image files, sorts them by name, and creates a PDF with one page per image. Convenient for batch converting folders of scans or photos.

**Args:**
- `image_dir` (Path): Path to directory containing image files.
- `output_path` (Path): Path where the PDF will be saved.
- `enhance_type` (str, optional): Enhancement to apply. Same options as `images_to_pdf`:
  - `'enhance'`, `'brightness'`, `'color'`, `'sharpness'`, `'auto'`, or `None`
- `enhance_strength` (float, optional): Enhancement strength factor. Default: 1.5.

**Returns:**
- `int`: Number of images added to the PDF.

**Raises:**
- `ImportError`: If pymupdf or Pillow is not installed.
- `FileNotFoundError`: If image_dir doesn't exist.
- `ValueError`: If no image files found in the directory.
- `ValueError`: If enhance_type is unknown.

**Requirements:**
- `pymupdf` (fitz)
- `Pillow` (PIL)

**Supported Extensions:**
`.jpg`, `.jpeg`, `.png`, `.bmp`, `.gif`, `.tiff`, `.tif`, `.webp`

**Examples:**
```python
from pathlib import Path
from pdfx import images_from_dir_to_pdf

# Convert all images in a directory
count = images_from_dir_to_pdf(
    Path("scans/"),
    Path("output.pdf")
)
print(f"Converted {count} images")

# With enhancement
images_from_dir_to_pdf(
    Path("photos/"),
    Path("album.pdf"),
    enhance_type="enhance",
    enhance_strength=1.8
)
```

**Note:**
- Images are processed in sorted alphabetical order
- Only files with recognized image extensions are included
- Case-insensitive extension matching

---

## OCR

### ocr_make_searchable

```python
def ocr_make_searchable(
    input_path: Path,
    output_path: Path,
    lang: str = "eng"
) -> int
```

Make a PDF searchable using OCR (Optical Character Recognition).

**Description:**
Performs OCR on a PDF to extract text and create a searchable version. Useful for scanned documents or PDFs with text embedded as images.

**Args:**
- `input_path` (Path): Path to input PDF file.
- `output_path` (Path): Path to output PDF file.
- `lang` (str, optional): Tesseract language code(s). Default: `"eng"` (English).
  - Single language: `"eng"`, `"fra"`, `"deu"`, `"spa"`, etc.
  - Multiple languages: `"eng+fra"`, `"eng+spa"`, etc.

**Returns:**
- `int`: Number of pages processed.

**Raises:**
- `ImportError`: If pymupdf, pytesseract, or pdf2image is not installed.
- `FileNotFoundError`: If input_path doesn't exist.
- `TesseractNotFoundError`: If Tesseract OCR is not installed on the system.

**Requirements:**
- `pymupdf` (fitz)
- `pytesseract`
- `pdf2image`
- **Tesseract OCR** (system installation required)

**Tesseract Installation:**
- **macOS**: `brew install tesseract tesseract-lang`
- **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr tesseract-ocr-[lang]`
- **Windows**: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

**Supported Languages:**
Use Tesseract language codes. Common ones:
- `eng` - English
- `fra` - French
- `deu` - German
- `spa` - Spanish
- `ita` - Italian
- `por` - Portuguese
- `rus` - Russian
- `chi_sim` - Simplified Chinese
- `chi_tra` - Traditional Chinese
- `jpn` - Japanese
- `kor` - Korean

**Examples:**
```python
from pathlib import Path
from pdfx import ocr_make_searchable

# English OCR
pages = ocr_make_searchable(
    Path("scanned.pdf"),
    Path("searchable.pdf"),
    lang="eng"
)

# Multi-language OCR (English + French)
ocr_make_searchable(
    Path("bilingual.pdf"),
    Path("searchable_bilingual.pdf"),
    lang="eng+fra"
)

# Spanish OCR
ocr_make_searchable(
    Path("documento.pdf"),
    Path("buscable.pdf"),
    lang="spa"
)
```

**Note:**
- OCR processing can be slow for large documents
- Quality of results depends on image quality and Tesseract configuration
- Output PDF will have searchable text layer overlaid on original images

---

## PDF Management

### merge_pdfs

```python
def merge_pdfs(input_dir: Path, output_path: Path) -> None
```

Merge all PDFs in a directory into a single file.

**Description:**
Combines all PDF files from a directory into one PDF, in alphabetical order by filename. Useful for consolidating multiple documents or scanned pages.

**Args:**
- `input_dir` (Path): Path to directory containing PDF files to merge.
- `output_path` (Path): Path where the merged PDF will be saved.

**Returns:**
- `None`

**Raises:**
- `ImportError`: If pypdf is not installed.
- `ValueError`: If no PDF files found in input_dir.
- `FileNotFoundError`: If input_dir doesn't exist.

**Requirements:**
- `pypdf` (>= 3.0.0)

**Examples:**
```python
from pathlib import Path
from pdfx import merge_pdfs

# Merge all PDFs in a directory
merge_pdfs(
    Path("invoices/"),
    Path("all_invoices.pdf")
)

# Merge scanned pages
merge_pdfs(
    Path("scans/"),
    Path("complete_document.pdf")
)
```

**Note:**
- Files are processed in sorted alphabetical order
- Only files with `.pdf` extension are included
- All pages from each PDF are included
- Uses `PdfWriter` for compatibility with pypdf >= 3.0.0

---

### split_pdf

```python
def split_pdf(
    input_path: Path,
    output_dir: Path,
    page_range: Optional[str] = None
) -> None
```

Split a PDF into individual pages or extract a specified range.

**Description:**
Extracts pages from a PDF into separate files. Can split all pages or just a specific range.

**Args:**
- `input_path` (Path): Path to input PDF file to split.
- `output_dir` (Path): Directory where split PDFs will be saved.
- `page_range` (str, optional): Page range to extract (e.g., `"1-3,5,7-9"`).
  - If `None`, all pages are split into individual files (default).
  - Supports individual pages and ranges, comma-separated.

**Returns:**
- `None`

**Raises:**
- `ImportError`: If pypdf is not installed.
- `FileNotFoundError`: If input_path doesn't exist.
- `ValueError`: If page_range format is invalid.

**Requirements:**
- `pypdf` (>= 3.0.0)

**Output Naming:**
- Files are named: `{original_name}_page_{page_number}.pdf`
- Example: `document_page_1.pdf`, `document_page_2.pdf`, etc.

**Examples:**
```python
from pathlib import Path
from pdfx import split_pdf

# Split all pages
split_pdf(
    Path("document.pdf"),
    Path("pages/")
)
# Creates: pages/document_page_1.pdf, pages/document_page_2.pdf, ...

# Extract specific pages
split_pdf(
    Path("document.pdf"),
    Path("selected_pages/"),
    page_range="1-3,5"
)
# Creates: selected_pages/document_page_1.pdf, ..., document_page_3.pdf, document_page_5.pdf

# Extract a range
split_pdf(
    Path("book.pdf"),
    Path("chapter/"),
    page_range="10-20"
)
# Creates: chapter/book_page_10.pdf through chapter/book_page_20.pdf
```

**Note:**
- Output directory is created automatically if it doesn't exist
- Page numbers are 1-based (first page is 1, not 0)
- Invalid page numbers in range are silently skipped
- Files are named with original filename + page number

---

## Internal Helper Functions

### _rgb_from_int

```python
def _rgb_from_int(color_int: int) -> Tuple[int, int, int]
```

**Description:**
Convert PyMuPDF color integer to RGB tuple. PyMuPDF represents colors as 24-bit integers where red is in bits 16-23, green in bits 8-15, and blue in bits 0-7.

**Args:**
- `color_int` (int): Integer color value from PyMuPDF (0x00000000 to 0x00FFFFFF).

**Returns:**
- `Tuple[int, int, int]`: RGB tuple with values 0-255.

**Examples:**
```python
_rgb_from_int(0xFF0000)  # Returns: (255, 0, 0) - Red
_rgb_from_int(0x00FF00)  # Returns: (0, 255, 0) - Green
_rgb_from_int(0x0000FF)  # Returns: (0, 0, 255) - Blue
```

---

### _color_distance

```python
def _color_distance(c1: Tuple[int, int, int], c2: Tuple[int, int, int]) -> float
```

**Description:**
Calculate Euclidean distance between two RGB colors in 3D color space. Lower values indicate more similar colors.

**Args:**
- `c1` (Tuple[int, int, int]): First RGB color, values 0-255.
- `c2` (Tuple[int, int, int]): Second RGB color, values 0-255.

**Returns:**
- `float`: Euclidean distance. Range: 0 (identical) to ~441 (opposite extremes).

**Examples:**
```python
_color_distance((255, 0, 0), (255, 0, 0))      # Returns: 0.0 (identical)
_color_distance((0, 0, 0), (255, 255, 255))    # Returns: 441.67 (black to white)
_color_distance((255, 0, 0), (250, 0, 0))      # Returns: 5.0 (very similar reds)
```

---

## Installation

### Basic Installation
```bash
pip install pdfx-tool
```

### Full Installation (All Features)
```bash
pip install pdfx-tool[full]
```

This installs all optional dependencies:
- `pymupdf` - PDF manipulation and rendering
- `Pillow` - Image processing
- `pytesseract` - OCR interface
- `pdf2image` - PDF to image conversion
- `numpy` - Numerical operations

### System Requirements for OCR
```bash
# macOS
brew install tesseract tesseract-lang

# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-all

# Windows
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

---

## Quick Start Examples

### Color-Based PDF Filtering
```python
from pathlib import Path
from pdfx import filter_pdf_by_color, parse_color_string

# Extract all red text
red = parse_color_string("red")
filter_pdf_by_color(
    Path("document.pdf"),
    Path("red_only.pdf"),
    red,
    tolerance=30
)
```

### Create Scanned-Looking PDF
```python
from pathlib import Path
from pdfx import create_scanned_pdf

create_scanned_pdf(
    Path("digital.pdf"),
    Path("scanned.pdf"),
    scan_quality="medium",
    add_noise=True,
    slight_skew=True
)
```

### Enhance Scanned Document
```python
from pathlib import Path
from pdfx import auto_enhance_pdf

auto_enhance_pdf(
    Path("old_scan.pdf"),
    Path("enhanced.pdf"),
    auto_mode="smart"
)
```

### Convert Images to PDF
```python
from pathlib import Path
from pdfx import images_from_dir_to_pdf

images_from_dir_to_pdf(
    Path("photos/"),
    Path("album.pdf"),
    enhance_type="enhance",
    enhance_strength=1.5
)
```

### PDF Management
```python
from pathlib import Path
from pdfx import merge_pdfs, split_pdf

# Merge PDFs
merge_pdfs(Path("invoices/"), Path("all_invoices.pdf"))

# Split PDF
split_pdf(Path("book.pdf"), Path("chapters/"), page_range="1-10")
```

---

## Error Handling

All functions may raise the following exceptions:

- `ImportError`: When required dependencies are not installed
- `FileNotFoundError`: When input files/directories don't exist
- `ValueError`: When invalid arguments are provided
- `PermissionError`: When lacking file system permissions

**Example:**
```python
from pathlib import Path
from pdfx import filter_pdf_by_color

try:
    filter_pdf_by_color(
        Path("document.pdf"),
        Path("output.pdf"),
        (255, 0, 0),
        tolerance=50
    )
except ImportError as e:
    print(f"Missing dependency: {e}")
except FileNotFoundError:
    print("Input file not found")
except ValueError as e:
    print(f"Invalid argument: {e}")
```

---

## Version Information

**Current Version:** 0.2.0

**Changelog:**
- **0.2.0**
  - Added `parse_page_ranges()` function
  - Added `dump_colors()` diagnostic function
  - Added `auto_enhance_pdf()` with 4 enhancement modes
  - Added `images_to_pdf()` and `images_from_dir_to_pdf()`
  - Added helper functions `_rgb_from_int()` and `_color_distance()`
  - Enhanced CLI with new options
  
- **0.1.0**
  - Initial release
  - Named color support (20 colors)
  - Fixed PdfMerger compatibility (pypdf >= 3.0.0)
  - Added `create_scanned_pdf()` function

---

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please see [DEVELOPMENT.md](DEVELOPMENT.md) for development setup and guidelines.

## Support

For issues, questions, or feature requests, please visit:
- GitHub: https://github.com/jonamadk/PDF-X
- PyPI: https://pypi.org/project/pdfx-tool/
