# Demo Package for PyPI

A sample Python package demonstrating how to create and publish packages to the Python Package Index (PyPI).

## Features

- **Calculator**: A simple calculator class with basic mathematical operations
- **Greeter**: Functions to greet single or multiple people

## Installation

```bash
pip install chandra-pypi-demo
```

## Usage

### Calculator

```python
from demo_package import Calculator

calc = Calculator()
result = calc.add(5, 3)  # Returns 8
result = calc.multiply(4, 7)  # Returns 28
result = calc.divide(10, 2)  # Returns 5.0

# View calculation history
history = calc.get_history()
print(history)
```

### Greeter

```python
from demo_package import greet, greet_multiple

# Greet a single person
message = greet("Alice")
print(message)  # "Hello, Alice!"

# Greet with custom message
message = greet("Bob", "Hi")
print(message)  # "Hi, Bob!"

# Greet multiple people
message = greet_multiple(["Alice", "Bob", "Charlie"])
print(message)  # "Hello, Alice, Bob, and Charlie!"
```

## Requirements

- Python 3.7 or higher

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Chandra - chandra385123@gmail.com

## Project Structure

```
chandra-pypi-demo/
├── demo_package/
│   ├── __init__.py
│   ├── calculator.py
│   └── greeter.py
├── pyproject.toml
├── README.md
├── LICENSE
├── MANIFEST.in
└── .gitignore
```
