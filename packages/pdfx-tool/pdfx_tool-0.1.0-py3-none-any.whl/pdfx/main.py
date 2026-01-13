"""
Main module for PdfX - PDF manipulation functions.

This module contains the core functionality for PDF operations including
merging, splitting, filtering by color, image filtering, recoloring, and OCR.
"""

from pathlib import Path
from typing import Tuple, Optional


def parse_color_string(color_str: str) -> Tuple[int, int, int]:
    """
    Parse a color string to RGB tuple.

    Supports:
    - Hex format: '#RRGGBB' (e.g., '#FF0000')
    - RGB format: 'R,G,B' (e.g., '255,0,0')
    - Named colors: 'red', 'blue', 'green', etc.

    Args:
        color_str: Color string in hex, RGB, or named color format

    Returns:
        Tuple of (R, G, B) values (0-255)

    Examples:
        >>> parse_color_string("#FF0000")
        (255, 0, 0)
        >>> parse_color_string("255,0,128")
        (255, 0, 128)
        >>> parse_color_string("red")
        (255, 0, 0)
    """
    # Common color names mapping
    COLOR_NAMES = {
        'black': (0, 0, 0),
        'white': (255, 255, 255),
        'red': (255, 0, 0),
        'green': (0, 128, 0),
        'blue': (0, 0, 255),
        'yellow': (255, 255, 0),
        'cyan': (0, 255, 255),
        'magenta': (255, 0, 255),
        'orange': (255, 165, 0),
        'purple': (128, 0, 128),
        'pink': (255, 192, 203),
        'brown': (165, 42, 42),
        'gray': (128, 128, 128),
        'grey': (128, 128, 128),
        'lime': (0, 255, 0),
        'navy': (0, 0, 128),
        'teal': (0, 128, 128),
        'silver': (192, 192, 192),
        'maroon': (128, 0, 0),
        'olive': (128, 128, 0),
    }

    color_str = color_str.strip().lower()

    # Check for named color first
    if color_str in COLOR_NAMES:
        return COLOR_NAMES[color_str]

    # Restore original case for error messages
    color_str_original = color_str
    color_str = color_str_original.strip()

    if color_str.startswith('#'):
        # Hex format: #RRGGBB
        hex_str = color_str[1:]
        if len(hex_str) != 6:
            raise ValueError(f"Invalid hex color format: {color_str}")
        r = int(hex_str[0:2], 16)
        g = int(hex_str[2:4], 16)
        b = int(hex_str[4:6], 16)
        return (r, g, b)
    elif ',' in color_str:
        # RGB format: R,G,B
        parts = color_str.split(',')
        if len(parts) != 3:
            raise ValueError(f"Invalid RGB color format: {color_str}")
        r, g, b = [int(p.strip()) for p in parts]
        if not all(0 <= val <= 255 for val in (r, g, b)):
            raise ValueError(f"RGB values must be 0-255: {color_str}")
        return (r, g, b)
    else:
        available_colors = ', '.join(sorted(COLOR_NAMES.keys())[:10]) + ', ...'
        raise ValueError(
            f"Color must be in format '#RRGGBB', 'R,G,B', or a named color.\n"
            f"Got: '{color_str_original}'\n"
            f"Available named colors: {available_colors}"
        )


def filter_pdf_by_color(
    input_path: Path,
    output_path: Path,
    target_color: Tuple[int, int, int],
    tolerance: float = 0.0
) -> int:
    """
    Filter a PDF by text color, keeping only text matching the target color.

    Args:
        input_path: Path to input PDF file
        output_path: Path to output PDF file
        target_color: RGB tuple (0-255) of color to filter
        tolerance: Color distance tolerance for fuzzy matching

    Returns:
        Number of pages written

    Requires:
        pymupdf (fitz)
    """
    try:
        import fitz
    except ImportError:
        raise ImportError(
            "filter_pdf_by_color requires pymupdf. Install with: pip install pymupdf")

    doc = fitz.open(input_path)
    out_doc = fitz.open()

    target_r, target_g, target_b = target_color
    target_fitz = (target_r / 255.0, target_g / 255.0, target_b / 255.0)

    pages_written = 0
    for page_num in range(len(doc)):
        page = doc[page_num]
        new_page = out_doc.new_page(
            width=page.rect.width, height=page.rect.height)

        # Extract text with color information
        blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)

        for block in blocks.get("blocks", []):
            if block.get("type") == 0:  # text block
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        color = span.get("color")
                        if color is not None:
                            # Convert integer color to RGB
                            r = (color >> 16) & 0xFF
                            g = (color >> 8) & 0xFF
                            b = color & 0xFF

                            # Calculate color distance
                            distance = ((r - target_r) ** 2 + (g - target_g)
                                        ** 2 + (b - target_b) ** 2) ** 0.5

                            if distance <= tolerance:
                                # Keep this text span
                                text = span.get("text", "")
                                origin = span.get("origin")
                                fontname = span.get("font", "helv")
                                fontsize = span.get("size", 12)

                                if origin and text:
                                    new_page.insert_text(
                                        origin,
                                        text,
                                        fontname=fontname,
                                        fontsize=fontsize,
                                        color=(r / 255.0, g / 255.0, b / 255.0)
                                    )

        pages_written += 1

    out_doc.save(output_path)
    out_doc.close()
    doc.close()

    return pages_written


def apply_image_filter_to_pdf(
    input_path: Path,
    output_path: Path,
    filter_name: str,
    strength: float = 1.5
) -> int:
    """
    Apply an image-level filter to each page of a PDF.

    Args:
        input_path: Path to input PDF file
        output_path: Path to output PDF file
        filter_name: Filter to apply ('enhance', 'bw', 'grayscale', 'invert', 'auto')
        strength: Filter strength/threshold (meaning depends on filter)

    Returns:
        Number of pages written

    Requires:
        pymupdf (fitz), Pillow (PIL)
    """
    try:
        import fitz
        from PIL import Image, ImageEnhance, ImageOps
    except ImportError:
        raise ImportError("apply_image_filter_to_pdf requires pymupdf and Pillow. "
                          "Install with: pip install pymupdf Pillow")

    doc = fitz.open(input_path)
    out_doc = fitz.open()

    pages_written = 0
    for page_num in range(len(doc)):
        page = doc[page_num]

        # Render page to image
        pix = page.get_pixmap(dpi=150)
        img_data = pix.tobytes("png")

        # Load with PIL
        from io import BytesIO
        img = Image.open(BytesIO(img_data))

        # Apply filter
        if filter_name == "enhance":
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(strength)
        elif filter_name == "bw":
            img = img.convert("L")
            threshold = int(strength) if strength > 1 else 128
            img = img.point(lambda x: 255 if x > threshold else 0, mode='1')
        elif filter_name == "grayscale":
            img = img.convert("L")
        elif filter_name == "invert":
            img = ImageOps.invert(img.convert("RGB"))
        elif filter_name == "auto":
            img = ImageOps.autocontrast(img)
        else:
            raise ValueError(f"Unknown filter: {filter_name}")

        # Convert back to PDF
        img_bytes = BytesIO()
        img.save(img_bytes, format="PDF")
        img_bytes.seek(0)

        img_doc = fitz.open("pdf", img_bytes.read())
        new_page = out_doc.new_page(
            width=page.rect.width, height=page.rect.height)
        new_page.show_pdf_page(new_page.rect, img_doc, 0)
        img_doc.close()

        pages_written += 1

    out_doc.save(output_path)
    out_doc.close()
    doc.close()

    return pages_written


def recolor_pdf_text(
    input_path: Path,
    output_path: Path,
    target_color: Tuple[int, int, int],
    new_color: Tuple[int, int, int],
    tolerance: float = 0.0
) -> int:
    """
    Recolor text in a PDF that matches the target color.

    Args:
        input_path: Path to input PDF file
        output_path: Path to output PDF file
        target_color: RGB tuple (0-255) of color to match
        new_color: RGB tuple (0-255) of replacement color
        tolerance: Color distance tolerance for fuzzy matching

    Returns:
        Number of pages processed

    Requires:
        pymupdf (fitz)
    """
    try:
        import fitz
    except ImportError:
        raise ImportError(
            "recolor_pdf_text requires pymupdf. Install with: pip install pymupdf")

    doc = fitz.open(input_path)
    out_doc = fitz.open()

    target_r, target_g, target_b = target_color
    new_r, new_g, new_b = new_color

    pages_processed = 0
    for page_num in range(len(doc)):
        page = doc[page_num]
        new_page = out_doc.new_page(
            width=page.rect.width, height=page.rect.height)

        # Copy original page content
        new_page.show_pdf_page(new_page.rect, doc, page_num)

        # Extract and recolor matching text
        blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)

        for block in blocks.get("blocks", []):
            if block.get("type") == 0:  # text block
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        color = span.get("color")
                        if color is not None:
                            r = (color >> 16) & 0xFF
                            g = (color >> 8) & 0xFF
                            b = color & 0xFF

                            distance = ((r - target_r) ** 2 + (g - target_g)
                                        ** 2 + (b - target_b) ** 2) ** 0.5

                            if distance <= tolerance:
                                text = span.get("text", "")
                                origin = span.get("origin")
                                fontname = span.get("font", "helv")
                                fontsize = span.get("size", 12)

                                if origin and text:
                                    new_page.insert_text(
                                        origin,
                                        text,
                                        fontname=fontname,
                                        fontsize=fontsize,
                                        color=(new_r / 255.0, new_g /
                                               255.0, new_b / 255.0)
                                    )

        pages_processed += 1

    out_doc.save(output_path)
    out_doc.close()
    doc.close()

    return pages_processed


def ocr_make_searchable(
    input_path: Path,
    output_path: Path,
    lang: str = "eng"
) -> int:
    """
    Make a PDF searchable using OCR.

    Args:
        input_path: Path to input PDF file
        output_path: Path to output PDF file
        lang: Tesseract language code(s) (e.g., 'eng', 'fra', 'eng+fra')

    Returns:
        Number of pages processed

    Requires:
        pymupdf (fitz), pytesseract, pdf2image, Tesseract OCR installed
    """
    try:
        import fitz
        import pytesseract
        from pdf2image import convert_from_path
    except ImportError:
        raise ImportError("ocr_make_searchable requires pymupdf, pytesseract, and pdf2image. "
                          "Install with: pip install pymupdf pytesseract pdf2image")

    # Convert PDF to images
    images = convert_from_path(input_path)

    out_doc = fitz.open()
    pages_processed = 0

    for img in images:
        # Perform OCR
        ocr_data = pytesseract.image_to_pdf_or_hocr(
            img, extension='pdf', lang=lang)

        # Add to output document
        ocr_doc = fitz.open("pdf", ocr_data)
        new_page = out_doc.new_page(
            width=ocr_doc[0].rect.width, height=ocr_doc[0].rect.height)
        new_page.show_pdf_page(new_page.rect, ocr_doc, 0)
        ocr_doc.close()

        pages_processed += 1

    out_doc.save(output_path)
    out_doc.close()

    return pages_processed


# Placeholder functions for merge/split functionality
# These would contain the actual implementation based on your requirements

def merge_pdfs(input_dir: Path, output_path: Path) -> None:
    """Merge all PDFs in a directory into a single file."""
    try:
        from pypdf import PdfMerger
    except ImportError:
        raise ImportError(
            "merge_pdfs requires pypdf. Install with: pip install pypdf")

    merger = PdfMerger()
    pdf_files = sorted(input_dir.glob("*.pdf"))

    if not pdf_files:
        raise ValueError(f"No PDF files found in {input_dir}")

    for pdf_file in pdf_files:
        merger.append(str(pdf_file))

    merger.write(str(output_path))
    merger.close()


def split_pdf(input_path: Path, output_dir: Path, page_range: Optional[str] = None) -> None:
    """Split a PDF into individual pages or a specified range."""
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        raise ImportError(
            "split_pdf requires pypdf. Install with: pip install pypdf")

    output_dir.mkdir(parents=True, exist_ok=True)
    reader = PdfReader(input_path)

    if page_range:
        # Parse page range (e.g., "1-3,5")
        pages_to_extract = []
        for part in page_range.split(','):
            if '-' in part:
                start, end = part.split('-')
                pages_to_extract.extend(range(int(start) - 1, int(end)))
            else:
                pages_to_extract.append(int(part) - 1)
    else:
        pages_to_extract = range(len(reader.pages))

    for page_num in pages_to_extract:
        if 0 <= page_num < len(reader.pages):
            writer = PdfWriter()
            writer.add_page(reader.pages[page_num])

            output_file = output_dir / \
                f"{input_path.stem}_page_{page_num + 1}.pdf"
            with open(output_file, 'wb') as f:
                writer.write(f)
