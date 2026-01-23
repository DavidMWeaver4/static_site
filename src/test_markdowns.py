import unittest

from markdown_blocks import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)


class TestTextNode(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_string(self):
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)

    def test_whitespace_only(self):
        self.assertEqual(block_to_block_type("   \n\t  "), BlockType.PARAGRAPH)

    def test_heading_without_space(self):
        # Missing space after #
        self.assertEqual(block_to_block_type("#Heading"), BlockType.PARAGRAPH)

    def test_heading_with_too_many_hashes(self):
        # More than 6 hashes should not match
        self.assertEqual(block_to_block_type("####### Heading"), BlockType.PARAGRAPH)

    def test_code_block_missing_closing_ticks(self):
        self.assertEqual(block_to_block_type("```\nprint('hi')"), BlockType.PARAGRAPH)

    def test_code_block_missing_opening_newline(self):
        # Must start with ```\n exactly
        self.assertEqual(block_to_block_type("```print('hi')```"), BlockType.PARAGRAPH)

    def test_code_block_with_extra_whitespace_around(self):
        # strip() should still allow detection
        self.assertEqual(block_to_block_type("  ```\ncode\n```  "), BlockType.CODE)

    def test_quote_without_space(self):
        # > must be followed by space
        self.assertEqual(block_to_block_type(">Quote"), BlockType.PARAGRAPH)

    def test_unordered_list_without_space(self):
        self.assertEqual(block_to_block_type("-item"), BlockType.PARAGRAPH)

    def test_ordered_list_without_space(self):
        self.assertEqual(block_to_block_type("1.item"), BlockType.PARAGRAPH)

    def test_ordered_list_non_numeric_prefix(self):
        self.assertEqual(block_to_block_type("one. item"), BlockType.PARAGRAPH)

    def test_multiple_lines_only_first_line_valid(self):
        # Only checks the start of the entire block
        text = "# Heading\nNot really a heading"
        self.assertEqual(block_to_block_type(text), BlockType.HEADING)

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()
