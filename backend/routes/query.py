from fastapi import APIRouter, HTTPException

from models.schemas import QueryRequest, QueryResponse, SourceInfo
from services.embeddings import embed_query
from services.vector_store import query_similar
from services.llm import generate_answer
from logger import get_logger

router = APIRouter()
log = get_logger("routes.query")


@router.post("/query", response_model=QueryResponse)
async def query_knowledge(req: QueryRequest):
    """Ask a question against the knowledge base."""
    try:
        query_emb = await embed_query(req.question)
        results = query_similar(query_emb)

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        if not documents:
            return QueryResponse(
                answer="No relevant information found in your knowledge base. Try adding some notes or URLs first.",
                sources=[],
            )

        # Build context for LLM
        context_chunks = []
        sources = []
        seen_docs = set()

        for doc, meta, dist in zip(documents, metadatas, distances):
            relevance = 1 - dist  # cosine distance to similarity
            context_chunks.append({
                "title": meta.get("title", "Unknown"),
                "text": doc,
            })

            doc_id = meta.get("doc_id", "")
            if doc_id not in seen_docs:
                seen_docs.add(doc_id)
                sources.append(SourceInfo(
                    item_id=doc_id,
                    title=meta.get("title", "Unknown"),
                    snippet=doc[:200],
                    relevance_score=round(relevance, 3),
                ))

        answer = await generate_answer(req.question, context_chunks)
        log.info(f"Answered query: {req.question[:60]}... ({len(sources)} sources)")

        return QueryResponse(answer=answer, sources=sources)

    except Exception as e:
        log.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
