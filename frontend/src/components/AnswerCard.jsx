export default function AnswerCard({ result, loading }) {
  if (loading) {
    return (
      <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-5">
        <p className="text-sm text-zinc-400">Thinking...</p>
        <div className="mt-3 space-y-2">
          <div className="h-3 bg-zinc-800 rounded w-full animate-pulse" />
          <div className="h-3 bg-zinc-800 rounded w-5/6 animate-pulse" />
          <div className="h-3 bg-zinc-800 rounded w-4/6 animate-pulse" />
        </div>
      </div>
    );
  }

  if (!result) return null;

  return (
    <div className="rounded-lg border border-zinc-800 bg-zinc-900 overflow-hidden">
      <div className="p-5">
        <h2 className="text-sm font-medium text-zinc-400 mb-3">Answer</h2>
        <div className="text-sm text-zinc-200 whitespace-pre-wrap leading-relaxed">
          {result.answer}
        </div>
      </div>

      {result.sources.length > 0 && (
        <div className="border-t border-zinc-800 p-5">
          <h3 className="text-xs font-medium text-zinc-500 mb-3">
            Sources ({result.sources.length})
          </h3>
          <div className="space-y-2">
            {result.sources.map((src, i) => (
              <div key={`${src.item_id}-${i}`} className="bg-zinc-800 rounded p-3">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-sm font-medium text-zinc-200">{src.title}</span>
                  <span className="text-[10px] text-zinc-500">
                    {Math.round(src.relevance_score * 100)}% match
                  </span>
                </div>
                <p className="text-xs text-zinc-500 line-clamp-2">{src.snippet}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
