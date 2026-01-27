import unittest

from textnode import TextNode, TextType
from text_node_to_html_node import text_node_to_html_node
from split_nodes_delimiter import *
from extract_from_md import *
from markdown_to_blocks import markdown_to_blocks


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a link node", TextType.LINKS, "boot.dev")
        node2 = TextNode("This is a link node", TextType.IMAGES, "boot.dev")
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a link node", TextType.LINKS)
        node2 = TextNode("This is a link node", TextType.IMAGES)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_text_node_to_html_node_text(self):
        text_node = TextNode("hello", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "hello")


    def test_text_node_to_html_node_bold(self):
        text_node = TextNode("hello", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<b>hello</b>")


    def test_text_node_to_html_node_italic(self):
        text_node = TextNode("hello", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<i>hello</i>")


    def test_text_node_to_html_node_link(self):
        text_node = TextNode("OpenAI", TextType.LINKS, "https://openai.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(
            html_node.to_html(),
            '<a href="https://openai.com">OpenAI</a>',
        )


    def test_text_node_to_html_node_image(self):
        text_node = TextNode("kitten", TextType.IMAGES, "https://example.com/kitten.png")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(
            html_node.to_html(),
            '<img src="https://example.com/kitten.png" alt="kitten"></img>',
        )
    def test_split_nodes_delimiter_non_text_nodes_unchanged(self):
        old_nodes = [TextNode("already bold", TextType.BOLD)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, old_nodes)


    def test_split_nodes_delimiter_single_delimited_section(self):
        old_nodes = [TextNode("Hello **world**!", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

        self.assertEqual(
            new_nodes,
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("world", TextType.BOLD),
                TextNode("!", TextType.TEXT),
            ],
        )


    def test_split_nodes_delimiter_multiple_delimited_sections(self):
        old_nodes = [TextNode("a **b** c **d** e", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

        self.assertEqual(
            new_nodes,
            [
                TextNode("a ", TextType.TEXT),
                TextNode("b", TextType.BOLD),
                TextNode(" c ", TextType.TEXT),
                TextNode("d", TextType.BOLD),
                TextNode(" e", TextType.TEXT),
            ],
        )


    def test_split_nodes_delimiter_keeps_other_nodes_and_splits_text_node(self):
        old_nodes = [
            TextNode("start **mid** end", TextType.TEXT),
            TextNode("stay italic", TextType.ITALIC),
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

        self.assertEqual(
            new_nodes,
            [
                TextNode("start ", TextType.TEXT),
                TextNode("mid", TextType.BOLD),
                TextNode(" end", TextType.TEXT),
                TextNode("stay italic", TextType.ITALIC),
            ],
        )


    def test_split_nodes_delimiter_raises_on_invalid_markdown_even_splits(self):
        old_nodes = [TextNode("Hello **world", TextType.TEXT)]  # missing closing **
        with self.assertRaises(Exception):
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_images_single(self):
        text = "Here is an image ![alt text](https://example.com/img.png)"
        self.assertEqual(
            extract_markdown_images(text),
            [("alt text", "https://example.com/img.png")],
        )


    def test_extract_markdown_images_multiple(self):
        text = "![a](u1.png) and ![b](u2.jpg)"
        self.assertEqual(
            extract_markdown_images(text),
            [("a", "u1.png"), ("b", "u2.jpg")],
        )


    def test_extract_markdown_links_single(self):
        text = "This is a [link](https://example.com) in text."
        self.assertEqual(
            extract_markdown_links(text),
            [("link", "https://example.com")],
        )


    def test_extract_markdown_links_multiple(self):
        text = "[one](u1) blah [two](u2) end"
        self.assertEqual(
            extract_markdown_links(text),
            [("one", "u1"), ("two", "u2")],
        )


    def test_extract_markdown_links_ignores_images(self):
        text = "![img](img.png) and [site](https://example.com)"
        self.assertEqual(
            extract_markdown_links(text),
            [("site", "https://example.com")],
        )
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGES, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()