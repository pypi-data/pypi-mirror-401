import re


def chunk_markdown(markdown: str, max_chars: int) -> list[str]:
    """
    Chunk the markdown into smaller blocks of text, using number of characters as the limit.
    """
    # First, split the markdown into logical blocks (headings, code blocks, paragraphs, etc.)
    block_pattern = re.compile(
        r"(?=\n#{1,6} |\n[`*_-]{3,}|```|^-|\n\d+\.)", re.MULTILINE
    )
    blocks = block_pattern.split(markdown)
    blocks = [block.strip() for block in blocks if block.strip()]

    chunks: list[str] = []
    current_chunk = ""

    for block in blocks:
        if len(current_chunk) + len(block) + 2 <= max_chars:
            # Add to current chunk
            current_chunk += "\n\n" + block if current_chunk else block
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            # If block is too big, break it further
            if len(block) > max_chars:
                sub_blocks = re.split(r"(\n\n|\n)", block)
                temp = ""
                for sub in sub_blocks:
                    if len(temp) + len(sub) + 1 <= max_chars:
                        temp += sub
                    else:
                        if temp:
                            chunks.append(temp.strip())
                        temp = sub
                if temp:
                    chunks.append(temp.strip())
                current_chunk = ""
            else:
                current_chunk = block

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
