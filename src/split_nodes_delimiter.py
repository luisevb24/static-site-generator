from textnode import TextType, TextNode
from extract_from_md import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        elif node.text_type == TextType.TEXT:
            result = node.text.split(delimiter)
            if len(result) % 2 == 0:
                raise Exception("Invalid markdown")
            result_nodes = []
            for i, part in enumerate(result):
                if part == "":
                    continue
                if i % 2 == 0: 
                    text_node = TextNode(part, TextType.TEXT)
                    result_nodes.append(text_node)
                if i % 2 != 0:
                    text_node = TextNode(part, text_type)
                    result_nodes.append(text_node)
            new_nodes.extend(result_nodes)
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else: 
            extraction = extract_markdown_images(node.text)
            if len(extraction) == 0:
                new_nodes.append(node)
            else:
                current_text = node.text
                for image_alt, image_link in extraction:
                    image_markdown = f"![{image_alt}]({image_link})"
                    sections = current_text.split(image_markdown, 1)
                    before = sections[0]
                    after = sections[1]
                    if before != "":
                        new_nodes.append(TextNode(before, TextType.TEXT))
                    new_nodes.append(TextNode(image_alt, TextType.IMAGES, image_link))
                    current_text = after
                if current_text != "":
                    new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else: 
            extraction = extract_markdown_links(node.text)
            if len(extraction) == 0:
                new_nodes.append(node)
            else:
                current_text = node.text
                for link_anchor, link in extraction:
                    link_markdown = f"[{link_anchor}]({link})"
                    sections = current_text.split(link_markdown, 1)
                    before = sections[0]
                    after = sections[1]
                    if before != "":
                        new_nodes.append(TextNode(before, TextType.TEXT))
                    new_nodes.append(TextNode(link_anchor, TextType.LINKS, link))
                    current_text = after
                if current_text != "":
                    new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes
        