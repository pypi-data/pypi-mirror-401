import unittest
import sys
import io
from star import triangle, pyramid, diamond, arrow, right_triangle

class TestStarPatterns(unittest.TestCase):
    def setUp(self):
        # Redirect stdout to capture print output
        self.capturedOutput = io.StringIO()
        sys.stdout = self.capturedOutput

    def tearDown(self):
        # Reset redirection
        sys.stdout = sys.__stdout__

    def get_output(self):
        return self.capturedOutput.getvalue()

    def test_triangle_default(self):
        """Test triangle with default height (equals width)"""
        triangle(3)
        expected = "*\n**\n***\n"
        self.assertEqual(self.get_output(), expected)

    def test_triangle_custom_height(self):
        """Test triangle with custom height"""
        triangle(5, 3)
        expected = "*\n***\n*****\n"
        self.assertEqual(self.get_output(), expected)

    def test_pyramid(self):
        pyramid(3)
        expected = "  *\n ***\n*****\n"
        self.assertEqual(self.get_output(), expected)

    def test_diamond(self):
        diamond(3)
        expected = "  *\n ***\n*****\n ***\n  *\n"
        self.assertEqual(self.get_output(), expected)

    def test_arrow(self):
        arrow(3)
        expected = "*\n**\n***\n**\n*\n"
        self.assertEqual(self.get_output(), expected)

    def test_custom_char(self):
        triangle(2, char='#')
        expected = "#\n##\n"
        self.assertEqual(self.get_output(), expected)

    def test_right_triangle(self):
        right_triangle(3)
        expected = "  *\n **\n***\n"
        self.assertEqual(self.get_output(), expected)

if __name__ == '__main__':
    unittest.main()
