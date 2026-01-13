"""
PdfX - A local CLI tool for PDF manipulation.

PdfX provides utilities for merging, splitting, filtering, and converting PDFs
while keeping your documents private on your local machine.
"""

__version__ = "0.1.0"
__author__ = "Manoj Adhikari"
__license__ = "MIT"

from pdfx.main import (
    parse_color_string,
    filter_pdf_by_color,
    apply_image_filter_to_pdf,
    recolor_pdf_text,
    ocr_make_searchable,
)

__all__ = [
    "parse_color_string",
    "filter_pdf_by_color",
    "apply_image_filter_to_pdf",
    "recolor_pdf_text",
    "ocr_make_searchable",
    "__version__",
]
