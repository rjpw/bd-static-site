import re
from textnode import TextNode, TextType
from leafnode import LeafNode

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def markdown_to_blocks(markdown):
    """
    Breaks a markdown document into blocks based on blank lines (i.e. '\n\n').
    
    :param markdown: Raw markdown document
    """

    # raw array from markdown
    raw_blocks = markdown.split('\n\n')
    clean_blocks = []
    for block in raw_blocks:
        clean_blocks.append(block.strip())
    return clean_blocks

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text, None)
        case TextType.BOLD:
            return LeafNode("b", text_node.text, text_node.props)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text, text_node.props)
        case TextType.CODE:
            return LeafNode("code", text_node.text, text_node.props)
        case TextType.LINK:
            props = {}
            props["href"] = text_node.url
            return LeafNode("a", text_node.text, props)
        case TextType.IMAGE:
            props = {}
            props["src"] = text_node.url
            props["alt"] = text_node.text
            return LeafNode("img", "", props)
        case _:
            raise Exception("unknown text type")
        
def text_type_from_delimiter(delimiter):
    match delimiter:
        case '**':
            return TextType.BOLD
        case '`':
            return TextType.CODE
        case '_':
            return TextType.ITALIC
        case _:
            raise Exception("unsupported delimiter")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:

        # skip nodes that have already been processed and converted
        if not node.text_type == TextType.TEXT:
            new_nodes.append(node)
        else:

            segments = node.text.split(delimiter)

            # we should have an odd number greater than or equal to 3
            if len(segments) >= 3 and len(segments) % 2 == 1:
                in_delimited_segment = False
                for segment in segments:
                    if len(segment) > 0:
                        text_node = TextNode(segment, text_type if in_delimited_segment else TextType.TEXT)
                        new_nodes.append(text_node)
                    in_delimited_segment = not in_delimited_segment
            elif len(segments) == 1:
                # handle text nodes that don't have the delimiter
                new_nodes.append(TextNode(segments[0], TextType.TEXT))
            else:
                raise Exception("unmatched delimiters")

    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:

        if not node.text_type == TextType.TEXT:
            new_nodes.append(node)
        else:

            text = node.text
            image_matches = extract_markdown_images(text)

            while len(image_matches) > 0:

                image_alt, image_link = image_matches[0]
                sections = text.split(f"![{image_alt}]({image_link})", 1)

                # at this point we have only what does NOT have the image link
                if len(sections[0]) > 0:
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))

                # get the remainder, and find images in it
                text = sections[1]
                image_matches = extract_markdown_images(text)

            if len(text) > 0:
                new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):

    new_nodes = []

    for node in old_nodes:

        if not node.text_type == TextType.TEXT:
            new_nodes.append(node)
        else:
            
            text = node.text
            link_matches = extract_markdown_links(text)

            while len(link_matches) > 0:

                link_text, link_href = link_matches[0]
                sections = text.split(f"[{link_text}]({link_href})", 1)

                #print(f"sections: {sections}, link_text: {link_text}, link_href {link_href}")

                # at this point we have only what does NOT have a link
                if len(sections[0]) > 0:
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(link_text, TextType.LINK, link_href))

                # get the remainder, and find any links in it
                text = sections[1]
                link_matches = extract_markdown_links(text)

            if len(text) > 0:
                new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):

    node = TextNode(text, TextType.TEXT)
    bold_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
    code_nodes = split_nodes_delimiter(bold_nodes, '`', TextType.CODE)
    italic_nodes = split_nodes_delimiter(code_nodes, '_', TextType.ITALIC)
    image_nodes = split_nodes_image(italic_nodes)
    new_nodes = split_nodes_link(image_nodes)

    return new_nodes
