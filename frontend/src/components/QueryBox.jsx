import { useState } from "react";
import { queryKnowledge } from "../api/client";

export default function QueryBox({ onResult, onLoading }) {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    if (!question.trim()) return;
    setLoading(true);
    setError("");
    onLoading?.(true);
    try {
      const result = await queryKnowledge(question);
      onResult(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
      onLoading?.(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="rounded-lg border border-zinc-800 bg-zinc-900 p-4 space-y-3">
      <h2 className="text-sm font-medium text-zinc-400">Ask a Question</h2>
      <div className="flex gap-2">
        <input
          type="text"
          placeholder="What would you like to know?"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          className="flex-1 px-3 py-2 bg-zinc-800 border border-zinc-700 rounded text-sm text-zinc-200 placeholder-zinc-500 focus:outline-none focus:border-zinc-600"
        />
        <button
          type="submit"
          disabled={loading || !question.trim()}
          className="px-4 py-2 bg-zinc-100 text-zinc-900 rounded text-sm font-medium hover:bg-white disabled:opacity-30 disabled:cursor-not-allowed"
        >
          {loading ? "..." : "Ask"}
        </button>
      </div>
      {error && <p className="text-red-400 text-xs">{error}</p>}
    </form>
  );
}
