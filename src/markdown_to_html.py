from src.markdown_to_blocks import markdown_to_blocks
from src.block import *
from src.htmlnode import *
from src.text_to_nodes import text_to_nodes

def markdown_to_html(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = [] # append nodes here to pass to div
    for block in blocks:
        block_type = block_to_blocktype(block)
        match block_type:
            case BlockType.HEADING:
                check = block.split(" ")
                num = len(check[0])
                children = []
                textnodes = text_to_nodes(" ".join(check[1:]))
                for n in textnodes:
                    children.append(text_node_to_html_node(n))
                node = ParentNode(f"h{num}", children)
            case BlockType.CODE:
                content = block.split("```")
                code_text = content[1].lstrip("\n")
                innermost = text_node_to_html_node(TextNode(code_text, TextType.PLAIN))
                parent = ParentNode("code", [innermost])
                node = ParentNode("pre", [parent])
            case BlockType.QUOTE:
                check = block.split(">")
                children = []
                textnodes = text_to_nodes(" ".join(check).strip())
                for n in textnodes:
                    children.append(text_node_to_html_node(n))
                node = ParentNode("blockquote", children)
            case BlockType.UNORD:
                check = block.split("\n")
                children = []
                for line in check:
                    line = line.strip("- ")
                    textnodes = text_to_nodes(line)
                    grandchildren = []
                    for n in textnodes:
                        grandchildren.append(text_node_to_html_node(n))
                    linode = ParentNode("li", grandchildren)
                    children.append(linode)
                node = ParentNode("ul", children)
            case BlockType.ORD:
                check = block.split("\n")
                children = []
                for line in check:
                    line = line.lstrip("0123456789. ")
                    textnodes =  text_to_nodes(line)
                    grandchildren = []
                    for n in textnodes:
                        grandchildren.append(text_node_to_html_node(n))
                    linode = ParentNode("li", grandchildren)
                    children.append(linode)
                node = ParentNode("ol", children)
            case BlockType.PARAGRAPH:
                children = []
                textnodes = text_to_nodes(block.replace("\n", " "))
                for n in textnodes:
                    children.append(text_node_to_html_node(n))
                node = ParentNode("p", children)

        nodes.append(node)
    div = ParentNode("div", nodes)
    return div
