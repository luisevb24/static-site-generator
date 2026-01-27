import unittest

from textnode import TextNode, TextType
from text_node_to_html_node import text_node_to_html_node
from split_nodes_delimiter import *
from extract_from_md import *
from text_to_textnodes import text_to_textnodes

class TestSplitter(unittest.TestCase):
    # ---------- split_nodes_image (5) ----------

    def test_split_nodes_image_non_text_nodes_unchanged(self):
        old_nodes = [TextNode("bold", TextType.BOLD)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(new_nodes, old_nodes)


    def test_split_nodes_image_no_images_returns_original_node(self):
        old_nodes = [TextNode("just text here", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(new_nodes, old_nodes)


    def test_split_nodes_image_single_image_in_middle(self):
        old_nodes = [TextNode("Hello ![alt](img.png) world", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("alt", TextType.IMAGES, "img.png"),
                TextNode(" world", TextType.TEXT),
            ],
        )


    def test_split_nodes_image_image_at_start(self):
        old_nodes = [TextNode("![a](u1) tail", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(
            new_nodes,
            [
                TextNode("a", TextType.IMAGES, "u1"),
                TextNode(" tail", TextType.TEXT),
            ],
        )


    def test_split_nodes_image_multiple_images(self):
        old_nodes = [TextNode("x ![a](u1) y ![b](u2) z", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(
            new_nodes,
            [
                TextNode("x ", TextType.TEXT),
                TextNode("a", TextType.IMAGES, "u1"),
                TextNode(" y ", TextType.TEXT),
                TextNode("b", TextType.IMAGES, "u2"),
                TextNode(" z", TextType.TEXT),
            ],
        )


    # ---------- split_nodes_link (5) ----------

    def test_split_nodes_link_non_text_nodes_unchanged(self):
        old_nodes = [TextNode("italic", TextType.ITALIC)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertEqual(new_nodes, old_nodes)


    def test_split_nodes_link_no_links_returns_original_node(self):
        old_nodes = [TextNode("just text here", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertEqual(new_nodes, old_nodes)


    def test_split_nodes_link_single_link_in_middle(self):
        old_nodes = [TextNode("Go to [site](https://x.com) now", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Go to ", TextType.TEXT),
                TextNode("site", TextType.LINKS, "https://x.com"),
                TextNode(" now", TextType.TEXT),
            ],
        )


    def test_split_nodes_link_link_at_end(self):
        old_nodes = [TextNode("click [here](u1)", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertEqual(
            new_nodes,
            [
                TextNode("click ", TextType.TEXT),
                TextNode("here", TextType.LINKS, "u1"),
            ],
        )


    def test_split_nodes_link_multiple_links(self):
        old_nodes = [TextNode("a [one](u1) b [two](u2) c", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertEqual(
            new_nodes,
            [
                TextNode("a ", TextType.TEXT),
                TextNode("one", TextType.LINKS, "u1"),
                TextNode(" b ", TextType.TEXT),
                TextNode("two", TextType.LINKS, "u2"),
                TextNode(" c", TextType.TEXT),
            ],
        )

    def test_text_to_textnodes_plain_text(self):
        nodes = text_to_textnodes("hello world")
        self.assertEqual(nodes, [TextNode("hello world", TextType.TEXT)])


    def test_text_to_textnodes_bold_only(self):
        nodes = text_to_textnodes("**bold**")
        self.assertEqual(nodes, [TextNode("bold", TextType.BOLD)])


    def test_text_to_textnodes_italic_only(self):
        nodes = text_to_textnodes("_italic_")
        self.assertEqual(nodes, [TextNode("italic", TextType.ITALIC)])


    def test_text_to_textnodes_code_only(self):
        nodes = text_to_textnodes("`code`")
        self.assertEqual(nodes, [TextNode("code", TextType.CODE)])


    def test_text_to_textnodes_bold_in_sentence(self):
        nodes = text_to_textnodes("Hello **world**!")
        self.assertEqual(
            nodes,
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("world", TextType.BOLD),
                TextNode("!", TextType.TEXT),
            ],
        )


    def test_text_to_textnodes_italic_in_sentence(self):
        nodes = text_to_textnodes("Hello _world_!")
        self.assertEqual(
            nodes,
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("world", TextType.ITALIC),
                TextNode("!", TextType.TEXT),
            ],
        )


    def test_text_to_textnodes_code_in_sentence(self):
        nodes = text_to_textnodes("Use `print()` please")
        self.assertEqual(
            nodes,
            [
                TextNode("Use ", TextType.TEXT),
                TextNode("print()", TextType.CODE),
                TextNode(" please", TextType.TEXT),
            ],
        )


    def test_text_to_textnodes_link_in_sentence(self):
        nodes = text_to_textnodes("Go to [site](https://x.com) now")
        self.assertEqual(
            nodes,
            [
                TextNode("Go to ", TextType.TEXT),
                TextNode("site", TextType.LINKS, "https://x.com"),
                TextNode(" now", TextType.TEXT),
            ],
        )


    def test_text_to_textnodes_image_in_sentence(self):
        nodes = text_to_textnodes("Look ![alt](img.png) ok")
        self.assertEqual(
            nodes,
            [
                TextNode("Look ", TextType.TEXT),
                TextNode("alt", TextType.IMAGES, "img.png"),
                TextNode(" ok", TextType.TEXT),
            ],
        )


    def test_text_to_textnodes_mixed_all_types(self):
        text = "A **b** _c_ `d` [e](u) ![f](img) Z"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("A ", TextType.TEXT),
                TextNode("b", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("c", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("d", TextType.CODE),
                TextNode(" ", TextType.TEXT),
                TextNode("e", TextType.LINKS, "u"),
                TextNode(" ", TextType.TEXT),
                TextNode("f", TextType.IMAGES, "img"),
                TextNode(" Z", TextType.TEXT),
            ],
        )


