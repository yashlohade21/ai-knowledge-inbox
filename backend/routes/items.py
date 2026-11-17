from fastapi import APIRouter

from models.schemas import ItemsResponse, ItemSummary
from services import item_store
from services.vector_store import delete_item as delete_chunks
from logger import get_logger

router = APIRouter()
log = get_logger("routes.items")


@router.get("/items", response_model=ItemsResponse)
async def list_items():
    """List all saved items in the knowledge base."""
    raw_items = item_store.get_all()
    items = []
    for item in raw_items:
        items.append(ItemSummary(
            id=item["id"],
            title=item["title"],
            type=item["type"],
            preview=item["content"][:200],
            created_at=item["created_at"],
            chunk_count=item["chunk_count"],
        ))
    log.info(f"Listed {len(items)} items")
    return ItemsResponse(items=items)


@router.delete("/items/{item_id}")
async def remove_item(item_id: str):
    """Delete an item from the knowledge base."""
    item_store.delete(item_id)
    delete_chunks(item_id)
    log.info(f"Deleted item {item_id}")
    return {"detail": "Item deleted"}
