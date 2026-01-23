import re
from enum import Enum

from htmlnode import HTMLNode, LeafNode, ParentNode
from text_to_textnode import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(text):
    my_text = text.strip()
    if re.match(r"^#{1,6}\s+", my_text):
        return BlockType.HEADING
    if my_text.startswith("```\n") and my_text.endswith("```"):
        return BlockType.CODE
    if my_text.startswith("> "):
        return BlockType.QUOTE
    if re.match(r"^(\-|\*|\+)\s+", my_text):
        return BlockType.UNORDERED_LIST
    if re.match(r"^\d+\.\s+", my_text):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    blocks = [block.strip() for block in markdown.split("\n\n")]
    blocks = [block for block in blocks if block != ""]
    return blocks


def markdown_to_html_node(markdown):
    my_blocks = markdown_to_blocks(markdown)
    children_blocks = []
    for block in my_blocks:
        type = block_to_block_type(block)
        if type == BlockType.PARAGRAPH:
            children_blocks.append(markdown_to_paragraph(block))
        elif type == BlockType.CODE:
            children_blocks.append(markdown_to_code(block))
        elif type == BlockType.HEADING:
            children_blocks.append(markdown_to_heading(block))
        elif type == BlockType.QUOTE:
            children_blocks.append(markdown_to_quote(block))
        elif type == BlockType.UNORDERED_LIST:
            children_blocks.append(markdown_to_unordered(block))
        elif type == BlockType.ORDERED_LIST:
            children_blocks.append(markdown_to_ordered(block))
    return ParentNode("div", children_blocks)


def markdown_to_paragraph(block):
    lines = block.split("\n")
    stripped = [line.strip() for line in lines if line.strip() != ""]
    line_children = " ".join(stripped)
    return ParentNode("p", text_to_children(line_children))


def markdown_to_code(block):
    lines = block.split("\n")
    inner_lines = lines[1:-1]
    first = inner_lines[0]
    indent = len(first) - len(first.lstrip(" "))
    dedented = []
    for line in inner_lines:
        i = 0
        while i < indent and i < len(line) and line[i] == " ":
            i += 1
        dedented.append(line[i:])

    my_lines = "\n".join(dedented) + "\n"
    raw = TextNode(my_lines, TextType.TEXT)
    child = text_node_to_html_node(raw)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def markdown_to_heading(block):
    line = block.split("\n")[0]
    depth = 0
    for char in line:
        if char == "#":
            depth += 1
        else:
            break
    text = line[depth:].lstrip()
    line_kids = text_to_children(text)
    return ParentNode(f"h{depth}", line_kids)


def markdown_to_quote(block):
    lines = block.split("\n")
    cleaned_lines = []
    for line in lines:
        line = line.lstrip()
        if line.startswith(">"):
            line = line[1:]
            if line.startswith(" "):
                line = line[1:]
        cleaned_lines.append(line)
    line_children = " ".join(cleaned_lines)
    line_kids = text_to_children(line_children)
    return ParentNode("blockquote", line_kids)


def markdown_to_unordered(block):
    lines = block.split("\n")
    cleaned_lines = []
    for line in lines:
        if not line.strip():
            continue
        content = line[2:]
        children = text_to_children(content)
        cleaned_lines.append(ParentNode("li", children))
    return ParentNode("ul", cleaned_lines)


def markdown_to_ordered(block):
    lines = block.split("\n")
    cleaned_lines = []
    for line in lines:
        if not line.strip():
            continue
        _, content = line.strip().split(" ", 1)
        children = text_to_children(content)
        cleaned_lines.append(ParentNode("li", children))
    return ParentNode("ol", cleaned_lines)


def text_to_children(text):
    nodes = text_to_textnodes(text)
    html_nodes = []
    for node in nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes
