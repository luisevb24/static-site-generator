import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_returns_empty_string_when_props_is_none(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_to_html_raises_not_implemented_error(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_href(self):
        node = LeafNode(
            "a",
            "Click here",
            {"href": "https://example.com"}
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://example.com">Click here</a>'
        )



    def test_leaf_to_html_h1_with_class(self):
        node = LeafNode(
            "h1",
            "Title",
            {"class": "main-title"}
        )
        self.assertEqual(
            node.to_html(),
            '<h1 class="main-title">Title</h1>'
        )


    def test_leaf_to_html_span_with_multiple_props(self):
        node = LeafNode(
            "span",
            "Text",
            {"class": "highlight", "id": "msg"}
        )
        self.assertEqual(
            node.to_html(),
            '<span class="highlight" id="msg">Text</span>'
        )   
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container"><span>child</span></div>',
        )
    def test_to_html_no_tag_raises_error(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()
if __name__ == "__main__":
    unittest.main()
