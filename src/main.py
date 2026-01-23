import os
import shutil
from random import shuffle

from copystatic import copy_files_recursive
from textnode import TextNode, TextType

# hello world
dir_path_static = "./static"
dir_path_public = "./public"


def main():
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    copy_files_recursive(dir_path_static, dir_path_public)
    print(TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev"))


if __name__ == "__main__":
    main()
