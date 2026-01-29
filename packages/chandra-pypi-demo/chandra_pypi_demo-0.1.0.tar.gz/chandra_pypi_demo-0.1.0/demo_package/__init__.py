"""
Demo Package - A sample Python package for PyPI publishing demonstration.

This package demonstrates how to create and publish a Python package to PyPI.
"""

__version__ = "0.1.0"
__author__ = "Chandra"
__email__ = "chandra385123@gmail.com"

from .calculator import Calculator
from .greeter import greet, greet_multiple

__all__ = ["Calculator", "greet", "greet_multiple"]
