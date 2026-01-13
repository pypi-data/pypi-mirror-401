"""
PdfX - A local CLI tool for PDF manipulation.

PdfX provides utilities for merging, splitting, filtering, and converting PDFs
while keeping your documents private on your local machine.
"""

__version__ = "0.2.2"
__author__ = "Manoj Adhikari"
__license__ = "MIT"

from pdfx.main import (
    parse_color_string,
    parse_page_ranges,
    dump_colors,
    filter_pdf_by_color,
    apply_image_filter_to_pdf,
    auto_enhance_pdf,
    create_scanned_pdf,
    images_to_pdf,
    images_from_dir_to_pdf,
    recolor_pdf_text,
    ocr_make_searchable,
)

__all__ = [
    "parse_color_string",
    "parse_page_ranges",
    "dump_colors",
    "filter_pdf_by_color",
    "apply_image_filter_to_pdf",
    "auto_enhance_pdf",
    "create_scanned_pdf",
    "images_to_pdf",
    "images_from_dir_to_pdf",
    "recolor_pdf_text",
    "ocr_make_searchable",
    "__version__",
]
