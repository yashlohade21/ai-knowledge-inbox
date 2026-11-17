from config import settings
from logger import get_logger

log = get_logger("chunker")


def chunk_text(text: str) -> list[str]:
    """Split text into overlapping chunks using recursive character splitting."""
    size = settings.chunk_size
    overlap = settings.chunk_overlap
    separators = ["\n\n", "\n", ". ", " ", ""]

    chunks = _recursive_split(text, separators, size)

    # Add overlap between chunks
    result = []
    for i, chunk in enumerate(chunks):
        if i > 0 and overlap > 0:
            prev_tail = chunks[i - 1][-overlap:]
            chunk = prev_tail + chunk
        result.append(chunk.strip())

    result = [c for c in result if c]
    log.info(f"Split text ({len(text)} chars) into {len(result)} chunks")
    return result


def _recursive_split(text: str, separators: list[str], size: int) -> list[str]:
    if len(text) <= size:
        return [text] if text.strip() else []

    for sep in separators:
        if sep and sep in text:
            parts = text.split(sep)
            chunks = []
            current = ""
            for part in parts:
                candidate = current + sep + part if current else part
                if len(candidate) <= size:
                    current = candidate
                else:
                    if current:
                        chunks.append(current)
                    if len(part) > size:
                        chunks.extend(_recursive_split(part, separators[separators.index(sep) + 1:], size))
                    else:
                        current = part
            if current:
                chunks.append(current)
            return chunks

    # Last resort: hard split by character count
    return [text[i:i + size] for i in range(0, len(text), size)]
