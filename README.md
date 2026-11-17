# AI Knowledge Inbox

A minimal RAG (Retrieval-Augmented Generation) web app. Save notes or URLs, ask questions over your saved content, and get LLM-generated answers with cited sources.

## Quick Start

```bash
git clone https://github.com/yashlohade21/ai-knowledge-inbox.git
cd ai-knowledge-inbox
./setup.sh
```

The setup script checks prerequisites, installs dependencies, and prints run instructions.

## Manual Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- [Groq API key](https://console.groq.com) (free tier)

### 1. Clone and configure

```bash
git clone https://github.com/yashlohade21/ai-knowledge-inbox.git
cd ai-knowledge-inbox
cp .env.example .env
```

Open `.env` and add your Groq API key:

```
GROQ_API_KEY=gsk_your_key_here
```

> Embeddings run locally using ChromaDB's built-in ONNX model. No embedding API key needed.

### 2. Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs at http://localhost:8000. API docs at http://localhost:8000/docs.

First request downloads the embedding model (~80MB, cached after that).

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at http://localhost:5173.

## How It Works

```
User saves note/URL
       ↓
  Extract text (BeautifulSoup for URLs)
       ↓
  Chunk text (500 chars, 50 overlap)
       ↓
  Generate embeddings (local ONNX model)
       ↓
  Store in ChromaDB + save raw content to disk
       ↓
User asks a question
       ↓
  Embed question → retrieve top-k similar chunks
       ↓
  Build prompt with retrieved context
       ↓
  Groq LLM generates answer with source citations
```

## Tech Stack

| Layer | Choice | Why |
|-------|--------|-----|
| Backend | FastAPI | Async, Pydantic validation, auto-docs at `/docs` |
| Frontend | React + Tailwind (Vite) | Hooks, simple state, fast dev server |
| LLM | Groq (`qwen/qwen3.8-27b`) | Free tier, fast inference |
| Embeddings | ChromaDB ONNX (`all-MiniLM-L6-v2`) | Local, no API needed, no rate limits |
| Vector Store | ChromaDB (file-based) | Lightweight, persistent, zero infra |
| URL Fetching | httpx + BeautifulSoup | Server-side content extraction |

## API

### `POST /ingest` — Save a note or URL

```json
// Request
{ "type": "note", "content": "FastAPI is built on Starlette...", "title": "FastAPI Notes" }

// Response
{ "id": "abc-123", "title": "FastAPI Notes", "chunk_count": 3, "type": "note" }
```

### `GET /items` — List saved items

```json
// Response
{
  "items": [
    { "id": "abc-123", "title": "FastAPI Notes", "type": "note", "preview": "FastAPI is built on...", "created_at": "2026-11-17T...", "chunk_count": 3 }
  ]
}
```

### `DELETE /items/{id}` — Delete an item

### `POST /query` — Ask a question

```json
// Request
{ "question": "What is FastAPI based on?" }

// Response
{
  "answer": "Based on the saved notes, FastAPI is built on Starlette and Pydantic...",
  "sources": [
    { "item_id": "abc-123", "title": "FastAPI Notes", "snippet": "FastAPI is built on Starlette...", "relevance_score": 0.85 }
  ]
}
```

Validation: empty content returns 422, URL fetch failures return descriptive errors, empty questions return 422.

## Project Structure

```
ai-knowledge-inbox/
├── setup.sh                     # One-command setup script
├── .env.example                 # Environment template (just GROQ_API_KEY)
├── backend/
│   ├── main.py                  # FastAPI app, CORS, route mounting
│   ├── config.py                # Settings (API keys, model config, chunk params)
│   ├── logger.py                # Structured logging
│   ├── models/
│   │   └── schemas.py           # Pydantic request/response models
│   ├── routes/
│   │   ├── ingest.py            # POST /ingest
│   │   ├── items.py             # GET /items, DELETE /items/{id}
│   │   └── query.py             # POST /query
│   └── services/
│       ├── chunker.py           # Recursive character splitter
│       ├── embeddings.py        # Local ONNX embedding wrapper
│       ├── vector_store.py      # ChromaDB operations
│       ├── item_store.py        # Raw content persistence (JSON)
│       ├── llm.py               # Groq chat completion
│       └── url_fetcher.py       # httpx + BeautifulSoup extraction
└── frontend/
    └── src/
        ├── App.jsx              # Layout, state management
        ├── api/client.js        # Backend API wrapper
        └── components/
            ├── IngestForm.jsx   # Note/URL input form
            ├── ItemList.jsx     # Saved items list
            ├── QueryBox.jsx     # Question input
            └── AnswerCard.jsx   # Answer + source citations
```

## Design Decisions and Tradeoffs

### Chunking: Recursive character split (500 chars, 50 overlap)

Simple and predictable. Splits on paragraph breaks first, then sentences, then words, then hard character limit. Overlap prevents losing context at boundaries.

**At scale:** Character-based splitting can cut mid-sentence. Sentence-boundary or semantic chunking would preserve meaning better. Chunk size needs tuning per domain.

### Vector Store: ChromaDB file-based

Zero infrastructure. Persists to disk across restarts. Good enough for single-user.

**At scale:** No concurrent write safety, no filtering beyond metadata, no replication. Would move to pgvector or a managed service like Pinecone/Weaviate.

### Embeddings: Local ONNX (all-MiniLM-L6-v2, 384 dims)

Runs on CPU in milliseconds. No external API dependency, no rate limits, no cost.

**At scale:** CPU-bound for large batch ingests. Would move to GPU-accelerated inference or a hosted embedding API.

### LLM: Groq free tier

Fast inference, zero cost for demo. Model choice is swappable via `config.py`.

**At scale:** Rate limits (30 req/min on free tier). Would add response caching, switch to OpenAI/Anthropic, and add streaming for better UX.

### Storage: Dual store (ChromaDB + JSON files)

ChromaDB stores chunked embeddings for vector search. Raw content and metadata are persisted separately as JSON files for item listing and full-text access.

**At scale:** Would use PostgreSQL for metadata and raw content, keeping the vector store focused on embeddings only.

### No Auth

Single-user, single collection. Assignment specifies no auth needed.

**Production:** JWT auth, user-scoped collections, row-level access control.

## Debuggability

- **Structured logging** in every service with timestamps and module names
- **Clear error messages** for URL fetch failures, empty content, API errors
- **HTTP status codes**: 422 for validation, 400 for bad input, 500 for server errors
- **Pydantic validation** enforces request shape at the API boundary
- **FastAPI auto-docs** at `/docs` for interactive API testing
