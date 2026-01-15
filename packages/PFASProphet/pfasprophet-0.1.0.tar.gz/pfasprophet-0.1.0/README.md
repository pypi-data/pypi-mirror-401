# PFASProphet

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

A tool for giving a score on the likelihood of PFAS (Per- and Polyfluoroalkyl Substances) from mass spectrometry data using machine learning.

## Features
- Obtain a PFAS scores from precursor masses and fragment ions.
- Support for CSV files or direct list inputs.
- can be run from python directly or Command-line interface (CLI).
- Handles ionised vs. neutral masses (negative ESI mode).
- See examples for usage.

## Installation
1. Clone the repository: `git clone https://github.com/yourusername/PFASProphet.git`
2. Navigate to the directory: `cd PFASProphet`
3. Create a virtual environment: `python -m venv .venv`
4. Activate it: `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Linux/Mac)
5. Install: `pip install -e .`

## Usage
### CLI Examples
- **Predict from lists**: `pfasprophet --mass "[248.9461]" --fragments "[[63.9624]]"`
- **Predict from CSV**: `pfasprophet --file data.csv`
- **Help**: `pfasprophet` or `pfasprophet --help`

### Python API
```python
from PFASProphet import PFASProphet

prophet = PFASProphet()
result = prophet.predict(mass=[248.9461], fragments=[[63.9624]])
print(result)