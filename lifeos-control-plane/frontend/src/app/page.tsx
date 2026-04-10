"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import { samplePrompt } from "@/lib/mock-data";

export default function HomePage() {
  const [text, setText] = useState(samplePrompt);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  async function submit() {
    setLoading(true);
    const workflow = await api.createWorkflow({ request_text: text, user_id: "demo-user", mode: "mock" });
    await api.planWorkflow(workflow.id);
    await api.simulateWorkflow(workflow.id);
    setLoading(false);
    router.push(`/workflows/${workflow.id}`);
  }

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold">Dashboard</h1>
      <div className="card">
        <p className="text-sm mb-2">Create governed workflow request</p>
        <textarea className="w-full border rounded p-2 h-36" value={text} onChange={(e) => setText(e.target.value)} />
        <button onClick={submit} className="mt-3 px-4 py-2 bg-slate-900 text-white rounded">
          {loading ? "Submitting..." : "Create + Plan + Simulate"}
        </button>
      </div>
    </div>
  );
}
