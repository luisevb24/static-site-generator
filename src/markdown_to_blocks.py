def markdown_to_blocks(markdown):
    return [b.strip() for b in markdown.split("\n\n") if b.strip() != ""]
