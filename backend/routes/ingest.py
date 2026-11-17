import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
import httpx

from models.schemas import IngestRequest, IngestResponse
from services.chunker import chunk_text
from services.embeddings import embed_texts
from services.vector_store import add_documents
from services.url_fetcher import fetch_url_content
from services import item_store
from logger import get_logger

router = APIRouter()
log = get_logger("routes.ingest")


@router.post("/ingest", response_model=IngestResponse)
async def ingest_item(req: IngestRequest):
    """Save a note or URL to the knowledge base."""
    doc_id = str(uuid.uuid4())
    text = ""
    title = req.title or ""

    try:
        if req.type == "url":
            text, page_title = await fetch_url_content(req.content)
            if not title:
                title = page_title or req.content[:80]
        else:
            text = req.content
            if not title:
                title = text[:80].split("\n")[0]

        chunks = chunk_text(text)
        if not chunks:
            raise HTTPException(status_code=400, detail="No content to process after chunking")

        embeddings = await embed_texts(chunks)

        created_at = datetime.now(timezone.utc).isoformat()
        source = req.content if req.type == "url" else ""

        chunk_metadata = {
            "doc_id": doc_id,
            "title": title,
            "type": req.type,
            "source": source,
            "created_at": created_at,
        }

        chunk_count = add_documents(doc_id, chunks, embeddings, chunk_metadata)

        # Store raw content and metadata
        item_store.save_item(doc_id, {
            "id": doc_id,
            "title": title,
            "type": req.type,
            "content": text,
            "source": source,
            "created_at": created_at,
            "chunk_count": chunk_count,
        })

        log.info(f"Ingested {req.type}: {title} ({chunk_count} chunks)")

        return IngestResponse(
            id=doc_id,
            title=title,
            chunk_count=chunk_count,
            type=req.type,
        )

    except HTTPException:
        raise
    except httpx.HTTPStatusError as e:
        log.error(f"URL fetch failed: {e}")
        raise HTTPException(status_code=422, detail=f"Failed to fetch URL: {e.response.status_code}")
    except Exception as e:
        log.error(f"Ingest failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
