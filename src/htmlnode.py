class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other):
        pass

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if len(self.props) == 0:
            return None
        props_string = ""
        for k in sorted(list(self.props.keys())):
            props_string += f' {k}="{self.props[k]}"'
        return props_string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"