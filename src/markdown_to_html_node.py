from markdown_to_blocks import markdown_to_blocks
from block_to_block_type import block_to_block_type, BlockType
from htmlnode import HTMLNode, ParentNode, LeafNode
from text_to_textnodes import text_to_textnodes
from text_node_to_html_node import text_node_to_html_node


def markdown_to_html_node(markdown):
    parent_children = []
    parent = ParentNode("div", parent_children)

    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)
        tag = ""
        block_text = block
        if block_type == BlockType.HEADING:
            if block.startswith("######"):
                tag = "h6"
            elif block.startswith("#####"):
                tag = "h5"
            elif block.startswith("####"):
                tag = "h4"    
            elif block.startswith("###"):
                tag = "h3" 
            elif block.startswith("##"):
                tag = "h2"
            elif block.startswith("#"):
                tag = "h1"
            block_text = block.lstrip("#").strip()
        elif block_type == BlockType.PARAGRAPH:
            tag = "p"
            lines = block.splitlines()
            cleaned = [line.strip() for line in lines if line.strip()]
            block_text = " ".join(cleaned)
        elif block_type == BlockType.CODE:
            lines = block.split("\n")
            inner_lines = lines[1:-1]
            inner_lines = [line.lstrip() for line in inner_lines]
            block_text = "\n".join(inner_lines) + "\n"
            code_node = LeafNode("code", block_text)
            pre_node = ParentNode("pre", [code_node])
            parent_children.append(pre_node)
        elif block_type == BlockType.QUOTE:
            tag = "blockquote"
            lines = block.split("\n")
            stripped = []
            for line in lines:
                line = line.lstrip("> ").strip()
                if line:
                    stripped.append(line)
            block_text = " ".join(stripped)
        elif block_type == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            li_children = []
            for line in lines:
                line = line.strip()
                if not line:
                    continue 
                item_text = line[2:]
                children = text_to_children(item_text)
                li_node = ParentNode("li", children)
                li_children.append(li_node)
            ul_node = ParentNode("ul", li_children)
            parent_children.append(ul_node)
        elif block_type == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            li_children = []
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                dot_index = line.find(".")
                item_text = line[dot_index+1:].strip()
                children = text_to_children(item_text)
                li_node = ParentNode("li", children)
                li_children.append(li_node)
            ol_node = ParentNode("ol", li_children)
            parent_children.append(ol_node)

        if tag:
            block_children = text_to_children(block_text)
            html_node = ParentNode(tag, block_children)
            parent_children.append(html_node)

    return parent

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children