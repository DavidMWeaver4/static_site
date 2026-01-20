class HTMLNode():
    def __init__(self, tag=None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Not implemented")
    def props_to_html(self):
        if self.props == None or self.props == {}:
            return ""
        return " "+ " ".join(f'{key}="{value}"' for key, value in self.props.items())

    def __repr__(self):
        return (f"tag={self.tag}, value={self.value}, children={self.children}, props={self.props}")

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props= None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("No value in LeafNode")
        if self.tag is None:
            return self.value
        props_html = ""
        if self.props:
            props_html = " " + " ".join(f'{key}="{value}"' for key, value in self.props.items())

        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"

    def __repr__(self):
        return (f"tag={self.tag}, value={self.value}, props={self.props}")

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode value error")
        if self.children is None:
            raise ValueError("ParentNode children error")
        child_html = ""
        for node in self.children:
            child_html += node.to_html()
        return f"<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>"
