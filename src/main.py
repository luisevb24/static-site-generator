from textnode import TextNode, TextType
from source_to_destination_directory import source_to_destination_directory
from generate_pages_recursive import generate_pages_recursive
import os
from markdown_to_blocks import markdown_to_blocks
from block_to_block_type import block_to_block_type
import sys


print("Hello world")

def main():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    basepath = ""
    if len(sys.argv) < 2:
        basepath = "/"
    else:
        basepath = sys.argv[1]
    

    static_dir = os.path.join(BASE_DIR, "..", "static")
    public_dir = os.path.join(BASE_DIR, "..", "docs")
    index_dir = os.path.join(BASE_DIR, "..", "content")
    tem_dir = os.path.join(BASE_DIR, "..", "template.html")
    write_dir = os.path.join(BASE_DIR, "..", "docs")
    source_to_destination_directory(static_dir, public_dir)
    generate_pages_recursive(index_dir, tem_dir, write_dir, basepath)

main()
