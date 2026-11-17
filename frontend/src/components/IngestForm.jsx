import { useState } from "react";
import { ingestItem } from "../api/client";

export default function IngestForm({ onIngested }) {
  const [type, setType] = useState("note");
  const [content, setContent] = useState("");
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function switchType(t) {
    setType(t);
    setContent("");
    setTitle("");
    setError("");
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!content.trim()) return;
    setLoading(true);
    setError("");
    try {
      await ingestItem(type, content, title);
      setContent("");
      setTitle("");
      onIngested();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="rounded-lg border border-zinc-800 bg-zinc-900 p-4 space-y-3">
      <div className="flex items-center justify-between">
        <h2 className="text-sm font-medium text-zinc-400">Add Knowledge</h2>
        <div className="flex gap-1 bg-zinc-800 rounded p-0.5">
          {["note", "url"].map((t) => (
            <button
              key={t}
              type="button"
              onClick={() => switchType(t)}
              className={`px-2.5 py-1 rounded text-xs font-medium ${
                type === t ? "bg-zinc-700 text-zinc-100" : "text-zinc-500 hover:text-zinc-300"
              }`}
            >
              {t === "note" ? "Note" : "URL"}
            </button>
          ))}
        </div>
      </div>

      <input
        type="text"
        placeholder="Title (optional)"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        className="w-full px-3 py-2 bg-zinc-800 border border-zinc-700 rounded text-sm text-zinc-200 placeholder-zinc-500 focus:outline-none focus:border-zinc-600"
      />

      {type === "note" ? (
        <textarea
          placeholder="Paste your note here..."
          value={content}
          onChange={(e) => setContent(e.target.value)}
          rows={3}
          className="w-full px-3 py-2 bg-zinc-800 border border-zinc-700 rounded text-sm text-zinc-200 placeholder-zinc-500 focus:outline-none focus:border-zinc-600 resize-y"
        />
      ) : (
        <input
          type="url"
          placeholder="https://example.com/article"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          className="w-full px-3 py-2 bg-zinc-800 border border-zinc-700 rounded text-sm text-zinc-200 placeholder-zinc-500 focus:outline-none focus:border-zinc-600"
        />
      )}

      {error && <p className="text-red-400 text-xs">{error}</p>}

      <button
        type="submit"
        disabled={loading || !content.trim()}
        className="w-full py-2 bg-zinc-100 text-zinc-900 rounded text-sm font-medium hover:bg-white disabled:opacity-30 disabled:cursor-not-allowed"
      >
        {loading ? "Processing..." : "Save"}
      </button>
    </form>
  );
}
