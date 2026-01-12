import unittest

from textnode import TextNode
from markdown_conversion import *
from markdown_enums import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
        
    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_missing_url_matters(self):
        node = TextNode("alt", TextType.LINK, None)
        node2 = TextNode("alt", TextType.LINK, "https://boot.dev")
        self.assertNotEqual(node, node2)

    def test_alt_text_matters(self):
        node = TextNode("alt", TextType.LINK)
        node2 = TextNode("alt alt", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_a_from_text(self):
        node = TextNode("anchor text", TextType.LINK, url="http://example.com/")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "anchor text")
        self.assertEqual(html_node.to_html(), '<a href="http://example.com/">anchor text</a>')

    def test_img_from_text(self):
        node = TextNode("alt text", TextType.IMAGE, url="http://example.com/images/logo.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.to_html(), '<img alt="alt text" src="http://example.com/images/logo.png"></img>')

    def test_split_nodes_for_bold(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_nodes_with_italics(self):
        node = TextNode("This is text with an _italic phrase_ and then _another one_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected_nodes = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic phrase", TextType.ITALIC),
            TextNode(" and then ", TextType.TEXT),
            TextNode("another one", TextType.ITALIC),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_nodes_for_code(self):
        node = TextNode('JSON: `{"foo": "bar"}`', TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '`', TextType.CODE)
        expected_nodes = [
            TextNode("JSON: ", TextType.TEXT),
            TextNode('{"foo": "bar"}', TextType.CODE),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

if __name__ == "__main__":
    unittest.main()