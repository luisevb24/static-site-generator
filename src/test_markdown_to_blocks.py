import unittest
from markdown_to_blocks import  markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
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
    def test_markdown_to_blocks_single_block(self):
        markdown = "Hello world"
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, ["Hello world"])


    def test_markdown_to_blocks_multiple_blocks(self):
        markdown = "Block one\n\nBlock two\n\nBlock three"
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(
            blocks,
            ["Block one", "Block two", "Block three"],
        )


    def test_markdown_to_blocks_trims_whitespace(self):
        markdown = "  Block one  \n\n   Block two   "
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(
            blocks,
            ["Block one", "Block two"],
        )


    def test_markdown_to_blocks_ignores_empty_blocks(self):
        markdown = "Block one\n\n\n\nBlock two"
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(
            blocks,
            ["Block one", "Block two"],
        )


    def test_markdown_to_blocks_only_whitespace(self):
        markdown = "   \n\n   \n\n"
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, [])

        





if __name__ == "__main__":
    unittest.main()