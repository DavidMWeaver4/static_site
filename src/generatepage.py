from markdown_blocks import markdown_to_html_node
from htmlnode import ParentNode, LeafNode, HTMLNode
from extracttitle import extract_title
import os
from pathlib import Path

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    html_content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page_html = template.replace("{{ Title }}", title)
    page_html = page_html.replace("{{ Content }}", html_content)

    dirpath = os.path.dirname(dest_path)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(page_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    all_files_in_content = os.listdir(dir_path_content)
    for all_files in all_files_in_content:
        my_path = os.path.join(dir_path_content, all_files)
        if os.path.isfile(my_path):
            file_path = Path(my_path)
            if file_path.suffix == ".md":
                relative = file_path.relative_to(Path("./content"))
                html_relative = relative.with_suffix(".html")
                dest_path = Path(dest_dir_path) / html_relative
                generate_page(my_path, template_path, dest_path)

        if os.path.isdir(my_path):
            generate_pages_recursive(my_path, template_path, dest_dir_path)
