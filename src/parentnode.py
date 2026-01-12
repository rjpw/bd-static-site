from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("missing node tag")
        if not self.children:
            raise ValueError("parent tag must have children")
        
        inner_html = ""
        for child in self.children:
            inner_html += child.to_html()

        props_string = "" if not self.props else self.props_to_html()

        return f"<{self.tag}{props_string}>{inner_html}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"