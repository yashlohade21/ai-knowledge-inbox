import { useState, useEffect } from "react";
import IngestForm from "./components/IngestForm";
import ItemList from "./components/ItemList";
import QueryBox from "./components/QueryBox";
import AnswerCard from "./components/AnswerCard";
import { getItems } from "./api/client";

export default function App() {
  const [items, setItems] = useState([]);
  const [queryResult, setQueryResult] = useState(null);
  const [isQuerying, setIsQuerying] = useState(false);

  useEffect(() => {
    loadItems();
  }, []);

  async function loadItems() {
    try {
      const data = await getItems();
      setItems(data.items);
    } catch (err) {
      console.error("Failed to load items:", err);
    }
  }

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <header className="mb-8">
        <h1 className="text-2xl font-bold text-zinc-100">AI Knowledge Inbox</h1>
        <p className="text-sm text-zinc-500 mt-1">
          Save notes and URLs, then ask questions to get answers with cited sources.
        </p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <IngestForm onIngested={loadItems} />
          <ItemList
            items={items}
            onDeleted={(id) => setItems((prev) => prev.filter((i) => i.id !== id))}
          />
        </div>
        <div className="lg:col-span-3 space-y-6">
          <QueryBox onResult={setQueryResult} onLoading={setIsQuerying} />
          <AnswerCard result={queryResult} loading={isQuerying} />
        </div>
      </div>
    </div>
  );
}
