# Topsis-sneha-102303033

Python package implementing TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution).

## Description

    Run TOPSIS on input_file and write result to output_file.

    input_file: path to CSV or XLSX
    weights_str: e.g. "1,1,1,2"
    impacts_str: e.g. "+,+,-,+"
    output_file: path to CSV to write

## conditions

- The input file must be a CSV or XLSX file.
- The input file must contain at least three columns.
- All columns except the first must contain numeric data.
- The number of weights and impacts must match the number of criteria (columns minus one).

## Installation

```bash
pip install Topsis-sneha-102303033
```

## Usage

```python
from topsis_sneha_102303033 import topsis
topsis("input.csv", "1,1,1,2", "+,-,+,+", "output.csv")
```

## License

This project is licensed under the MIT License.

## Author

Sneha Gupta - 102303033
