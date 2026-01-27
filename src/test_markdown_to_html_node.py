import unittest
from markdown_to_html_node import markdown_to_html_node


class TestMarkdownToHtml(unittest.TestCase):
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

    def test_markdown_to_html_node_empty(self):
        node = markdown_to_html_node("")
        self.assertEqual(node.to_html(), "<div></div>")


    def test_markdown_to_html_node_paragraph_single_line(self):
        md = "Hello world"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><p>Hello world</p></div>")


    def test_markdown_to_html_node_paragraph_multiline_collapses_to_spaces(self):
        md = "Hello\nworld\n\nNext"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><p>Hello world</p><p>Next</p></div>",
        )


    def test_markdown_to_html_node_heading_h1(self):
        md = "# Title"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><h1>Title</h1></div>")


    def test_markdown_to_html_node_heading_h4(self):
        md = "#### Title"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><h4>Title</h4></div>")


    def test_markdown_to_html_node_quote(self):
        md = "> quote line 1\n> quote line 2"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><blockquote>quote line 1 quote line 2</blockquote></div>",
        )


    def test_markdown_to_html_node_code_block(self):
        md = "```\n    print('hi')\n  x = 1\n```"
        node = markdown_to_html_node(md)
        # lstrip() en cada línea interna + siempre añade "\n" al final
        self.assertEqual(
            node.to_html(),
            "<div><pre><code>print('hi')\nx = 1\n</code></pre></div>",
        )


    def test_markdown_to_html_node_unordered_list(self):
        md = "- one\n- two\n- three"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul><li>one</li><li>two</li><li>three</li></ul></div>",
        )


    def test_markdown_to_html_node_ordered_list(self):
        md = "1. one\n2. two\n3. three"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ol><li>one</li><li>two</li><li>three</li></ol></div>",
        )


    def test_markdown_to_html_node_inline_formatting_in_paragraph(self):
        md = "This is **bold** and _italic_ and `code`."
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><p>This is <b>bold</b> and <i>italic</i> and <code>code</code>.</p></div>",
        )
