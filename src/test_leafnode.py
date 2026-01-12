import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_a(self):
        node = LeafNode("a")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_repr(self):
        node = LeafNode("span", "just some text",)
        node_string = str(node)
        self.assertTrue(node_string, "LeafNode(span, just some text, None)")

    def test_prop_conversion(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = LeafNode("a", "Google", props)
        prop_string = node.props_to_html()
        self.assertEqual(prop_string, ' href="https://www.google.com" target="_blank"')

if __name__ == "__main__":
    unittest.main()