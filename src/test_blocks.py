import unittest
from block_to_block_type import block_to_block_type, BlockType

class TestHTMLNode(unittest.TestCase):
    def test_heading_h1(self):
        self.assertEqual(block_to_block_type("# Hello"), BlockType.HEADING)

    def test_heading_h6(self):
        self.assertEqual(block_to_block_type("###### Hello"), BlockType.HEADING)

    def test_heading_requires_space_after_hashes(self):
        self.assertEqual(block_to_block_type("##Hello"), BlockType.PARAGRAPH)

    def test_heading_more_than_6_hashes_is_not_heading(self):
        self.assertEqual(block_to_block_type("####### Too many"), BlockType.PARAGRAPH)

    # --- Code blocks ---
    def test_code_block_multiline(self):
        md = "```\nprint('hi')\nprint('bye')\n```"
        self.assertEqual(block_to_block_type(md), BlockType.CODE)

    def test_code_block_requires_newline_after_backticks(self):
        md = "```print('hi')\n```"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_code_block_requires_closing_backticks(self):
        md = "```\nprint('hi')\n"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    # --- Quote blocks ---
    def test_quote_single_line(self):
        self.assertEqual(block_to_block_type("> quoted"), BlockType.QUOTE)

    def test_quote_multi_line_all_lines_must_start_with_gt_space(self):
        md = "> line 1\n> line 2\n> line 3"
        self.assertEqual(block_to_block_type(md), BlockType.QUOTE)

    def test_quote_fails_if_any_line_missing_prefix(self):
        md = "> line 1\nline 2"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    # --- Unordered lists ---
    def test_unordered_list_single_line(self):
        self.assertEqual(block_to_block_type("- item"), BlockType.UNORDERED_LIST)

    def test_unordered_list_multi_line(self):
        md = "- item 1\n- item 2\n- item 3"
        self.assertEqual(block_to_block_type(md), BlockType.UNORDERED_LIST)

    def test_unordered_list_fails_if_any_line_missing_prefix(self):
        md = "- item 1\nitem 2"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    # --- Ordered lists ---
    def test_ordered_list_single_line_must_start_at_1(self):
        self.assertEqual(block_to_block_type("1. item"), BlockType.ORDERED_LIST)

    def test_ordered_list_multi_line_increments_by_one(self):
        md = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(md), BlockType.ORDERED_LIST)

    def test_ordered_list_fails_if_not_starting_at_1(self):
        md = "2. first\n3. second"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_ordered_list_fails_if_numbers_do_not_increment(self):
        md = "1. first\n3. third"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_ordered_list_fails_if_missing_dot_space_format(self):
        md = "1) first\n2) second"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_ordered_list_allows_two_digit_numbers_if_sequence_is_correct(self):
        md = "\n".join([f"{i}. item" for i in range(1, 13)])  # 1..12
        self.assertEqual(block_to_block_type(md), BlockType.ORDERED_LIST)

    # --- Paragraph fallback ---
    def test_paragraph_default(self):
        md = "This is a normal paragraph.\nStill the same paragraph line."
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_empty_block_treated_as_paragraph(self):
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()