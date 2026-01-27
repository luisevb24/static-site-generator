from split_nodes_delimiter import *

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    nodes = split_nodes_link(split_nodes_image(split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter([node], "_", TextType.ITALIC), "**", TextType.BOLD), "`", TextType.CODE)))
    return nodes