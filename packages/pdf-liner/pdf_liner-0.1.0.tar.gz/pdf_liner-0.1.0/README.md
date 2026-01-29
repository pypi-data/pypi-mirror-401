# PDF Liner

A simple Python tool that adds equally spaced horizontal lines to PDF files, making them perfect for printing and handwriting and taking notes on them.

## Installation

### Install from PyPI (Recommended)

Install pdf-liner directly from PyPI:

```bash
pip install pdf-liner
```

Or using pipx for isolated installation:

```bash
pipx install pdf-liner
```

### Install from Source

1. Clone the repository:
```bash
git clone https://github.com/raideno/pdf-liner.git
cd pdf-liner
```

2. Install using Poetry:
```bash
poetry install
```

Or install in development mode using pip:
```bash
pip install -e .
```

## Usage

Once installed, you can use the `pdf-liner` command from anywhere:

```bash
pdf-liner input.pdf
```

This will create `input_lined.pdf` with default settings (20-point spacing, 0.25 opacity).

### Specify Output File

```bash
pdf-liner input.pdf -o output.pdf
# or
pdf-liner input.pdf --output output.pdf
```

### Customize Line Spacing and Opacity

```bash
pdf-liner input.pdf -o output.pdf -s 25 -a 0.2
# or
pdf-liner input.pdf --output output.pdf --line-spacing 25 --opacity 0.2
```

- `-s` or `--line-spacing`: Space between lines in points (default: 20)
- `-a` or `--opacity`: Line opacity from 0.0 to 1.0 (default: 0.25)

### Enhance Bottom Lines for Better Printing

Some printers tend to fade lines at the bottom of pages. Use the `-e` option to make the bottom lines thicker and darker:

```bash
pdf-liner input.pdf -e 5
# or
pdf-liner input.pdf --enhance-bottom-lines 5
```

- `-e` or `--enhance-bottom-lines`: Number of bottom lines to enhance (default: 3, set to 0 to disable)

### Add Padding Pages

Add a blank lined page after each page:

```bash
pdf-liner input.pdf -p
# or
pdf-liner input.pdf --padding
```

### Get Help

```bash
pdf-liner -h
# or
pdf-liner --help
```

## Parameters

- **input_pdf** (required) - Path to the input PDF file
- **-o, --output** (optional) - Path for the output file (default: `input_lined.pdf`)
- **-s, --line-spacing** (optional) - Space between lines in points (default: 20)
- **-a, --opacity** (optional) - Line opacity from 0.0 to 1.0 (default: 0.25)
- **-e, --enhance-bottom-lines** (optional) - Number of bottom lines to enhance for better printing (default: 3)
- **-p, --padding** (optional) - Adds a white page with lines after each page

## Development

### Requirements

- Python 3.9+
- Poetry

### Setup Development Environment

```bash
# Install Poetry if you haven't already
pip install poetry

# Install dependencies
poetry install

# Run the tool
poetry run pdf-liner input.pdf
```

### Build the Package

```bash
poetry build
```

This will create distribution files in the `dist/` directory.

## Publishing

The package is automatically published to PyPI when a new release is created on GitHub. The workflow uses the `PYPI_API_TOKEN` secret configured in the repository.

To publish manually:

```bash
poetry config pypi-token.pypi YOUR_PYPI_TOKEN
poetry publish --build
```

## License

MIT
