#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from array import array
import unittest
from double_preceding4 import double_preceding

class TestDoublePreceding(unittest.TestCase):
    """Tests for double_preceding function.""" 

    def test_already_arranged(self):
        """Test with already arranged values.""" 
        argument = array('i', [5, 10, 15])
        expected = array('i', [0, 10, 20])
        double_preceding(argument)
        self.assertEqual(expected, argument)

    def test_identical(self):
        """Test with multiple identical values.""" 
        argument = array('i', [0, 1, 1])
        expected = array('i', [0, 0, 2])
        double_preceding(argument)
        self.assertEqual(expected, argument)

    def test_empty(self):
        """Test with an empty array."""
        argument = []
        expected = []
        double_preceding(argument)
        self.assertEqual(expected, argument)

if __name__ == "__main__":
    unittest.main()