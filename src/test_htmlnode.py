import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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


if __name__ == "__main__":
    unittest.main()
