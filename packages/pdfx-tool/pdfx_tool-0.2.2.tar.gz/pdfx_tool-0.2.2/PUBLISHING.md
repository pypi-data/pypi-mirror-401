# Publishing to PyPI

This guide explains how to build and publish the `pdfx-tool` package to PyPI.

## Prerequisites

1. Install build tools:
   ```bash
   pip install --upgrade build twine
   ```

2. Create accounts on:
   - [PyPI](https://pypi.org/account/register/) (production)
   - [TestPyPI](https://test.pypi.org/account/register/) (testing)

## Build the Package

1. Make sure you're in the project root directory:
   ```bash
   cd /path/to/PDF-X
   ```

2. Clean any previous builds:
   ```bash
   rm -rf build/ dist/ *.egg-info pdfx.egg-info
   ```

3. Build the package:
   ```bash
   python -m build
   ```

   This creates:
   - `dist/pdfx_tool-0.1.0.tar.gz` (source distribution)
   - `dist/pdfx_tool-0.1.0-py3-none-any.whl` (wheel distribution)

## Test the Package Locally

1. Create a test virtual environment:
   ```bash
   python -m venv test_env
   source test_env/bin/activate  # On Windows: test_env\Scripts\activate
   ```

2. Install the package locally:
   ```bash
   pip install dist/pdfx_tool-0.1.0-py3-none-any.whl
   ```

3. Test the installation:
   ```bash
   pdfx --version
   pdfx --help
   ```

4. Deactivate and clean up:
   ```bash
   deactivate
   rm -rf test_env
   ```

## Publish to TestPyPI (Recommended First Step)

1. Upload to TestPyPI:
   ```bash
   python -m twine upload --repository testpypi dist/*
   ```

   You'll be prompted for your TestPyPI username and password.

2. Test installation from TestPyPI:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pdfx-tool
   ```

   Note: We use `--extra-index-url` because dependencies like `pypdf` are only on PyPI, not TestPyPI.

3. Verify the installation:
   ```bash
   pdfx --version
   ```

## Publish to PyPI (Production)

Once you've tested on TestPyPI:

1. Upload to PyPI:
   ```bash
   python -m twine upload dist/*
   ```

   You'll be prompted for your PyPI username and password.

2. Verify the package is live:
   ```bash
   pip install pdfx-tool
   ```

## Using API Tokens (Recommended)

Instead of passwords, use API tokens for better security:

1. Create API tokens on PyPI/TestPyPI:
   - Go to Account Settings → API tokens
   - Create a token with scope for this project

2. Create a `~/.pypirc` file:
   ```ini
   [distutils]
   index-servers =
       pypi
       testpypi

   [pypi]
   username = __token__
   password = pypi-YOUR-API-TOKEN-HERE

   [testpypi]
   username = __token__
   password = pypi-YOUR-TESTPYPI-TOKEN-HERE
   ```

3. Set file permissions:
   ```bash
   chmod 600 ~/.pypirc
   ```

Now `twine upload` will use the tokens automatically.

## Version Management

Before each release:

1. Update the version in `pdfx/__init__.py`:
   ```python
   __version__ = "0.1.1"  # Increment version
   ```

2. Update the version in `pyproject.toml`:
   ```toml
   version = "0.1.1"
   ```

3. Commit the changes:
   ```bash
   git add pdfx/__init__.py pyproject.toml
   git commit -m "Bump version to 0.1.1"
   git tag v0.1.1
   git push && git push --tags
   ```

4. Rebuild and upload following the steps above.

## Troubleshooting

### "File already exists" error
- You can't overwrite existing versions on PyPI
- Increment the version number and rebuild

### Import errors after installation
- Make sure all dependencies are listed in `pyproject.toml`
- Test with a clean virtual environment

### Missing files in package
- Check `MANIFEST.in` includes all necessary files
- Use `python -m build --sdist` and check contents:
  ```bash
  tar -tzf dist/pdfx_tool-0.1.0.tar.gz
  ```

## Additional Resources

- [Python Packaging User Guide](https://packaging.python.org/)
- [PyPI Help](https://pypi.org/help/)
- [Twine Documentation](https://twine.readthedocs.io/)
