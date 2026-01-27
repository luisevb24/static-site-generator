class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        formatted_string = ""
        if self.props is None:
            return ""
        for key, value in self.props.items():
            formatted_string += f' {key}="{value}"'
        return formatted_string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return f"{self.value}"
        props = self.props_to_html()
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("Every ParentNode must have a tag")
        if self.children == None:
            raise ValueError("Every ParentNode must have children")
        child_nodes = []
        for child in self.children:
            child_nodes.append(child.to_html())
        props = self.props_to_html()
        child_nodes_html = "".join(child_nodes)
        return f"<{self.tag}{props}>{child_nodes_html}</{self.tag}>"