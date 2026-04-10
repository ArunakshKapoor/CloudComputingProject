"use client";
import { useState } from "react";
import { api } from "@/lib/api";

export default function EvaluationsPage() {
  const [result, setResult] = useState<any>();
  return (
    <div>
      <h1 className="text-2xl mb-4">Evaluations</h1>
      <button onClick={async () => setResult(await api.runEval("productivity_prompts"))} className="px-3 py-2 bg-slate-900 text-white rounded">Run Productivity Dataset</button>
      {result && <pre className="card mt-3 text-xs">{JSON.stringify(result, null, 2)}</pre>}
    </div>
  );
}
