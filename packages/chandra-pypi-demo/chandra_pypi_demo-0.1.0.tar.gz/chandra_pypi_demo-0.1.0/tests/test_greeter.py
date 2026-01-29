"""
Tests for the greeter functions.
"""

import unittest
from demo_package import greet, greet_multiple


class TestGreeter(unittest.TestCase):
    """Test cases for greeter functions."""
    
    def test_greet_default(self):
        """Test greet with default greeting."""
        self.assertEqual(greet("Alice"), "Hello, Alice!")
        self.assertEqual(greet("Bob"), "Hello, Bob!")
    
    def test_greet_custom(self):
        """Test greet with custom greeting."""
        self.assertEqual(greet("Alice", "Hi"), "Hi, Alice!")
        self.assertEqual(greet("Bob", "Good morning"), "Good morning, Bob!")
    
    def test_greet_multiple_empty(self):
        """Test greet_multiple with empty list."""
        self.assertEqual(greet_multiple([]), "Hello!")
    
    def test_greet_multiple_single(self):
        """Test greet_multiple with single name."""
        self.assertEqual(greet_multiple(["Alice"]), "Hello, Alice!")
    
    def test_greet_multiple_two(self):
        """Test greet_multiple with two names."""
        self.assertEqual(greet_multiple(["Alice", "Bob"]), "Hello, Alice and Bob!")
    
    def test_greet_multiple_three_plus(self):
        """Test greet_multiple with three or more names."""
        self.assertEqual(
            greet_multiple(["Alice", "Bob", "Charlie"]),
            "Hello, Alice, Bob, and Charlie!"
        )
        self.assertEqual(
            greet_multiple(["Alice", "Bob", "Charlie", "David"]),
            "Hello, Alice, Bob, Charlie, and David!"
        )


if __name__ == "__main__":
    unittest.main()
