import os
from generate_page import generate_page

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    contents = os.listdir(dir_path_content)

    for item in contents:
        full_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(full_path) and item.lower().endswith(".md"):
            # cambiar .md -> .html
            dest_path = os.path.splitext(dest_path)[0] + ".html"
            generate_page(full_path, template_path, dest_path)

        elif os.path.isdir(full_path):
            generate_pages_recursive(full_path, template_path, dest_path)
