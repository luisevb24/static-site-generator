import os
from markdown_to_html_node import markdown_to_html_node
from extract_title import extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Normaliza paths a absolutos (relativos al archivo actual)
    from_abs = from_path if os.path.isabs(from_path) else os.path.join(base_dir, from_path)
    template_abs = template_path if os.path.isabs(template_path) else os.path.join(base_dir, template_path)
    dest_abs = dest_path if os.path.isabs(dest_path) else os.path.join(base_dir, dest_path)

    # Lee archivos
    with open(from_abs, "r", encoding="utf-8") as f:
        md_content = f.read()

    with open(template_abs, "r", encoding="utf-8") as f:
        template_content = f.read()

    # Convierte markdown -> HTML
    html_node = markdown_to_html_node(md_content)
    html_string = html_node.to_html()        
    html_title = extract_title(md_content)

    # Inyecta en template (reasignando)
    template_content = template_content.replace("{{ Title }}", html_title)
    template_content = template_content.replace("{{ Content }}", html_string)

    # Crea el directorio destino (padre)
    dest_dir = os.path.dirname(dest_abs)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    # Escribe archivo final
    with open(dest_abs, "w", encoding="utf-8") as f:
        f.write(template_content)
