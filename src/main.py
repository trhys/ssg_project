import shutil
import os
import argparse
from pathlib import Path
from src.markdown_to_html import markdown_to_html

def main():
    parser = argparse.ArgumentParser(prog="static_site_generator")
    parser.add_argument("path", default="/")
    base_path = parser.parse_args()
    copy_static()
    generate_pages_recursive("content/", "template.html", "docs/", base_path.path)

def get_contents(path):
    contents = os.listdir(path)
    for item in contents:
        if os.path.isdir(os.path.join(path, item)):
            get_contents(os.path.join(path, item))
        else:
            os.makedirs(os.path.join("docs/", path[7:]), exist_ok=True)
            shutil.copy(os.path.join(path, item), os.path.join("docs/", path[7:]))

def copy_static():
    if os.path.exists("docs/"):
        shutil.rmtree("docs/")
    os.mkdir("docs/")
    get_contents("static/")

def extract_title(md):
    lines = md.split("#")
    if lines[1] == "":
        raise Exception("must have valid header for title")
    return lines[1]

def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        md = f.read()
        f.close()
    with open(template_path) as t:
        template = t.read()
        t.close()
    html = markdown_to_html(md).to_html()
    title = extract_title(md)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', 'href="{base_path}')
    template = template.replace('src="/', 'src="{base_path}')
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, mode="w") as h:
        h.write(template)
        h.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    content = os.listdir(dir_path_content)
    for c in content:
        if os.path.isfile(os.path.join(dir_path_content, c)):
            if c.split(".")[1] == "md":
                path = Path(os.path.join(dest_dir_path, c))
                dest_path = path.with_suffix(".html")
                generate_page(os.path.join(dir_path_content, c), template_path, dest_path, base_path)
        else:
            generate_pages_recursive(os.path.join(dir_path_content, c), template_path, os.path.join(dest_dir_path, c), base_path)


main()

