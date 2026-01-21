from textnode import TextNode, TextType
from extract_markdown import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if delimiter not in node.text:
            new_nodes.append(node)
            continue
        node_string = node.text.split(delimiter)
        if len(node_string) % 2 == 0:
            raise Exception("Invalid, markdown formatted section doesn't close")

        new_node = []
        for i in range(len(node_string)):
            if node_string[i] == "":
                continue
            if i % 2 == 0:
                new_node.append(TextNode(node_string[i], TextType.TEXT))
            else:
                new_node.append(TextNode(node_string[i], text_type))


        new_nodes.extend(new_node)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        images= extract_markdown_images(text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for alt, url in images:
            image_markdown = f"![{alt}]({url})"
            sections = text.split(image_markdown, 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            text = sections[1]
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        links = extract_markdown_links(text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for link_text, link_url in links:
            link_markdown = f"[{link_text}]({link_url})"
            sections = text.split(link_markdown, 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            text = sections[1]
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes
