# Bitmap

A Python package to process raw camera data into 1-bit bitmap images.

## Installation

```bash
pip install bitmap
```

## Usage

```python
from bitmap import BitmapProcessor

# Initialize with a raw camera file
processor = BitmapProcessor('image.nef')

# Process to 1-bit bitmap and save
processor.process_to_1bit('output.bmp')
```

## Features

- Process raw camera data (NEF, CR2, ARW, etc.) into 1-bit bitmap images
- Automatic grayscale conversion with proper luminance weighting
- Floyd-Steinberg dithering for optimal 1-bit conversion
- Simple and intuitive API

## Requirements

- Python >= 3.6
- rawpy >= 0.17.0
- Pillow >= 9.0.0
- numpy >= 1.21.0

## Development

### Install in Development Mode

```bash
pip install -e .
```

### Run Tests

```bash
python -m unittest discover tests
```

## Building and Distribution

### Build the Package

```bash
python setup.py sdist bdist_wheel
```

### Install Locally

```bash
pip install .
```

### Upload to PyPI (after building)

```bash
pip install twine
twine upload dist/*
```

## License

MIT License
