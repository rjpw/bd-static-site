import unittest

from markdown_conversion import *
from markdown_enums import BlockType

class TestBlockType(unittest.TestCase):
    """
    Validates that blocks from this enum can be identified by
    markdown_conversion.block_to_block_type

        class BlockType(Enum):
            PARAGRAPH      
            HEADING        
            CODE           
            QUOTE          
            UNORDERED_LIST 
            ORDERED_LIST   

    """

    def test_default_blocktype(self):
        block = "This is just some text"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_h1(self):
        block = "# README"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_h6(self):
        block = "###### Some deeply nested paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_h7(self):
        block = "####### Too many hashes"
        self.assertNotEqual(block_to_block_type(block), BlockType.HEADING)
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_codeblock(self):
        block = """
```
def test_h7(self):
    block = "####### Too many hashes"
    self.assertNotEqual(block_to_block_type(block), BlockType.HEADING)
    self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
```
"""
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_can_identify_quoteblock(self):
        block = """
> Four score and seven years ago
> someone said something momentous
> and I must admit I forget the details
"""
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = """
- Four score and seven years ago
- someone said something momentous
- and I must admit I forget the details
"""
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list(self):
        block = """
1. Four score and seven years ago
2. someone said something momentous
3. and I must admit I forget the details
"""
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_can_get_header_from_block(self):
        block = "### This should be an H3 block"
        header = get_header_from_block(block)
        self.assertEqual(header.tag, "h3")

    def test_can_get_codeblock_from_block(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = get_codeblock_from_block(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre>",
        )

    def test_can_generate_blockquote(self):
        md = """
> Four score and seven years ago
> someone said something momentous
> and I must admit I forget the details
"""

        node = get_blockquote_from_block(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<blockquote>Four score and seven years ago\nsomeone said something momentous\nand I must admit I forget the details</blockquote>",
        )

    def test_codeblock_to_nodes(self):
        md = """
> "I am in fact a Hobbit in all but size."
> 
> -- J.R.R. Tolkien
"""

        node = get_blockquote_from_block(md)
        html = node.to_html()
        expected = '<blockquote>"I am in fact a Hobbit in all but size."\n\n-- J.R.R. Tolkien</blockquote>'

        self.assertEqual(
            html,
            expected,
        )
    

    def test_can_generate_ul(self):
        md = """
- Four score and seven years ago
- someone said something momentous
- and I must admit I forget the details
"""

        node = get_ul_from_block(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<ul><li>Four score and seven years ago</li><li>someone said something momentous</li><li>and I must admit I forget the details</li></ul>",
        )

    def test_can_generate_ol(self):
        md = """
1. Four score and seven years ago
1. someone said something momentous
1. and I must admit I forget the details
"""

        node = get_ol_from_block(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<ol><li>Four score and seven years ago</li><li>someone said something momentous</li><li>and I must admit I forget the details</li></ol>",
        )

