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
    image_group.add_argument(
        "--enhance", action="store_const", const="enhance", dest="shorthand_filter")
    image_group.add_argument("--bw", action="store_const",
                             const="bw", dest="shorthand_filter")
    image_group.add_argument(
        "--grayscale", action="store_const", const="grayscale", dest="shorthand_filter")
    image_group.add_argument(
        "--invert", action="store_const", const="invert", dest="shorthand_filter")
    image_group.add_argument(
        "--auto", action="store_const", const="auto", dest="shorthand_filter")

    # Scanned copy options
    scan_group = parser.add_argument_group("scanned copy options")
    scan_group.add_argument(
        "--create-scanned",
        action="store_true",
        help="Create a scanned-looking copy of the PDF",
    )
    scan_group.add_argument(
        "--scan-quality",
        type=str,
        choices=["low", "medium", "high"],
        default="medium",
        help="Scan quality level (default: medium)",
    )
    scan_group.add_argument(
        "--no-noise",
        action="store_true",
        help="Disable noise/grain effect",
    )
    scan_group.add_argument(
        "--add-skew",
        action="store_true",
        help="Add slight rotation to simulate imperfect scanning",
    )

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

    # Auto PDF enhancement options
    enhance_group = parser.add_argument_group("PDF auto-enhancement options")
    enhance_group.add_argument(
        "--pdf-enhance",
        action="store_true",
        help="Automatically enhance a scanned PDF with smart defaults (use --filter-file for input)",
    )
    enhance_group.add_argument(
        "--pdf-enhance-mode",
        type=str,
        choices=["smart", "contrast", "strong", "auto"],
        default="smart",
        help="Auto-enhancement mode: smart (contrast + autocontrast, recommended), contrast (1.5x), strong (2.0x for very faded), auto (autocontrast only). Default: smart",
    )

    # Image-to-PDF conversion options
    img_pdf_group = parser.add_argument_group(
        "image-to-PDF conversion options")
    img_pdf_group.add_argument(
        "--image-to-pdf",
        action="store_true",
        help="Convert image(s) to PDF (use --image-file or --image-dir)",
    )
    img_pdf_group.add_argument(
        "--image-file",
        type=Path,
        help="Single image file to convert to PDF",
    )
    img_pdf_group.add_argument(
        "--image-dir",
        type=Path,
        help="Directory containing images to convert to PDF (processes all images in sorted order)",
    )
    img_pdf_group.add_argument(
        "--image-out",
        type=Path,
        help="Output path for the generated PDF (default: Images.pdf or <dir>_to_pdf.pdf)",
    )
    img_pdf_group.add_argument(
        "--image-enhance",
        type=str,
        choices=["enhance", "brightness", "color", "sharpness", "auto"],
        help="Apply color enhancement to images during PDF conversion. enhance=contrast, brightness=brightness, color=saturation, sharpness=sharpness, auto=autocontrast",
    )
    img_pdf_group.add_argument(
        "--image-enhance-strength",
        type=float,
        default=1.5,
        help="Strength of image enhancement (for contrast/brightness/color/sharpness: 1.0 = no change, < 1.0 = decrease, > 1.0 = increase). Default: 1.5",
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
                output_dir = args.split_file.parent.parent / \
                    "Splitted_Docs" / args.split_file.stem

            print(f"Splitting {args.split_file}...")
            split_pdf(args.split_file, output_dir, args.page_range)
            print(f"✓ Split pages saved to: {output_dir}")
            return 0

        if args.split or args.split_dir:
            split_dir = args.split_dir or Path("filesToSplit")
            if not split_dir.exists():
                print(
                    f"Error: Directory not found: {split_dir}", file=sys.stderr)
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
            output_path = args.filter_out or args.filter_file.parent / \
                f"{args.filter_file.stem}_filtered.pdf"

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
                print(
                    f"Filtering {args.filter_file} by color {args.color_filter}...")
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
            output_path = args.filter_out or args.filter_file.parent / \
                f"{args.filter_file.stem}_{filter_name}.pdf"

            print(f"Applying {filter_name} filter to {args.filter_file}...")
            pages = apply_image_filter_to_pdf(
                args.filter_file,
                output_path,
                filter_name,
                args.image_strength,
            )
            print(f"✓ Processed {pages} pages, saved to: {output_path}")
            return 0

        # Handle scanned copy creation
        if args.filter_file and args.create_scanned:
            output_path = args.filter_out or args.filter_file.parent / \
                f"{args.filter_file.stem}_scanned.pdf"

            print(f"Creating scanned copy of {args.filter_file}...")
            print(f"  Quality: {args.scan_quality}")
            print(f"  Noise: {'disabled' if args.no_noise else 'enabled'}")
            print(f"  Skew: {'enabled' if args.add_skew else 'disabled'}")

            pages = create_scanned_pdf(
                args.filter_file,
                output_path,
                scan_quality=args.scan_quality,
                add_noise=not args.no_noise,
                slight_skew=args.add_skew,
            )
            print(
                f"✓ Created scanned copy with {pages} pages, saved to: {output_path}")
            return 0

        # Handle OCR
        if args.filter_file and args.ocr:
            output_path = args.filter_out or args.filter_file.parent / \
                f"{args.filter_file.stem}_ocr.pdf"

            print(f"Running OCR on {args.filter_file}...")
            pages = ocr_make_searchable(
                args.filter_file, output_path, args.ocr_lang)
            print(
                f"✓ OCR completed for {pages} pages, saved to: {output_path}")
            return 0

        # Handle automatic PDF enhancement
        if args.pdf_enhance:
            if args.filter_file is None:
                print("--pdf-enhance requires --filter-file PATH")
                return 2
            output_path = args.filter_out or args.filter_file.parent / \
                f"{args.filter_file.stem}_enhanced.pdf"

            print(f"Auto-enhancing {args.filter_file}...")
            print(f"  Mode: {args.pdf_enhance_mode}")
            try:
                pages = auto_enhance_pdf(
                    args.filter_file, output_path, auto_mode=args.pdf_enhance_mode)
                print(
                    f"✓ Enhanced {pages} pages ({args.pdf_enhance_mode} mode), saved to: {output_path}")
                return 0
            except Exception as e:
                print(f"Error while auto-enhancing PDF: {e}", file=sys.stderr)
                return 2

        # Handle image-to-PDF conversion
        if args.image_to_pdf:
            if args.image_file is None and args.image_dir is None:
                print("--image-to-pdf requires either --image-file or --image-dir")
                return 2
            try:
                if args.image_file:
                    # Convert single image
                    output_path = args.image_out or args.image_file.parent / \
                        f"{args.image_file.stem}.pdf"
                    images_written = images_to_pdf(
                        [args.image_file], output_path,
                        enhance_type=args.image_enhance,
                        enhance_strength=args.image_enhance_strength)
                    print(
                        f"✓ Converted {images_written} image(s) to {output_path}")
                    return 0
                elif args.image_dir:
                    # Convert all images in directory
                    output_path = args.image_out or \
                        (args.image_dir.parent /
                         f"{args.image_dir.name}_to_pdf.pdf")
                    images_written = images_from_dir_to_pdf(
                        args.image_dir, output_path,
                        enhance_type=args.image_enhance,
                        enhance_strength=args.image_enhance_strength)
                    print(
                        f"✓ Converted {images_written} image(s) from {args.image_dir} to {output_path}")
                    return 0
            except Exception as e:
                print(
                    f"Error while converting images to PDF: {e}", file=sys.stderr)
                return 2

        # Handle dump colors
        if args.dump_colors and args.filter_file:
            print(f"Analyzing colors in {args.filter_file}...")
            try:
                dump_colors(args.filter_file)
                return 0
            except Exception as e:
                print(f"Error while dumping colors: {e}", file=sys.stderr)
                return 2

        # Default: show help if no action specified
        parser.print_help()
        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
