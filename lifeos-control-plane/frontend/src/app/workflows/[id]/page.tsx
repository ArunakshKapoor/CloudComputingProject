"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { api } from "@/lib/api";

export default function WorkflowDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [wf, setWf] = useState<any>();
  const [sim, setSim] = useState<any>();

  useEffect(() => {
    api.getWorkflow(id).then(setWf);
  }, [id]);

  async function runSimulation() {
    setSim(await api.simulateWorkflow(id));
    setWf(await api.getWorkflow(id));
  }

  async function execute() {
    await api.executeWorkflow(id);
    setWf(await api.getWorkflow(id));
  }

  if (!wf) return <div>Loading...</div>;

  return (
    <div className="space-y-4">
      <div className="card">
        <div className="font-semibold">{wf.request_text}</div>
        <div>Status: {wf.status}</div>
      </div>
      <div className="grid grid-cols-2 gap-4">
        <div className="card">
          <h3 className="font-semibold mb-2">Plan</h3>
          {wf.steps.map((s: any) => (
            <div key={s.id} className="border-b py-2 text-sm">
              {s.name} · {s.risk_level} · {s.policy_decision}
            </div>
          ))}
        </div>
        <div className="card">
          <h3 className="font-semibold mb-2">Simulation</h3>
          {sim?.steps?.map((s: any) => (
            <pre key={s.step_id} className="text-xs whitespace-pre-wrap">
              {s.preview}
            </pre>
          )) || "Run simulation"}
        </div>
      </div>
      <div className="flex gap-3">
        <button onClick={runSimulation} className="px-3 py-2 rounded bg-amber-500 text-white">Simulate</button>
        <button onClick={execute} className="px-3 py-2 rounded bg-emerald-600 text-white">Execute</button>
        <Link href={`/workflows/${id}/approvals`} className="px-3 py-2 rounded bg-slate-200">Approvals</Link>
        <Link href={`/workflows/${id}/trace`} className="px-3 py-2 rounded bg-slate-200">Trace</Link>
      </div>
    </div>
  );
}
