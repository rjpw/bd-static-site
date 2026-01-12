import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_not_impl(self):
        node = HTMLNode("p")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        span = HTMLNode("span", "just some text",)
        node = HTMLNode("p", None, [span])
        node_string = node.__repr__()
        self.assertTrue(node_string, "HTMLNode(p, None, [HTMLNode(span, just some text, None, None)], None)")

    def test_prop_conversion(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode("a", "Google", None, props)
        prop_string = node.props_to_html()
        self.assertEqual(prop_string, ' href="https://www.google.com" target="_blank"')

if __name__ == "__main__":
    unittest.main()