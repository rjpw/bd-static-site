import os, re
from htmlnode import HTMLNode
from leafnode import LeafNode
from textnode import TextNode
from parentnode import ParentNode
from markdown_enums import TextType, BlockType

def is_header(block):
    matches = re.findall(r"^#{1,6} (.*)$", block)
    return len(matches) > 0

def is_codeblock(block):
    matches = re.findall(r"```\n(.*\n)+```", block, re.MULTILINE)
    return len(matches) > 0

def is_quoteblock(block):
    lines = block.strip().split('\n')
    matches = re.findall(r"> (.*)", block, re.MULTILINE)
    return len(lines) == len(matches)

def is_unordered_list(block):
    lines = block.strip().split('\n')
    matches = re.findall(r"- (.*)", block, re.MULTILINE)
    return len(lines) == len(matches)

def is_ordered_list(block):
    lines = block.strip().split('\n')
    matches = re.findall(r"(\d+)\. (.*)", block, re.MULTILINE)
    return len(lines) == len(matches)

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def extract_title(text):
    if is_header(text):
        header = get_header_from_block(text)
        if header.tag == 'h1' and header.value:
            return header.value
        else:
            raise Exception("Invalid title")
    else:
        raise Exception("Not a header")

def block_to_block_type(block):
    """

    Returns a BlockType for a given block.
    
    * Headings start with 1-6 # characters, followed by a space and then the heading text.
    * Multiline Code blocks must start with 3 backticks and a newline, then end with 3 backticks.
    * Every line in a quote block must start with a "greater-than" character and a space: >
    * Every line in an unordered list block must start with a - character, followed by a space.
    * Every line in an ordered list block must start with a number followed by a . character and a space. 
      The number must start at 1 and increment by 1 for each line.
    * If none of the above conditions are met, the block is a normal paragraph.
    
    :param block: Description
    """

    if is_header(block):
        return BlockType.HEADING
    elif is_codeblock(block):
        return BlockType.CODE
    elif is_quoteblock(block):
        return BlockType.QUOTE
    elif is_unordered_list(block):
        return BlockType.UNORDERED_LIST
    elif is_ordered_list(block):
        return BlockType.ORDERED_LIST
    elif is_ordered_list(block):
        return BlockType.ORDERED_LIST
    else:
        # return default the moment
        return BlockType.PARAGRAPH

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

def get_file_contents(file_path):
    with open(file_path, "r") as f:
        return f.read()

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {template_path} using {dest_path}")
    markdown = get_file_contents(from_path)
    template = get_file_contents(template_path)
    html_content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown_to_blocks(markdown)[0])
    page_content = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    with open(dest_path, "w") as f:
        f.write(page_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

    if not os.path.exists(dest_dir_path):
        # make the target directory (since we know it was removed)
        print(f"Creating target directory: {dest_dir_path}")
        os.mkdir(dest_dir_path)

    # find and copy source contents
    print(f"Crawling directory: {dir_path_content}")

    contents = os.listdir(dir_path_content)
    for item in contents:

        # print(f"item: {item}")
        source_subpath = os.path.join(dir_path_content, item)
        target_subpath = os.path.join(dest_dir_path, item)

        if os.path.isfile(source_subpath):
            print(f"found file: {source_subpath}")
            target_filename = item[:-3] + ".html"
            generate_page(source_subpath, template_path, os.path.join(dest_dir_path, target_filename))
        else:
            print(f"Recursing into {source_subpath}")
            generate_pages_recursive(source_subpath, template_path, target_subpath)

def get_header_from_block(block):
    matches = re.findall(r"^(#{1,6}) +(.*)$", block)
    if len(matches) == 0:
        raise Exception("No header detected")
    tag = f"h{len(matches[0][0])}"
    return LeafNode(tag, matches[0][1])

def get_codeblock_from_block(block):
    matches = re.findall(r"```\n(.*)```", block, re.DOTALL)
    codeblock = LeafNode("code", matches[0])
    preformat_node = ParentNode("pre", [codeblock])
    return preformat_node

def get_blockquote_from_block(block):
    matches = re.findall(r"> (.*)", block, re.MULTILINE)
    quoteblock = LeafNode("blockquote", "\n".join(matches))
    return quoteblock

def get_ul_from_block(block):
    matches = re.findall(r"- (.*)", block, re.MULTILINE)
    children = []
    for match in matches:
        text_nodes = text_to_textnodes(match)
        # print(f"text_nodes: {text_nodes}")
        leaf_nodes = []
        for node in text_nodes:
            leaf_nodes.append(text_node_to_html_node(node))
        children.append(ParentNode("li", leaf_nodes))
    return ParentNode("ul", children)

def get_ol_from_block(block):
    matches = re.findall(r"\d+\. (.*)", block, re.MULTILINE)
    children = []
    for match in matches:
        text_nodes = text_to_textnodes(match)
        # print(f"text_nodes: {text_nodes}")
        leaf_nodes = []
        for node in text_nodes:
            leaf_nodes.append(text_node_to_html_node(node))
        children.append(ParentNode("li", leaf_nodes))
    return ParentNode("ol", children)

def get_para_from_block(block):
    text_nodes = text_to_textnodes(block)
    leaf_nodes = []
    for node in text_nodes:
        leaf_nodes.append(text_node_to_html_node(node))
    return ParentNode("p", leaf_nodes)

def markdown_to_html_node(markdown):
    """
    Converts a markdown block to a parent ParentNode (i.e. a DIV)
    with recursively nested subnodes, each of the appropriate tag.
    
    :param markdown: Markdown text 
    """

    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:

        block_type = block_to_block_type(block)
        #print(f"\nDetected block type: {block_type} for block: {block[:20]}")

        match block_type:
            case BlockType.HEADING:
                children.append(get_header_from_block(block))
            case BlockType.CODE:
                children.append(get_codeblock_from_block(block))
            case BlockType.QUOTE:
                children.append(get_blockquote_from_block(block))
            case BlockType.UNORDERED_LIST:
                children.append(get_ul_from_block(block))
            case BlockType.ORDERED_LIST:
                children.append(get_ol_from_block(block))
            case BlockType.PARAGRAPH:
                children.append(get_para_from_block(block))
            case _:
                raise Exception("unexpected block type")
    
    # create a parent node and return it
    return ParentNode("div", children)


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
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

    # print(f"Nodes: {new_nodes}")

    return new_nodes
