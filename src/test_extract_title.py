import unittest
from extract_title import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title_simple(self):
        md = "# Hello World"
        title = extract_title(md)
        self.assertEqual(title, "Hello World")


    def test_extract_title_ignores_non_h1_headings(self):
        md = "## Subtitle\n# Real Title"
        title = extract_title(md)
        self.assertEqual(title, "Real Title")


    def test_extract_title_ignores_text_before_title(self):
        md = "Some intro text\n\n# My Title\nMore text"
        title = extract_title(md)
        self.assertEqual(title, "My Title")


    def test_extract_title_first_valid_title_is_used(self):
        md = "# First Title\n# Second Title"
        title = extract_title(md)
        self.assertEqual(title, "First Title")


    def test_extract_title_raises_if_not_found(self):
        md = "No title here\n## Subtitle only"
        with self.assertRaises(Exception):
            extract_title(md)
