# Development Guide

## Setup Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pdfx.git
   cd pdfx
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install in development mode with all dependencies:
   ```bash
   pip install -e ".[full,dev]"
   ```

## Project Structure

```
PDF-X/
├── pdfx/                  # Main package
│   ├── __init__.py        # Package initialization and version
│   ├── __main__.py        # Module entry point (python -m pdfx)
│   ├── cli.py             # Command-line interface
│   └── main.py            # Core PDF manipulation functions
├── tests/                 # Test suite
│   ├── test_color_filter.py
│   ├── test_image_filter.py
│   └── test_recolor_and_ocr.py
├── pyproject.toml         # Modern Python packaging config
├── setup.py               # Backward compatible setup
├── MANIFEST.in            # Specify files to include in distribution
├── README.md              # User documentation
├── LICENSE                # MIT License
├── requirements.txt       # Dependency list (for reference)
├── PUBLISHING.md          # PyPI publishing guide
└── DEVELOPMENT.md         # This file
```

## Running Tests

Run all tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=pdfx --cov-report=html
```

Run specific test file:
```bash
pytest tests/test_color_filter.py
```

Run specific test function:
```bash
pytest tests/test_color_filter.py::test_parse_color_string
```

## Code Quality

### Format code with Black
```bash
black pdfx/ tests/
```

### Lint with Flake8
```bash
flake8 pdfx/ tests/
```

### Type checking with mypy
```bash
mypy pdfx/
```

## Testing the CLI Locally

After installing in development mode (`pip install -e .`):

```bash
pdfx --help
pdfx --version
```

Or run as a module:
```bash
python -m pdfx --help
```

## Making Changes

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and add tests

3. Run tests and code quality checks:
   ```bash
   pytest
   black pdfx/ tests/
   flake8 pdfx/ tests/
   ```

4. Commit your changes:
   ```bash
   git add .
   git commit -m "Add feature: description"
   ```

5. Push and create a pull request:
   ```bash
   git push origin feature/your-feature-name
   ```

## Adding New Features

### Adding a new CLI option

1. Update `pdfx/cli.py`:
   - Add argument to parser
   - Add handling logic in `main()` function

2. Update `pdfx/main.py`:
   - Implement the core functionality

3. Add tests in `tests/`:
   - Create or update test files

4. Update `README.md`:
   - Document the new option
   - Add usage examples

### Adding new dependencies

1. Update `pyproject.toml`:
   ```toml
   dependencies = [
       "existing-package>=1.0.0",
       "new-package>=2.0.0",
   ]
   ```

2. Update `setup.py` (for backward compatibility):
   ```python
   install_requires=[
       "existing-package>=1.0.0",
       "new-package>=2.0.0",
   ],
   ```

3. Reinstall in development mode:
   ```bash
   pip install -e ".[full,dev]"
   ```

## Release Checklist

Before releasing a new version:

- [ ] All tests pass (`pytest`)
- [ ] Code is formatted (`black pdfx/ tests/`)
- [ ] No linting errors (`flake8 pdfx/ tests/`)
- [ ] Version bumped in `pdfx/__init__.py`
- [ ] Version bumped in `pyproject.toml`
- [ ] CHANGELOG updated (if you have one)
- [ ] README updated with new features
- [ ] Tested locally (`pip install -e .`)
- [ ] Committed and tagged:
  ```bash
  git commit -m "Release v0.1.1"
  git tag v0.1.1
  git push && git push --tags
  ```
- [ ] Built distribution (`python -m build`)
- [ ] Uploaded to TestPyPI first
- [ ] Tested installation from TestPyPI
- [ ] Uploaded to PyPI

See [PUBLISHING.md](PUBLISHING.md) for detailed publishing instructions.

## Common Development Tasks

### Clean build artifacts
```bash
rm -rf build/ dist/ *.egg-info pdfx.egg-info
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
```

### Rebuild the package
```bash
python -m build
```

### Install specific version locally
```bash
pip install dist/pdfx_tool-0.1.0-py3-none-any.whl
```

### Check package contents
```bash
tar -tzf dist/pdfx_tool-0.1.0.tar.gz
```

### Uninstall the package
```bash
pip uninstall pdfx-tool
```

## Getting Help

- Check existing issues: https://github.com/yourusername/pdfx/issues
- Create a new issue: https://github.com/yourusername/pdfx/issues/new
- Read the README: [README.md](README.md)
