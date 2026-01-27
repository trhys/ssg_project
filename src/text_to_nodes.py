from src.split_nodes import *

def text_to_nodes(text):
    original_node = TextNode(text, TextType.PLAIN)
    split = split_nodes_delimiter([original_node], "`", TextType.CODE)
    split = split_nodes_delimiter(split, "**", TextType.BOLD)
    split = split_nodes_delimiter(split, "_", TextType.ITALIC)
    split = split_nodes_link(split)
    split = split_nodes_image(split)
    return split
