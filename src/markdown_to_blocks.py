

def markdown_to_blocks(markdown):
    blocks = []
    lines = markdown.split("\n\n")
    for line in lines:
        if line.strip() == "" or line == "\n":
            continue
        blocks.append(line.strip())
    return blocks
