"""
Main module for PdfX - PDF manipulation functions.

This module contains the core functionality for PDF operations including
merging, splitting, filtering by color, image filtering, recoloring, and OCR.
"""

from pathlib import Path
from typing import Tuple, Optional, List
import os
import tempfile


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


def parse_page_ranges(range_str: Optional[str]) -> Optional[List[int]]:
    """Parse a page-range string like "1-3,5" into a list of 1-based page numbers.

    Returns None if range_str is None or empty.

    Examples:
        >>> parse_page_ranges("1-3,5")
        [1, 2, 3, 5]
        >>> parse_page_ranges("2,4-6")
        [2, 4, 5, 6]
    """
    if not range_str:
        return None
    pages: List[int] = []
    for part in range_str.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            lo_str, hi_str = part.split("-", 1)
            try:
                lo = int(lo_str)
                hi = int(hi_str)
            except ValueError:
                raise ValueError(f"Invalid range component: {part}")
            if lo > hi:
                raise ValueError(f"Invalid range (start > end): {part}")
            pages.extend(range(lo, hi + 1))
        else:
            try:
                pages.append(int(part))
            except ValueError:
                raise ValueError(f"Invalid page number: {part}")
    # dedupe and sort
    return sorted(dict.fromkeys(pages))


def _rgb_from_int(color_int: int) -> Tuple[int, int, int]:
    """Convert PyMuPDF color int to (r,g,b)."""
    r = (color_int >> 16) & 255
    g = (color_int >> 8) & 255
    b = color_int & 255
    return (r, g, b)


def _color_distance(c1: Tuple[int, int, int], c2: Tuple[int, int, int]) -> float:
    """Calculate Euclidean distance between two RGB colors."""
    return ((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2 + (c1[2]-c2[2])**2) ** 0.5


def dump_colors(input_path: Path, max_samples: int = 5) -> None:
    """Dump unique text span colors found in a PDF for diagnosis.

    Prints the integer color value, converted RGB, appearance count, and a few text samples.

    Args:
        input_path: Path to PDF file to analyze
        max_samples: Maximum number of text samples to show per color

    Requires:
        pymupdf (fitz)
    """
    try:
        import fitz
    except ImportError:
        raise ImportError(
            "dump_colors requires pymupdf. Install with: pip install pymupdf")

    doc = fitz.open(str(input_path))
    colors = {}
    for page in doc:
        textdict = page.get_text("dict")
        for block in textdict.get("blocks", []):
            if "lines" not in block:
                continue
            for line in block["lines"]:
                for span in line.get("spans", []):
                    color_int = span.get("color")
                    if color_int is None:
                        continue
                    entry = colors.setdefault(
                        color_int, {"rgb": _rgb_from_int(color_int), "count": 0, "samples": []})
                    entry["count"] += 1
                    txt = span.get("text", "").strip()
                    if txt and len(entry["samples"]) < max_samples:
                        entry["samples"].append(txt)
    doc.close()

    if not colors:
        print("No colored text spans found. Text may be embedded as images or colors may not be available via text spans.")
        return

    for ci, info in sorted(colors.items(), key=lambda kv: -kv[1]["count"]):
        print(f"Color int={ci} -> RGB={info['rgb']} (count={info['count']})")
        for s in info["samples"]:
            print(f"  sample: {s}")


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


def create_scanned_pdf(
    input_path: Path,
    output_path: Path,
    scan_quality: str = "medium",
    add_noise: bool = True,
    slight_skew: bool = False
) -> int:
    """
    Create a scanned-looking copy of a PDF with realistic scan effects.

    Args:
        input_path: Path to input PDF file
        output_path: Path to output PDF file
        scan_quality: Quality level ('low', 'medium', 'high')
        add_noise: Add subtle noise/grain to simulate scanner artifacts
        slight_skew: Add very slight rotation to simulate imperfect scanning

    Returns:
        Number of pages written

    Requires:
        pymupdf (fitz), Pillow (PIL), numpy
    """
    try:
        import fitz
        from PIL import Image, ImageEnhance, ImageFilter
        import numpy as np
    except ImportError:
        raise ImportError("create_scanned_pdf requires pymupdf, Pillow, and numpy. "
                          "Install with: pip install pymupdf Pillow numpy")

    # Quality settings
    quality_settings = {
        'low': {'dpi': 100, 'contrast': 1.1, 'brightness': 0.95, 'noise_level': 15},
        'medium': {'dpi': 150, 'contrast': 1.05, 'brightness': 0.98, 'noise_level': 8},
        'high': {'dpi': 200, 'contrast': 1.02, 'brightness': 0.99, 'noise_level': 5},
    }

    settings = quality_settings.get(scan_quality, quality_settings['medium'])

    doc = fitz.open(input_path)
    out_doc = fitz.open()

    pages_written = 0
    for page_num in range(len(doc)):
        page = doc[page_num]

        # Render page to image at specified DPI
        pix = page.get_pixmap(dpi=settings['dpi'])
        img_data = pix.tobytes("png")

        # Load with PIL
        from io import BytesIO
        img = Image.open(BytesIO(img_data))

        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Apply slight rotation for skew effect (0.2-0.5 degrees)
        if slight_skew:
            import random
            angle = random.uniform(-0.5, 0.5)
            img = img.rotate(angle, fillcolor='white', expand=False)

        # Adjust contrast and brightness for scanned look
        if settings['contrast'] != 1.0:
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(settings['contrast'])

        if settings['brightness'] != 1.0:
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(settings['brightness'])

        # Add subtle noise/grain
        if add_noise:
            img_array = np.array(img)
            noise = np.random.normal(
                0, settings['noise_level'], img_array.shape)
            noisy_img = np.clip(img_array + noise, 0, 255).astype(np.uint8)
            img = Image.fromarray(noisy_img)

        # Slight blur to simulate scanner optics
        img = img.filter(ImageFilter.GaussianBlur(radius=0.3))

        # Subtle sharpening to compensate
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.1)

        # Convert back to PDF
        img_bytes = BytesIO()
        img.save(img_bytes, format="PDF", quality=95)
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


def auto_enhance_pdf(input_path: Path, output_path: Path, auto_mode: str = "smart") -> int:
    """Automatically enhance a PDF with smart defaults for scanned documents.

    Auto modes:
      - smart: Apply contrast enhancement followed by autocontrast for optimal results (recommended)
      - contrast: Apply moderate contrast enhancement (1.5x)
      - strong: Apply strong contrast enhancement (2.0x) for heavily faded documents
      - auto: Apply autocontrast only

    Returns the number of pages processed.

    Requires:
        pymupdf (fitz), Pillow (PIL)
    """
    try:
        import fitz
        from PIL import Image, ImageEnhance, ImageOps
    except ImportError:
        raise ImportError(
            "auto_enhance_pdf requires pymupdf and Pillow. "
            "Install with: pip install pymupdf Pillow")

    doc = fitz.open(str(input_path))
    out = fitz.open()
    pages_written = 0

    for page in doc:
        # render at higher resolution for better quality
        mat = fitz.Matrix(2.0, 2.0)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)

        # Apply enhancement based on selected mode
        if auto_mode == "smart":
            # Step 1: Apply contrast enhancement
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.5)
            # Step 2: Apply autocontrast for fine-tuning
            img = ImageOps.autocontrast(img)
        elif auto_mode == "contrast":
            # Moderate contrast enhancement
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.5)
        elif auto_mode == "strong":
            # Strong contrast enhancement for very faded documents
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(2.0)
        elif auto_mode == "auto":
            # Just autocontrast
            img = ImageOps.autocontrast(img)
        else:
            raise ValueError(f"Unknown auto-enhance mode: {auto_mode}")

        # write to a temporary PNG file and insert into a same-sized PDF page
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tf:
            tmpname = tf.name
            img.save(tmpname, format="PNG")

        rect = page.rect
        new_page = out.new_page(width=rect.width, height=rect.height)
        new_page.insert_image(rect, filename=tmpname)
        try:
            os.unlink(tmpname)
        except Exception:
            pass
        pages_written += 1

    out.save(str(output_path))
    out.close()
    doc.close()
    return pages_written


def images_to_pdf(image_paths: List[Path], output_path: Path, enhance_type: Optional[str] = None, enhance_strength: float = 1.5) -> int:
    """Convert one or more image files to a PDF with optional color enhancement.

    Supported image formats: JPEG, PNG, BMP, GIF, TIFF, etc. (anything Pillow supports).

    Enhancement types:
      - enhance: increase contrast (strength = factor, 1.0 = no change)
      - brightness: adjust brightness (strength = factor, 1.0 = no change)
      - color: adjust color saturation (strength = factor, 1.0 = no change)
      - sharpness: adjust sharpness (strength = factor, 1.0 = no change)
      - auto: apply autocontrast

    Returns the number of images written to PDF.

    Requires:
        pymupdf (fitz), Pillow (PIL)
    """
    try:
        import fitz
        from PIL import Image, ImageEnhance, ImageOps
    except ImportError:
        raise ImportError(
            "images_to_pdf requires pymupdf and Pillow. "
            "Install with: pip install pymupdf Pillow")

    if not image_paths:
        raise ValueError("No image files provided")

    # ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # open a new PDF document
    pdf_doc = fitz.open()
    images_added = 0

    for img_path in image_paths:
        if not img_path.exists():
            print(f"Warning: Image file not found: {img_path}")
            continue

        try:
            # open image with Pillow to get dimensions
            img = Image.open(str(img_path))
            # convert RGBA and other modes to RGB if needed
            if img.mode not in ("RGB", "L"):
                img = img.convert("RGB")

            # Apply color enhancement if requested
            if enhance_type:
                if enhance_type == "enhance":
                    # Increase contrast
                    enhancer = ImageEnhance.Contrast(img)
                    img = enhancer.enhance(enhance_strength)
                elif enhance_type == "brightness":
                    # Adjust brightness
                    enhancer = ImageEnhance.Brightness(img)
                    img = enhancer.enhance(enhance_strength)
                elif enhance_type == "color":
                    # Adjust color saturation
                    enhancer = ImageEnhance.Color(img)
                    img = enhancer.enhance(enhance_strength)
                elif enhance_type == "sharpness":
                    # Adjust sharpness
                    enhancer = ImageEnhance.Sharpness(img)
                    img = enhancer.enhance(enhance_strength)
                elif enhance_type == "auto":
                    # Apply autocontrast
                    img = ImageOps.autocontrast(img)
                else:
                    raise ValueError(
                        f"Unknown enhancement type: {enhance_type}")

            # get image dimensions
            width, height = img.size

            # create a new PDF page with the same dimensions (in points)
            page_width = width
            page_height = height
            new_page = pdf_doc.new_page(width=page_width, height=page_height)

            # save image to temporary file and insert into PDF
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tf:
                tmpname = tf.name
                img.save(tmpname, format="PNG")

            rect = new_page.rect
            new_page.insert_image(rect, filename=tmpname)
            try:
                os.unlink(tmpname)
            except Exception:
                pass

            images_added += 1
        except Exception as exc:
            print(f"Warning: Failed to process image {img_path}: {exc}")
            continue

    if images_added == 0:
        raise ValueError("No images were successfully processed")

    # save the PDF
    pdf_doc.save(str(output_path))
    pdf_doc.close()
    return images_added


def images_from_dir_to_pdf(image_dir: Path, output_path: Path, enhance_type: Optional[str] = None, enhance_strength: float = 1.5) -> int:
    """Convert all image files from a directory into a single PDF with optional color enhancement.

    Processes images in sorted order. Supported formats: JPEG, PNG, BMP, GIF, TIFF, etc.

    Enhancement types:
      - enhance: increase contrast (strength = factor, 1.0 = no change)
      - brightness: adjust brightness (strength = factor, 1.0 = no change)
      - color: adjust color saturation (strength = factor, 1.0 = no change)
      - sharpness: adjust sharpness (strength = factor, 1.0 = no change)
      - auto: apply autocontrast

    Returns the number of images added to the PDF.

    Requires:
        pymupdf (fitz), Pillow (PIL)
    """
    if not image_dir.exists():
        raise FileNotFoundError(f"Directory not found: {image_dir}")

    # find all image files with common extensions
    image_extensions = {".jpg", ".jpeg", ".png",
                        ".bmp", ".gif", ".tiff", ".tif", ".webp"}
    image_files = sorted(
        [f for f in image_dir.glob("*") if f.is_file()
         and f.suffix.lower() in image_extensions]
    )

    if not image_files:
        raise ValueError(f"No image files found in {image_dir}")

    return images_to_pdf(image_files, output_path, enhance_type=enhance_type, enhance_strength=enhance_strength)


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
        from pypdf import PdfWriter, PdfReader
    except ImportError:
        raise ImportError(
            "merge_pdfs requires pypdf. Install with: pip install pypdf")

    merger = PdfWriter()
    pdf_files = sorted(input_dir.glob("*.pdf"))

    if not pdf_files:
        raise ValueError(f"No PDF files found in {input_dir}")

    for pdf_file in pdf_files:
        reader = PdfReader(str(pdf_file))
        for page in reader.pages:
            merger.add_page(page)

    with open(str(output_path), 'wb') as output_file:
        merger.write(output_file)


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
