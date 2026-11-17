import chromadb
from config import settings
from logger import get_logger

log = get_logger("vector_store")

_client = None
_collection = None


def _get_collection():
    global _client, _collection
    if _collection is None:
        _client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
        _collection = _client.get_or_create_collection(
            name="knowledge_base",
            metadata={"hnsw:space": "cosine"},
        )
        log.info("ChromaDB collection initialized")
    return _collection


def add_documents(
    doc_id: str,
    chunks: list[str],
    embeddings: list[list[float]],
    metadata: dict,
) -> int:
    """Store chunks with their embeddings in ChromaDB."""
    col = _get_collection()
    ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [{**metadata, "chunk_index": i} for i in range(len(chunks))]

    col.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
    )
    log.info(f"Added {len(chunks)} chunks for doc {doc_id}")
    return len(chunks)


def query_similar(query_embedding: list[float], top_k: int = None) -> dict:
    """Find the most similar chunks to the query embedding."""
    col = _get_collection()
    k = top_k or settings.top_k
    count = col.count()
    if count == 0:
        return {"documents": [[]], "metadatas": [[]], "distances": [[]]}

    k = min(k, count)
    results = col.query(
        query_embeddings=[query_embedding],
        n_results=k,
    )
    log.info(f"Retrieved {len(results['documents'][0])} chunks")
    return results


def delete_item(doc_id: str) -> bool:
    """Delete all chunks belonging to a document."""
    col = _get_collection()
    all_data = col.get(include=["metadatas"])
    ids_to_delete = []
    for i, meta in enumerate(all_data["metadatas"]):
        if meta.get("doc_id") == doc_id:
            ids_to_delete.append(all_data["ids"][i])

    if ids_to_delete:
        col.delete(ids=ids_to_delete)
        log.info(f"Deleted {len(ids_to_delete)} chunks for doc {doc_id}")
        return True
    return False
