"""Tests for spintax-py library"""

import unittest
from spintaxpy import parse, count, choose, spintax_range


class TestRange(unittest.TestCase):
    """Test range generator"""
    
    def test_basic_range(self):
        """Test basic range from 1 to 5"""
        result = list(spintax_range(1, 5))
        self.assertEqual(result, [1, 2, 3, 4, 5])
    
    def test_range_with_step(self):
        """Test range with step"""
        result = list(spintax_range(0, 10, 2))
        self.assertEqual(result, [0, 2, 4, 6, 8, 10])
    
    def test_range_with_step_include_end(self):
        """Test range with step that includes end value"""
        result = list(spintax_range(0, 10, 3, True))
        self.assertEqual(result, [0, 3, 6, 9, 10])


class TestParse(unittest.TestCase):
    """Test parse function"""
    
    def test_no_patterns(self):
        """Test template with no patterns"""
        result = list(parse("Hello, world!"))
        self.assertEqual(result, ["Hello, world!"])
    
    def test_basic_choices(self):
        """Test basic choices pattern"""
        result = list(parse("Hello, {world|friend|universe}!"))
        expected = ["Hello, world!", "Hello, friend!", "Hello, universe!"]
        self.assertEqual(result, expected)
    
    def test_basic_range(self):
        """Test basic range pattern"""
        result = list(parse("Count: {1,5}"))
        expected = ["Count: 1", "Count: 2", "Count: 3", "Count: 4", "Count: 5"]
        self.assertEqual(result, expected)
    
    def test_range_with_step(self):
        """Test range pattern with step"""
        result = list(parse("Value: {0,10,2}"))
        expected = ["Value: 0", "Value: 2", "Value: 4", "Value: 6", "Value: 8", "Value: 10"]
        self.assertEqual(result, expected)
    
    def test_multiple_patterns(self):
        """Test multiple patterns in template"""
        result = list(parse("{small|large} {box|circle}"))
        expected = [
            "small box",
            "small circle",
            "large box",
            "large circle"
        ]
        self.assertEqual(result, expected)
    
    def test_three_patterns(self):
        """Test three patterns combination"""
        result = list(parse("{small|large} {box|circle} in {red|blue}"))
        self.assertEqual(len(result), 8)
        self.assertIn("small box in red", result)
        self.assertIn("large circle in blue", result)
    
    def test_back_reference(self):
        """Test back reference pattern"""
        result = list(parse("The {blue|straw|rasp}berries taste like {$0}berries"))
        expected = [
            "The blueberries taste like blueberries",
            "The strawberries taste like strawberries",
            "The raspberries taste like raspberries"
        ]
        self.assertEqual(result, expected)
    
    def test_whitespace_in_range(self):
        """Test that whitespace is ignored in range patterns"""
        result = list(parse("Value: { 1, 5 }"))
        expected = ["Value: 1", "Value: 2", "Value: 3", "Value: 4", "Value: 5"]
        self.assertEqual(result, expected)
    
    def test_whitespace_in_choices(self):
        """Test that whitespace is preserved in choices"""
        result = list(parse("{option1 |option2}"))
        expected = ["option1 ", "option2"]
        self.assertEqual(result, expected)
    
    def test_url_generation(self):
        """Test URL generation"""
        result = list(parse("https://example.com/{products|users}/{1,3}"))
        expected = [
            "https://example.com/products/1",
            "https://example.com/products/2",
            "https://example.com/products/3",
            "https://example.com/users/1",
            "https://example.com/users/2",
            "https://example.com/users/3"
        ]
        self.assertEqual(result, expected)


class TestCount(unittest.TestCase):
    """Test count function"""
    
    def test_count_no_patterns(self):
        """Test count with no patterns"""
        result = count("Hello!")
        self.assertEqual(result, 1)
    
    def test_count_basic_choices(self):
        """Test count with basic choices"""
        result = count("Hello {world|people|nurse}!")
        self.assertEqual(result, 3)
    
    def test_count_range(self):
        """Test count with range pattern"""
        result = count("Count: {1,5}")
        self.assertEqual(result, 5)
    
    def test_count_multiple_patterns(self):
        """Test count with multiple patterns"""
        result = count("{small|large} {box|circle}")
        self.assertEqual(result, 4)
    
    def test_count_with_back_reference(self):
        """Test count with back reference (shouldn't multiply)"""
        result = count("The {blue|straw|rasp}berries taste like {$0}berries")
        self.assertEqual(result, 3)


class TestChoose(unittest.TestCase):
    """Test choose function"""
    
    def test_choose_specific_index(self):
        """Test choose with specific indices"""
        picker = choose("Hello {world|nurse}!")
        result1 = picker(0)
        result2 = picker(1)
        self.assertEqual(result1, "Hello world!")
        self.assertEqual(result2, "Hello nurse!")
    
    def test_choose_multiple_patterns(self):
        """Test choose with multiple patterns"""
        picker = choose("The {red|blue|green} {box|circle}")
        result = picker(0, 1)
        self.assertEqual(result, "The red circle")
        
        result = picker(2, 0)
        self.assertEqual(result, "The green box")
    
    def test_choose_random(self):
        """Test choose with random selection"""
        picker = choose("Hello {world|universe}!")
        result = picker()
        self.assertIn(result, ["Hello world!", "Hello universe!"])
    
    def test_choose_with_back_reference(self):
        """Test choose with back reference"""
        picker = choose("The {blue|straw}berries taste like {$0}berries")
        result = picker(0)
        self.assertEqual(result, "The blueberries taste like blueberries")
        
        result = picker(1)
        self.assertEqual(result, "The strawberries taste like strawberries")


class TestIteration(unittest.TestCase):
    """Test iteration order"""
    
    def test_iteration_order(self):
        """Test that rightmost pattern is iterated first"""
        result = list(parse("{A|B} {1|2}"))
        expected = [
            "A 1",
            "A 2",
            "B 1",
            "B 2"
        ]
        self.assertEqual(result, expected)
    
    def test_iteration_order_three_patterns(self):
        """Test iteration order with three patterns"""
        result = list(parse("The color is {red|green|blue}. The letter is {A|B|C}"))
        expected = [
            "The color is red. The letter is A",
            "The color is red. The letter is B",
            "The color is red. The letter is C",
            "The color is green. The letter is A",
            "The color is green. The letter is B",
            "The color is green. The letter is C",
            "The color is blue. The letter is A",
            "The color is blue. The letter is B",
            "The color is blue. The letter is C"
        ]
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
