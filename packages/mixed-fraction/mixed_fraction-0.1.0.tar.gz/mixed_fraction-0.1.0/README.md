# mixed-fraction

A Python library for working with **mixed fractions** (integer + proper fraction)
with clean ASCII-style formatting and operator support.

## Features

- Mixed fraction representation (integer + fraction)
- Clean aligned ASCII output
- Supports addition, subtraction, multiplication, division
- Built on Python's `fractions.Fraction`
- Fully tested with `pytest`

## Installation

```bash
pip install mixed-fraction

For local development:
pip install -e .

    Usage

from mixed_fraction import MixedFraction

a = MixedFraction(20, 3)
b = MixedFraction(5, 3)

print(a + b)

    Output:

  1
8 —
  3

    Examples

print(MixedFraction(7, 2))

  1
3 —
  2

print(MixedFraction(88, 7))

   4
12 —
   7

print(MixedFraction(-25, 4))

   1
-6 —
   4

    Error Handling

 Invalid divisor:

MixedFraction(5, 0)

ZeroDivisionError: Divisor cannot be zero.

 Invalid parameter type:

MixedFraction("5", 2)

TypeError: dividend must be an integer

 Invalid operation:

MixedFraction(3, 2) + 5

TypeError: Unsupported operand type(s) for +: 'MixedFraction' and 'int'
    
    Testing

All tests are written using pytest.

Run tests from the project root:

 pytest

 Expected output:

======================== 5 passed in 0.05s ========================
 
 Project Structure

mixed_fraction/
│
├── mixed_fraction/
│   ├── __init__.py
│   └── mixed_fraction.py
│
├── tests/
│   └── test_mixed_fraction.py
│
├── pyproject.toml
├── README.md
└── LICENSE

## License

This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for details.









