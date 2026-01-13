"""
Setup configuration for pdfx-tool.

This file provides backward compatibility with older pip versions.
Modern installations should use pyproject.toml.
"""

from setuptools import setup

# Read the version from the package
version = {}
with open("pdfx/__init__.py") as f:
    for line in f:
        if line.startswith("__version__"):
            exec(line, version)

# Read the long description from README
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pdfx-tool",
    version=version.get("__version__", "0.1.0"),
    author="Manoj Adhikari",
    author_email="adhikarim@etsu.edu",
    description="A local CLI tool for PDF and image manipulation - merge PDFs, split by page/range, convert images to PDF with enhancement",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/pdfx-tool/",
    project_urls={
        "Bug Tracker": "https://github.com/jonamadk/pdfx/issues",
        "Documentation": "https://github.com/jonamadk/PDF-X/blob/main/API_DOCUMENTATION.md",
        "Source Code": "https://github.com/jonamadk/PDF-X",
        "Development": "https://github.com/jonamadk/PDF-X/blob/main/DEVELOPMENT.md",
    },
    packages=["pdfx"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Utilities",
        "Topic :: Office/Business",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pypdf>=3.0.0",
        "cryptography>=41.0.0",
    ],
    extras_require={
        "full": [
            "pymupdf>=1.22.0",
            "Pillow>=10.0.0",
            "pytesseract>=0.3.10",
            "pdf2image>=1.16.3",
        ],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "pdfx=pdfx.cli:main",
        ],
    },
    keywords="pdf cli merge split filter ocr convert",
    include_package_data=True,
)
