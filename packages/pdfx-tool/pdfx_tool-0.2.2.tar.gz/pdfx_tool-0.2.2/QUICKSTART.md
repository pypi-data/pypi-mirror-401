# PdfX Quick Start Guide

## Installation

```bash
# Install basic version (merge/split PDFs)
pip install pdfx-tool

# Install with all features (recommended)
pip install pdfx-tool[full]
```

## Basic Usage

### 1. Merge PDFs

Combine multiple PDFs into one:

```bash
# Merge all PDFs in a directory
pdfx -m /path/to/pdfs -o "Combined.pdf"

# Result: Creates Merged_Doc/Combined.pdf
```

### 2. Split PDF into Pages

Break a PDF into individual page files:

```bash
# Split entire PDF
pdfx --split-file document.pdf

# Result: Creates Splitted_Docs/document/document_page_1.pdf, document_page_2.pdf, etc.
```

### 3. Extract Specific Pages

Get only the pages you need:

```bash
# Extract pages 1-3 and page 5
pdfx --split-file document.pdf --page-range "1-3,5"

# Extract single page
pdfx --split-file document.pdf --page-range "10"

# Result: Creates only the requested pages
```

### 4. Convert Image to PDF

Turn an image into a PDF:

```bash
# Single image
pdfx --image-to-pdf --image-file photo.jpg --image-out photo.pdf
```

### 5. Merge Images into PDF

Combine multiple images into one PDF:

```bash
# All images in a directory
pdfx --image-to-pdf --image-dir /path/to/images

# Result: Creates /path/to/images_to_pdf.pdf
```

### 6. Convert Image to PDF with Enhancement

Make your scanned images look better:

```bash
# Enhance contrast for scanned documents
pdfx --image-to-pdf --image-file scan.jpg \
     --image-enhance enhance --image-enhance-strength 1.8

# Auto-enhance (automatic contrast adjustment)
pdfx --image-to-pdf --image-file scan.jpg --image-enhance auto
```

### 7. Enhance Existing PDF

Improve scanned PDF quality:

```bash
# Smart auto-enhancement (recommended)
pdfx --filter-file scanned.pdf --pdf-enhance

# Strong enhancement for faded documents
pdfx --filter-file faded.pdf --pdf-enhance --pdf-enhance-mode strong

# Result: Creates scanned_enhanced.pdf or faded_enhanced.pdf
```

## Common Workflows

### Scan to Enhanced PDF

```bash
# 1. Convert scanned images to PDF with enhancement
pdfx --image-to-pdf --image-dir ./scans \
     --image-enhance enhance --image-enhance-strength 1.8

# 2. Result: scans_to_pdf.pdf with improved quality
```

### Merge and Enhance

```bash
# 1. Merge all PDFs
pdfx -m ./documents -o "Combined.pdf"

# 2. Enhance the merged result
pdfx --filter-file Merged_Doc/Combined.pdf --pdf-enhance
```

### Extract and Process Pages

```bash
# 1. Extract specific pages
pdfx --split-file large.pdf --page-range "1-10"

# 2. Merge extracted pages with other PDFs
pdfx -m Splitted_Docs/large/ -o "First10Pages.pdf"
```

## Enhancement Options

### Image Enhancement Types

- `enhance` - Increase contrast (good for faded scans)
- `brightness` - Adjust brightness
- `color` - Increase color saturation
- `sharpness` - Make images sharper
- `auto` - Automatic contrast optimization

### Enhancement Strength

- `1.0` = No change
- `< 1.0` = Decrease effect
- `> 1.0` = Increase effect
- Default: `1.5` (recommended for most scans)

### PDF Enhancement Modes

- `smart` (default) - Contrast + autocontrast for best results
- `contrast` - Standard contrast boost (1.5x)
- `strong` - Heavy contrast boost (2.0x) for very faded documents
- `auto` - Autocontrast only

## Help and Options

View all available options:

```bash
pdfx --help
```

Check version:

```bash
pdfx --version
```

## Tips

1. **File paths with spaces**: Use quotes
   ```bash
   pdfx -m "/path/to/My Documents" -o "My Report.pdf"
   ```

2. **Batch processing**: Use shell loops
   ```bash
   for pdf in *.pdf; do
     pdfx --filter-file "$pdf" --pdf-enhance
   done
   ```

3. **Test enhancement strength**: Try different values (1.2, 1.5, 1.8, 2.0) to find what works best for your documents

4. **Organized output**: Results are automatically organized into `Merged_Doc/` and `Splitted_Docs/` directories

## Next Steps

- Read the full [README.md](README.md) for advanced features
- See [DEVELOPMENT.md](DEVELOPMENT.md) for contributing
- Check [PUBLISHING.md](PUBLISHING.md) for PyPI publishing guide

## Troubleshooting

**Problem**: Command not found after installation
```bash
# Solution: Make sure pip bin directory is in PATH, or use:
python -m pdfx --help
```

**Problem**: "Module not found" errors with advanced features
```bash
# Solution: Install full dependencies:
pip install pdfx-tool[full]
```

**Problem**: OCR not working
```bash
# Solution: Install Tesseract system package:
# macOS: brew install tesseract
# Ubuntu: sudo apt-get install tesseract-ocr
```
