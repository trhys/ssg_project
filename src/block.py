from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORD = "unordered_list"
    ORD = "ordered_list"

def block_to_blocktype(text):
    header_block = text.split("\n")
    headers = []
    for line in header_block:
        header = re.findall(r"^#{1,6} ", line)
        if header:
            headers.append(header)
    if headers and len(header_block) == 1:
        return BlockType.HEADING
    
    code_block = text
    code_begin = re.findall(r"^```\n", code_block)
    code_end = re.findall(r"```\Z", code_block)
    if code_begin and code_end:
        return BlockType.CODE

    quote_block = text.split("\n")
    quotes = []
    for line in quote_block:
        quote = re.findall(r"^>", line)
        if quote:
            quotes.append(quote)
    if len(quote_block) == len(quotes):
        return BlockType.QUOTE

    unord_block = text.split("\n")
    u_list = []
    for line in unord_block:
        unord = re.findall(r"^- ", line)
        if unord:
            u_list.append(unord)
    if len(unord_block) == len(u_list):
        return BlockType.UNORD

    ord_block = text.split("\n")
    ord_list = []
    for i in range(len(ord_block)):
        if ord_block[i].startswith(f"{i+1}. "):
            ord_list.append(ord_block[i])
    if len(ord_block) == len(ord_list):
        return BlockType.ORD

    return BlockType.PARAGRAPH
