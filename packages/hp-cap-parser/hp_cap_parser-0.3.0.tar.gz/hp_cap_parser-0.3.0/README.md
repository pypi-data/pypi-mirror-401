# hp-cap-parser

A Python library for parsing HP Content Aggregator for Products (CAP) data files. Provides a clean, simple API for extracting and analyzing CAP information from HP system outputs.

## Installation

```bash
pip install hp-cap-parser
```

## Usage

```python
from hp_cap_parser import HPCapParser

parser = HPCapParser()
parser.parse_file("input.xml", "output_directory")
```

## Development

### Setup

```bash
pip install -e .
```

### Running Tests

```bash
pytest
```

For verbose output:

```bash
pytest -v
```

For coverage report:

```bash
pytest --cov
```

TODO:

Lifestyle & other image types : https://cap.hpcontent.com/support/solutions/articles/9000058002-working-with-images-in-cap

