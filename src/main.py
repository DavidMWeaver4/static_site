import os
import sys
import shutil
from random import shuffle

from copystatic import copy_files_recursive
from textnode import TextNode, TextType
from generatepage import generate_page, generate_pages_recursive
# hello world
dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    copy_files_recursive(dir_path_static, dir_path_public)

    generate_pages_recursive(dir_path_content, template_path, dir_path_public, basepath)

    print(TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev"))


if __name__ == "__main__":
    main()
