"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";

export default function MemoryPage() {
  const [rows, setRows] = useState<any[]>([]);
  useEffect(() => {
    api.listMemory().then(setRows);
  }, []);

  return (
    <div>
      <h1 className="text-2xl mb-4">Memory</h1>
      <div className="space-y-2">
        {rows.map((m) => (
          <div key={m.id} className="card text-sm">
            <b>{m.key}</b>: {m.value} <span className="text-slate-500">({m.source})</span>
          </div>
        ))}
      </div>
    </div>
  );
}
