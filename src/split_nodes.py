from textnode import TextNode, TextType

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
