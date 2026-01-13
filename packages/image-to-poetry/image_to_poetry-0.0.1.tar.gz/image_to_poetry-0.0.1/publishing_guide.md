# Publishing `image-to-poetry` to PyPI

## Prerequisites

1.  **PyPI Account**: Ensure you have an account at [pypi.org](https://pypi.org/).
2.  **API Token**: Create an API token in your PyPI account settings.

## Build the Package

Run this from the project root (`image-to-poetry`):

```bash
# Clean previous builds
rm -rf dist/

# Build
python3 -m build
```

## Upload to PyPI

```bash
# Install twine if needed
pip install twine

# Upload
twine upload dist/*
```

*   **Username**: `__token__`
*   **Password**: [Your PyPI API Token]

## Installation After Publishing

```bash
pip install image-to-poetry
```

## Running the Tool

Remember, users will need to set their Gemini API key:

```bash
export GEMINI_API_KEY="AIzaSy..."
image2poetry input.jpg
```
