import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from split_nodes import split_nodes_delimiter, split_nodes_image
from extract_markdown import extract_markdown_images, extract_markdown_links
from text_to_textnode import text_to_textnodes

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_noteq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2  = TextNode("This is not a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    def test_url(self):
        node = TextNode("A", TextType.BOLD, None)
        node2 = TextNode("A", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_type(self):
        node = TextNode("A", TextType.BOLD, "https://www.boot.dev")
        node2 = TextNode("A", TextType.TEXT, "https://www.boot.dev")
        self.assertNotEqual(node, node2)


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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_extract_markdown_links_complex_urls(self):
        matches = extract_markdown_links("Check out [this search](https://www.google.com/search?q=python+regex) and [this section](https://docs.python.org/3/library/re.html#re.findall)")
        self.assertListEqual([("this search", "https://www.google.com/search?q=python+regex"),("this section", "https://docs.python.org/3/library/re.html#re.findall"),],matches,)

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_multiple(self):
        node = TextNode(
            "a ![one](url1) b ![two](url2) c",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("a ", TextType.TEXT),
                TextNode("one", TextType.IMAGE, "url1"),
                TextNode(" b ", TextType.TEXT),
                TextNode("two", TextType.IMAGE, "url2"),
                TextNode(" c", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        node = TextNode(
            "just plain text with no images",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("just plain text with no images", TextType.TEXT)],
            new_nodes,
        )


    def test_split_image_at_start(self):
        node = TextNode(
            "![start](url) after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start", TextType.IMAGE, "url"),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_split_image_at_end(self):
        node = TextNode(
            "before ![end](url)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("before ", TextType.TEXT),
                TextNode("end", TextType.IMAGE, "url"),
            ],
            new_nodes,
        )


    def test_split_adjacent_images(self):
        node = TextNode(
            "![one](url1)![two](url2)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("one", TextType.IMAGE, "url1"),
                TextNode("two", TextType.IMAGE, "url2"),
            ],
            new_nodes,
        )


    def test_split_image_empty_alt_text(self):
        node = TextNode(
            "text ![](url) more",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("text ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "url"),
                TextNode(" more", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_split_ignores_malformed_image(self):
        node = TextNode(
            "text ![broken](url more text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("text ![broken](url more text", TextType.TEXT)],
            new_nodes,
        )


    def test_split_multiple_nodes_input(self):
        nodes = [
            TextNode("a ![one](url1)", TextType.TEXT),
            TextNode(" middle ", TextType.TEXT),
            TextNode("![two](url2) b", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("a ", TextType.TEXT),
                TextNode("one", TextType.IMAGE, "url1"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("two", TextType.IMAGE, "url2"),
                TextNode(" b", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_non_text_node_passthrough(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("already bold", TextType.BOLD)],
            new_nodes,
        )

    def test_text_to_textnodes_links_and_images(self):
        text = "![alt](img.png)[boot](https://boot.dev)"
        nodes = text_to_textnodes(text)
        assert nodes == [
            TextNode("alt", TextType.IMAGE, "img.png"),
            TextNode("boot", TextType.LINK, "https://boot.dev"),
        ]

    def test_text_to_textnodes_plain_text_only(self):
        text = "Just a plain old sentence with nothing fancy."
        nodes = text_to_textnodes(text)
        assert nodes == [
            TextNode("Just a plain old sentence with nothing fancy.", TextType.TEXT),
        ]
if __name__ == "__main__":
    unittest.main()
