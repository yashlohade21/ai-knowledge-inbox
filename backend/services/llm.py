from groq import AsyncGroq
from config import settings
from logger import get_logger

log = get_logger("llm")

_client = AsyncGroq(api_key=settings.groq_api_key)

SYSTEM_PROMPT = """You are a helpful assistant that answers questions based on the user's saved knowledge base.
Use ONLY the provided context to answer. If the context doesn't contain enough information, say so clearly.
When referencing information, mention which source it came from using the source titles provided.
Keep answers concise and well-structured."""


async def generate_answer(question: str, context_chunks: list[dict]) -> str:
    """Generate an answer using retrieved context chunks."""
    context_parts = []
    for i, chunk in enumerate(context_chunks):
        title = chunk.get("title", f"Source {i+1}")
        text = chunk.get("text", "")
        context_parts.append(f"[Source: {title}]\n{text}")

    context_str = "\n\n---\n\n".join(context_parts)

    user_msg = f"""Context from knowledge base:
{context_str}

Question: {question}

Answer based on the context above. Cite your sources by title."""

    log.info(f"Generating answer for: {question[:80]}...")
    response = await _client.chat.completions.create(
        model=settings.llm_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.3,
        max_tokens=1024,
    )

    answer = response.choices[0].message.content
    log.info(f"Generated answer ({len(answer)} chars)")
    return answer
