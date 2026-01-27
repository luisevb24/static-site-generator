from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    """
    Determine the markdown block type of a single block of text.
    Assumes leading/trailing whitespace is already stripped.
    """
    if not block:
        return BlockType.PARAGRAPH

    lines = block.split("\n")

    # Multiline code block: starts with ``` + newline, ends with ```
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    # Heading: 1-6 #'s, then a space, then text
    first_line = lines[0]
    if first_line.startswith("#"):
        hash_count = 0
        for ch in first_line:
            if ch == "#":
                hash_count += 1
            else:
                break
        if 1 <= hash_count <= 6 and len(first_line) > hash_count and first_line[hash_count] == " ":
            return BlockType.HEADING

    # Quote: every line starts with "> "
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered list: every line starts with "- "
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list: every line starts with "N. " where N starts at 1 and increments
    expected = 1
    ordered_ok = True
    for line in lines:
        prefix = f"{expected}. "
        if not line.startswith(prefix):
            ordered_ok = False
            break
        expected += 1
    if ordered_ok:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
