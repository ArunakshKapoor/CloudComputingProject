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
    try {
      const workflow = await api.createWorkflow({
        request_text: text,
        user_id: "demo-user",
        mode: "mock",
      });
      await api.planWorkflow(workflow.id);
      await api.simulateWorkflow(workflow.id);
      router.push(`/workflows/${workflow.id}`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="page-title">Dashboard</h1>
        <p className="page-subtitle mt-1">
          Create a governed workflow request and preview its plan, simulation, and policy outcomes.
        </p>
      </div>

      <div className="card max-w-4xl">
        <div className="mb-4">
          <h2 className="text-sm font-semibold text-text">
            Create governed workflow request
          </h2>
          <p className="mt-1 text-sm text-muted">
            Submit a natural-language request to generate a multi-step workflow.
          </p>
        </div>

        <textarea
          className="app-input min-h-[180px] resize-y"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Describe the workflow you want LifeOS to plan..."
        />

        <div className="mt-4 flex items-center gap-3">
          <button
            onClick={submit}
            disabled={loading || !text.trim()}
            className="app-button-primary disabled:cursor-not-allowed disabled:opacity-60"
          >
            {loading ? "Submitting..." : "Create + Plan + Simulate"}
          </button>

          <span className="text-sm text-muted">
            Safe defaults with simulation before execution.
          </span>
        </div>
      </div>
    </div>
  );
}