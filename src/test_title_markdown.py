import unittest

from extracttitle import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_h1_title(self):
        md = "# My Title\nSome content"
        self.assertEqual(extract_title(md), "My Title")

    def test_h1_with_spaces(self):
        md = "   #   My Title   \nContent"
        self.assertEqual(extract_title(md), "My Title")

    def test_h2_before_h1(self):
        md = "## Subtitle\n# Main Title\nContent"
        self.assertEqual(extract_title(md), "Main Title")

    def test_no_h1(self):
        md = "## Subtitle\nSome content"
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertEqual(str(context.exception), "No title found in markdown")

    def test_empty_markdown(self):
        md = ""
        with self.assertRaises(Exception):
            extract_title(md)

    def test_h1_no_space(self):
        md = "#Title\nContent"
        self.assertEqual(extract_title(md), "Title")

    def test_h1_only_hash(self):
        md = "#\nContent"
        self.assertEqual(extract_title(md), "")

    def test_text_before_h1(self):
        md = "Intro text\n# Real Title\nMore"
        self.assertEqual(extract_title(md), "Real Title")

if __name__ == "__main__":
    unittest.main()
