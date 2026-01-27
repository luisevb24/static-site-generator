import os
import shutil

def source_to_destination_directory(source, destination):
    source = os.path.abspath(source)
    destination = os.path.abspath(destination)

    # 1) Asegurar que destination exista (con padres)
    os.makedirs(destination, exist_ok=True)

    # 2) Limpiar SOLO el contenido de este destination (no borra destination en sí)
    for item in os.listdir(destination):
        full_path = os.path.join(destination, item)
        if os.path.islink(full_path) or os.path.isfile(full_path):
            os.unlink(full_path)
        else:
            shutil.rmtree(full_path)

    # 3) Copiar recursivamente source -> destination
    for item in os.listdir(source):
        src_path = os.path.join(source, item)
        dst_path = os.path.join(destination, item)

        # Evitar symlinks para no salirte del árbol o crear loops
        if os.path.islink(src_path):
            continue

        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        elif os.path.isdir(src_path):
            source_to_destination_directory(src_path, dst_path)
