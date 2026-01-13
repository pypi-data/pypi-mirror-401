"""
Command-line interface for PdfX.

This module provides the CLI entry point for the PdfX tool.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from pdfx import __version__
from pdfx.main import (
    parse_color_string,
    filter_pdf_by_color,
    apply_image_filter_to_pdf,
    recolor_pdf_text,
    ocr_make_searchable,
    merge_pdfs,
    split_pdf,
)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="PdfX - A local CLI tool for PDF manipulation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"PdfX {__version__}",
    )
    
    # Merge options
    merge_group = parser.add_argument_group("merge options")
    merge_group.add_argument(
        "-m", "--merge-dir",
        type=Path,
        help="Directory containing PDFs to merge",
    )
    merge_group.add_argument(
        "-o", "--output",
        type=str,
        default="Merged Document.pdf",
        help="Output filename for merged PDF (default: 'Merged Document.pdf')",
    )
    
    # Split options
    split_group = parser.add_argument_group("split options")
    split_group.add_argument(
        "--split",
        action="store_true",
        help="Split PDFs in source directory into single pages",
    )
    split_group.add_argument(
        "--split-dir",
        type=Path,
        help="Directory containing PDFs to split",
    )
    split_group.add_argument(
        "--split-file",
        type=Path,
        help="Single PDF file to split into pages",
    )
    split_group.add_argument(
        "--split-out",
        type=Path,
        help="Output directory for split pages",
    )
    split_group.add_argument(
        "--page-range",
        type=str,
        help='Page range to extract (e.g., "1-3,5")',
    )
    
    # Filter options
    filter_group = parser.add_argument_group("filter options")
    filter_group.add_argument(
        "--filter-file",
        type=Path,
        help="PDF file to filter",
    )
    filter_group.add_argument(
        "--color-filter",
        type=str,
        help="Target color to filter (#RRGGBB or R,G,B)",
    )
    filter_group.add_argument(
        "--color-tolerance",
        type=float,
        default=0.0,
        help="Color distance tolerance (default: 0.0)",
    )
    filter_group.add_argument(
        "--filter-out",
        type=Path,
        help="Output path for filtered PDF",
    )
    
    # Image filter options
    image_group = parser.add_argument_group("image filter options")
    image_group.add_argument(
        "--image-filter",
        type=str,
        choices=["enhance", "bw", "grayscale", "invert", "auto"],
        help="Apply image-level filter",
    )
    image_group.add_argument(
        "--image-strength",
        type=float,
        default=1.5,
        help="Filter strength/threshold (default: 1.5)",
    )
    
    # Shorthand filter flags
    image_group.add_argument("--enhance", action="store_const", const="enhance", dest="shorthand_filter")
    image_group.add_argument("--bw", action="store_const", const="bw", dest="shorthand_filter")
    image_group.add_argument("--grayscale", action="store_const", const="grayscale", dest="shorthand_filter")
    image_group.add_argument("--invert", action="store_const", const="invert", dest="shorthand_filter")
    image_group.add_argument("--auto", action="store_const", const="auto", dest="shorthand_filter")
    
    # Recolor options
    recolor_group = parser.add_argument_group("recolor options")
    recolor_group.add_argument(
        "--recolor",
        type=str,
        help="Replacement color (#RRGGBB or R,G,B)",
    )
    recolor_group.add_argument(
        "--recolor-tolerance",
        type=float,
        default=0.0,
        help="Color matching tolerance for recoloring",
    )
    
    # OCR options
    ocr_group = parser.add_argument_group("OCR options")
    ocr_group.add_argument(
        "--ocr",
        action="store_true",
        help="Make PDF searchable using OCR",
    )
    ocr_group.add_argument(
        "--ocr-lang",
        type=str,
        default="eng",
        help="Tesseract language code (default: 'eng')",
    )
    
    # Diagnostics
    parser.add_argument(
        "--dump-colors",
        action="store_true",
        help="Print detected text colors in PDF",
    )
    
    args = parser.parse_args()
    
    try:
        # Handle merge
        if args.merge_dir:
            output_dir = args.merge_dir.parent / "Merged_Doc"
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / args.output
            
            print(f"Merging PDFs from {args.merge_dir}...")
            merge_pdfs(args.merge_dir, output_path)
            print(f"✓ Merged PDF saved to: {output_path}")
            return 0
        
        # Handle split
        if args.split_file:
            if args.split_out:
                output_dir = args.split_out
            else:
                output_dir = args.split_file.parent.parent / "Splitted_Docs" / args.split_file.stem
            
            print(f"Splitting {args.split_file}...")
            split_pdf(args.split_file, output_dir, args.page_range)
            print(f"✓ Split pages saved to: {output_dir}")
            return 0
        
        if args.split or args.split_dir:
            split_dir = args.split_dir or Path("filesToSplit")
            if not split_dir.exists():
                print(f"Error: Directory not found: {split_dir}", file=sys.stderr)
                return 1
            
            for pdf_file in split_dir.glob("*.pdf"):
                output_dir = split_dir.parent / "Splitted_Docs" / pdf_file.stem
                print(f"Splitting {pdf_file.name}...")
                split_pdf(pdf_file, output_dir)
            
            print("✓ All PDFs split successfully")
            return 0
        
        # Handle color filtering
        if args.filter_file and args.color_filter:
            target_color = parse_color_string(args.color_filter)
            output_path = args.filter_out or args.filter_file.parent / f"{args.filter_file.stem}_filtered.pdf"
            
            if args.recolor:
                new_color = parse_color_string(args.recolor)
                print(f"Recoloring text in {args.filter_file}...")
                pages = recolor_pdf_text(
                    args.filter_file,
                    output_path,
                    target_color,
                    new_color,
                    args.recolor_tolerance,
                )
                print(f"✓ Recolored {pages} pages, saved to: {output_path}")
            else:
                print(f"Filtering {args.filter_file} by color {args.color_filter}...")
                pages = filter_pdf_by_color(
                    args.filter_file,
                    output_path,
                    target_color,
                    args.color_tolerance,
                )
                print(f"✓ Filtered {pages} pages, saved to: {output_path}")
            
            return 0
        
        # Handle image filtering
        filter_name = args.shorthand_filter or args.image_filter
        if args.filter_file and filter_name:
            output_path = args.filter_out or args.filter_file.parent / f"{args.filter_file.stem}_{filter_name}.pdf"
            
            print(f"Applying {filter_name} filter to {args.filter_file}...")
            pages = apply_image_filter_to_pdf(
                args.filter_file,
                output_path,
                filter_name,
                args.image_strength,
            )
            print(f"✓ Processed {pages} pages, saved to: {output_path}")
            return 0
        
        # Handle OCR
        if args.filter_file and args.ocr:
            output_path = args.filter_out or args.filter_file.parent / f"{args.filter_file.stem}_ocr.pdf"
            
            print(f"Running OCR on {args.filter_file}...")
            pages = ocr_make_searchable(args.filter_file, output_path, args.ocr_lang)
            print(f"✓ OCR completed for {pages} pages, saved to: {output_path}")
            return 0
        
        # Handle dump colors
        if args.dump_colors and args.filter_file:
            print(f"Analyzing colors in {args.filter_file}...")
            try:
                import fitz
                doc = fitz.open(args.filter_file)
                colors_found = set()
                
                for page_num in range(len(doc)):
                    page = doc[page_num]
                    blocks = page.get_text("dict")
                    
                    for block in blocks.get("blocks", []):
                        if block.get("type") == 0:
                            for line in block.get("lines", []):
                                for span in line.get("spans", []):
                                    color = span.get("color")
                                    if color is not None:
                                        r = (color >> 16) & 0xFF
                                        g = (color >> 8) & 0xFF
                                        b = color & 0xFF
                                        text_sample = span.get("text", "")[:20]
                                        colors_found.add((r, g, b, text_sample))
                
                doc.close()
                
                print("\nColors found in document:")
                for r, g, b, sample in sorted(colors_found):
                    print(f"  RGB({r:3d},{g:3d},{b:3d}) = #{r:02X}{g:02X}{b:02X}  Sample: {sample}")
                
                return 0
            except ImportError:
                print("Error: --dump-colors requires pymupdf. Install with: pip install pymupdf", file=sys.stderr)
                return 2
        
        # Default: show help if no action specified
        parser.print_help()
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
