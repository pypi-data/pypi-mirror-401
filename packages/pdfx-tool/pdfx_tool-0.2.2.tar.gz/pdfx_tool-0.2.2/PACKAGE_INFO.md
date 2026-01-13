# PdfX Package Information

## Package Details

- **Package Name**: `pdfx-tool`
- **Version**: 0.1.0
- **Author**: Manoj Adhikari
- **Email**: adhikarim@etsu.edu
- **License**: MIT
- **Python Version**: >=3.8

## Description

A local CLI tool for PDF and image manipulation that keeps your documents private. Merge PDFs, split by pages or ranges, convert images to PDFs, and enhance scanned documents - all on your local machine.

## Core Features

### PDF Operations
1. **Merge PDFs**: Combine multiple PDF files from a directory into a single PDF document
2. **Split PDF into pages**: Break a PDF into individual page files
3. **Split PDF by page range**: Extract specific pages or page ranges (e.g., "1-3,5,7-10")

### Image to PDF Conversion
4. **Convert single image to PDF**: Turn any supported image into a PDF
5. **Merge images to PDF**: Combine multiple images from a directory into a single PDF

### Enhancement Features
6. **Image to PDF with enhancement**: Convert images to PDF with color/contrast enhancement for better scanned document quality
7. **Enhance existing PDFs**: Improve PDF colors and contrast (useful for scanned documents)

### Supported Image Formats
- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- GIF (.gif)
- TIFF (.tif, .tiff)
- WebP (.webp)

### Package Structure Created

```
PDF-X/
├── pdfx/                     # Main package directory
│   ├── __init__.py          # Package initialization (v0.1.0)
│   ├── __main__.py          # Enables: python -m pdfx
│   ├── cli.py               # Command-line interface
│   └── main.py              # Core PDF functions
├── tests/                    # Test suite (updated imports)
│   ├── __init__.py
│   ├── test_color_filter.py
│   ├── test_image_filter.py
│   └── test_recolor_and_ocr.py
├── dist/                     # Built distributions (ready to upload!)
│   ├── pdfx_tool-0.1.0-py3-none-any.whl (15KB)
│   └── pdfx_tool-0.1.0.tar.gz (22KB)
├── pyproject.toml           # Modern package configuration
├── setup.py                 # Backward compatibility
├── MANIFEST.in              # Files to include in package
├── README.md                # User documentation (updated)
├── LICENSE                  # MIT License
├── DEVELOPMENT.md           # Development guide (NEW)
├── PUBLISHING.md            # PyPI publishing guide (NEW)
└── requirements.txt         # Dependencies reference
```

### Built Distribution Files

✅ **Wheel**: `dist/pdfx_tool-0.1.0-py3-none-any.whl` (15KB)
✅ **Source**: `dist/pdfx_tool-0.1.0.tar.gz` (22KB)

These files are ready to upload to PyPI!

## Installation Methods

Once published to PyPI, users can install your package with:

### Basic Installation
```bash
pip install pdfx-tool
```

### Full Installation (with all features)
```bash
pip install pdfx-tool[full]
```

### From Local Build (for testing)
```bash
pip install dist/pdfx_tool-0.1.0-py3-none-any.whl
```

## Usage

After installation, users can use the package in three ways:

### 1. Command-line tool
```bash
pdfx --help
pdfx --version
pdfx -m /path/to/pdfs -o "merged.pdf"
```

### 2. Python module
```bash
python -m pdfx --help
```

### 3. Python library
```python
from pdfx import parse_color_string, filter_pdf_by_color
from pathlib import Path

color = parse_color_string("#FF0000")  # (255, 0, 0)
filter_pdf_by_color(Path("input.pdf"), Path("output.pdf"), color)
```

## Next Steps

### Before Publishing (Update These)

1. **Update email** in [pyproject.toml](pyproject.toml):
   ```toml
   authors = [
       {name = "Manoj Adhikari", email = "YOUR_REAL_EMAIL@example.com"}
   ]
   ```

2. **Update URLs** in [pyproject.toml](pyproject.toml):
   ```toml
   [project.urls]
   Homepage = "https://pypi.org/project/pdfx-tool/"
   Repository = "https://github.com/jonamadk/PDF-X"
   ```

3. **Update URLs** in [setup.py](setup.py):
   ```python
   author_email="adhikarim@etsu.edu",
   url="https://github.com/jonamadk/PDF-X",
   ```

### Publishing to PyPI

Follow the detailed instructions in [PUBLISHING.md](PUBLISHING.md):

1. **Test on TestPyPI first** (recommended):
   ```bash
   python -m twine upload --repository testpypi dist/*
   ```

2. **Publish to PyPI** (production):
   ```bash
   python -m twine upload dist/*
   ```

See [PUBLISHING.md](PUBLISHING.md) for complete step-by-step instructions.

### Development

See [DEVELOPMENT.md](DEVELOPMENT.md) for:
- Setting up development environment
- Running tests
- Code quality checks
- Adding new features
- Release checklist

## Package Features

### Dependencies

**Required (automatically installed)**:
- `pypdf>=3.0.0` - Core PDF manipulation
- `cryptography>=41.0.0` - PDF encryption support

**Optional (install with `[full]`)**:
- `pymupdf>=1.22.0` - Advanced PDF features, color filtering
- `Pillow>=10.0.0` - Image processing
- `pytesseract>=0.3.10` - OCR support
- `pdf2image>=1.16.3` - PDF to image conversion

**Development (install with `[dev]`)**:
- `pytest>=7.0.0` - Testing framework
- `pytest-cov>=4.0.0` - Code coverage
- `black>=23.0.0` - Code formatting
- `flake8>=6.0.0` - Linting
- `mypy>=1.0.0` - Type checking

### Entry Point

The package provides a console script:
- Command: `pdfx`
- Module: `pdfx.cli:main`

## Key Changes Made

1. ✅ Created `pdfx/` package directory
2. ✅ Moved core functionality to `pdfx/main.py`
3. ✅ Created CLI in `pdfx/cli.py`
4. ✅ Added `__main__.py` for module execution
5. ✅ Created `pyproject.toml` with modern packaging
6. ✅ Created `setup.py` for compatibility
7. ✅ Created `MANIFEST.in` for file inclusion
8. ✅ Updated test imports (`PdfX` → `pdfx`)
9. ✅ Updated README with pip installation
10. ✅ Added PUBLISHING.md guide
11. ✅ Added DEVELOPMENT.md guide
12. ✅ Successfully built distribution files

## Quality Checks

### Build Status
✅ Package builds successfully
✅ Wheel created: `pdfx_tool-0.1.0-py3-none-any.whl`
✅ Source distribution: `pdfx_tool-0.1.0.tar.gz`
✅ All required files included

### Package Info
- Name: `pdfx-tool`
- Version: `0.1.0`
- License: MIT
- Python: >=3.8
- Platform: OS Independent

## Testing the Package

Before publishing, test the package locally:

```bash
# Create test environment
python3 -m venv test_env
source test_env/bin/activate

# Install from wheel
pip install dist/pdfx_tool-0.1.0-py3-none-any.whl

# Test commands
pdfx --version
pdfx --help

# Clean up
deactivate
rm -rf test_env
```

## Support

For questions or issues:
1. Read [README.md](README.md) for usage examples
2. See [DEVELOPMENT.md](DEVELOPMENT.md) for development guide
3. Check [PUBLISHING.md](PUBLISHING.md) for publishing steps
4. Review test files in `tests/` for code examples

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

---

**Status**: ✅ Ready for PyPI publishing (after updating author info and URLs)
**Version**: 0.1.0
**Build Date**: January 10, 2026
