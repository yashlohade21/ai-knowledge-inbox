from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from logger import get_logger

log = get_logger("embeddings")

_ef = None


def get_embedding_function():
    """Return ChromaDB's default ONNX-based embedding function (all-MiniLM-L6-v2)."""
    global _ef
    if _ef is None:
        _ef = DefaultEmbeddingFunction()
        log.info("Loaded ONNX embedding model: all-MiniLM-L6-v2")
    return _ef


async def embed_texts(texts: list[str]) -> list[list[float]]:
    """Generate embeddings using ChromaDB's built-in ONNX model."""
    ef = get_embedding_function()
    embeddings = ef(texts)
    log.info(f"Generated embeddings for {len(texts)} texts")
    return embeddings


async def embed_query(text: str) -> list[float]:
    """Embed a single query string."""
    ef = get_embedding_function()
    return ef([text])[0]
