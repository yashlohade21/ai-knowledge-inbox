import json
import os
from config import settings
from logger import get_logger

log = get_logger("item_store")

_store_path = os.path.join(settings.chroma_persist_dir, "items.json")


def _load() -> dict:
    if os.path.exists(_store_path):
        with open(_store_path, "r") as f:
            return json.load(f)
    return {}


def _save(data: dict):
    os.makedirs(os.path.dirname(_store_path), exist_ok=True)
    with open(_store_path, "w") as f:
        json.dump(data, f)


def save_item(doc_id: str, item: dict):
    """Persist raw content and metadata for an item."""
    data = _load()
    data[doc_id] = item
    _save(data)
    log.info(f"Saved raw item: {doc_id}")


def get_item(doc_id: str) -> dict | None:
    data = _load()
    return data.get(doc_id)


def get_all() -> list[dict]:
    """Return all items sorted by created_at descending."""
    data = _load()
    items = list(data.values())
    items.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return items


def delete(doc_id: str) -> bool:
    data = _load()
    if doc_id in data:
        del data[doc_id]
        _save(data)
        log.info(f"Deleted raw item: {doc_id}")
        return True
    return False
