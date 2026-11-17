import httpx
from bs4 import BeautifulSoup
from logger import get_logger

log = get_logger("url_fetcher")


async def fetch_url_content(url: str) -> tuple[str, str]:
    """Fetch a URL and extract its text content and title.

    Returns (text_content, page_title).
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; KnowledgeInbox/1.0)",
    }

    async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # Extract title
    title = ""
    if soup.title and soup.title.string:
        title = soup.title.string.strip()

    # Remove script, style, nav, footer elements
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    # Get text from main content areas, fall back to body
    main = soup.find("main") or soup.find("article") or soup.find("body")
    text = main.get_text(separator="\n", strip=True) if main else ""

    # Clean up excessive whitespace
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    text = "\n".join(lines)

    if not text:
        raise ValueError(f"No text content extracted from {url}")

    log.info(f"Fetched URL: {url} — {len(text)} chars, title: {title[:60]}")
    return text, title
