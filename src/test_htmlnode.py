import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from split_nodes import split_nodes_delimiter


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_many_props(self):
        node = HTMLNode(
            "a",
            "google",
            None,
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"',
        )

    def test_props_to_html_no_props_none(self):
        node = HTMLNode("a", "google", None, None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_no_props_empty_dict(self):
        node = HTMLNode("a", "google", None, {})
        self.assertEqual(node.props_to_html(), "")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Value")
        self.assertEqual(node.to_html(), "Value")

    def test_leaf_to_html_no_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode("a", None, None)
            node.to_html()

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
    def test_to_html_with_no_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode("a", None, None)
            node.to_html()

    def test_to_html_with_no_value_p(self):
        with self.assertRaises(ValueError):
            child_node = LeafNode("span", "child")
            node = ParentNode(None, [child_node], None)
            node.to_html()

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_error(self):
        with self.assertRaises(Exception):
            node = TextNode("This is fucking stupid", TextType.IMG)
            html_node = text_node_to_html_node(node)

    def test_split_w_delimi(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_split_w_delimi_inv_type(self):
        with self.assertRaises(Exception):
            node = TextNode("This is text", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "**", TextType.IMG)


if __name__ == "__main__":
    unittest.main()
