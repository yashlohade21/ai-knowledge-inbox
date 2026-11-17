import { deleteItem } from "../api/client";

export default function ItemList({ items, onDeleted }) {
  async function handleDelete(id) {
    try {
      await deleteItem(id);
      onDeleted(id);
    } catch (err) {
      console.error("Delete failed:", err);
    }
  }

  if (!items.length) {
    return (
      <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-6 text-center text-zinc-500 text-sm">
        No items yet. Add a note or URL to get started.
      </div>
    );
  }

  return (
    <div className="rounded-lg border border-zinc-800 bg-zinc-900 overflow-hidden">
      <div className="px-4 py-3 border-b border-zinc-800 flex items-center justify-between">
        <h2 className="text-sm font-medium text-zinc-400">Saved Items</h2>
        <span className="text-xs text-zinc-600">{items.length}</span>
      </div>
      <div className="divide-y divide-zinc-800 max-h-[360px] overflow-y-auto">
        {items.map((item) => (
          <div key={item.id} className="px-4 py-3 group">
            <div className="flex items-start justify-between gap-2">
              <div className="min-w-0 flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className={`text-[10px] px-1.5 py-0.5 rounded font-medium ${
                    item.type === "url"
                      ? "bg-green-900/40 text-green-400"
                      : "bg-violet-900/40 text-violet-400"
                  }`}>
                    {item.type}
                  </span>
                  <span className="text-[10px] text-zinc-600">{item.chunk_count} chunks</span>
                </div>
                <p className="text-sm text-zinc-200 truncate">{item.title}</p>
                <p className="text-xs text-zinc-500 mt-0.5 line-clamp-2">{item.preview}</p>
              </div>
              <button
                onClick={() => handleDelete(item.id)}
                className="opacity-0 group-hover:opacity-100 text-zinc-600 hover:text-red-400 text-xs p-1"
              >
                &times;
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
