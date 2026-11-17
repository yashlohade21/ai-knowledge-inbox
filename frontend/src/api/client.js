const API_BASE = "http://localhost:8000";

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || "Request failed");
  }
  return res.json();
}

export async function ingestItem(type, content, title) {
  return request("/ingest", {
    method: "POST",
    body: JSON.stringify({ type, content, title: title || undefined }),
  });
}

export async function getItems() {
  return request("/items");
}

export async function deleteItem(id) {
  return request(`/items/${id}`, { method: "DELETE" });
}

export async function queryKnowledge(question) {
  return request("/query", {
    method: "POST",
    body: JSON.stringify({ question }),
  });
}
