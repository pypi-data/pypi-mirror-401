# DataGuard

DataGuard is a lightweight Python package for basic dataset quality validation with both API and CLI support.

## Features

- Missing value detection
- Duplicate row detection
- Optional target column analysis
- JSON report export
- Command line interface

## Installation

From TestPyPI:

```bash
pip install -i https://test.pypi.org/simple/ dataguard-lite
```

Local development:
```
pip install -e .
```

Usage (Python API)

```
from dataguard import validate_csv

report = validate_csv("data.csv", target="label")
report.summary()
report.to_json("report.json")
```
Usage (CLI)
```
dataguard data.csv
dataguard data.csv --target label
dataguard data.csv --json report.json
```
