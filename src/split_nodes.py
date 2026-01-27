from src.htmlnode import *
from src.extract_markdown import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.PLAIN:
            new = node.text.split(delimiter)
            if len(new) % 2 == 0:
                raise Exception("invalid markdown syntax. must have closing delimiter")
            for i in range(0, len(new)):
                new_text = new[i]
                if i % 2 == 0:
                    new[i] = TextNode(new_text, TextType.PLAIN)
                else:
                    new[i] = TextNode(new_text, text_type)
            new_nodes.extend(new)
        else:
            new_nodes.append(node)
    return new_nodes


def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            result.append(node)
            continue
        images = extract_markdown_images(node.text)
        if images:
            current_text = node.text
            for image in images:
                new = current_text.split(f"![{image[0]}]({image[1]})", maxsplit=1)
                if new[0]:
                    result.append(TextNode(new[0], TextType.PLAIN))
                result.append(TextNode(image[0], TextType.IMAGE, image[1]))
                current_text = new[1]
            if current_text:    
                result.append(TextNode(current_text, TextType.PLAIN))
        else:
            result.append(node)
    return result

def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            result.append(node)
            continue
        links = extract_markdown_links(node.text)
        if links:
            current_text = node.text
            for link in links:
                new = current_text.split(f"[{link[0]}]({link[1]})", maxsplit=1)
                if new[0]:
                    result.append(TextNode(new[0], TextType.PLAIN))
                result.append(TextNode(link[0], TextType.LINK, link[1]))
                current_text = new[1]
            if current_text:    
                result.append(TextNode(current_text, TextType.PLAIN))
        else:
            result.append(node)
    return result
