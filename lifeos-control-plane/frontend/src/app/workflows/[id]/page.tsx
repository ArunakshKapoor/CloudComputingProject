"use client";

import { useEffect, useMemo, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { api } from "@/lib/api";

function toneForStatus(status?: string) {
  const value = (status || "").toUpperCase();

  if (value.includes("COMPLETED")) {
    return "bg-emerald-100 text-emerald-800 dark:bg-emerald-500/20 dark:text-emerald-200";
  }
  if (value.includes("APPROVAL")) {
    return "bg-amber-100 text-amber-800 dark:bg-amber-500/20 dark:text-amber-200";
  }
  if (value.includes("BLOCK")) {
    return "bg-red-100 text-red-800 dark:bg-red-500/20 dark:text-red-200";
  }
  if (value.includes("EXECUTING") || value.includes("SIMULATING") || value.includes("PLANNING")) {
    return "bg-blue-100 text-blue-800 dark:bg-blue-500/20 dark:text-blue-200";
  }

  return "bg-surfaceAlt text-text";
}

function toneForRisk(risk?: string) {
  const value = (risk || "").toUpperCase();

  if (value === "HIGH") {
    return "bg-red-100 text-red-800 dark:bg-red-500/20 dark:text-red-200";
  }
  if (value === "MEDIUM") {
    return "bg-amber-100 text-amber-800 dark:bg-amber-500/20 dark:text-amber-200";
  }
  return "bg-blue-100 text-blue-800 dark:bg-blue-500/20 dark:text-blue-200";
}

export default function WorkflowDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [wf, setWf] = useState<any>();
  const [sim, setSim] = useState<any>();
  const [runningSimulation, setRunningSimulation] = useState(false);
  const [runningExecution, setRunningExecution] = useState(false);

  useEffect(() => {
    api.getWorkflow(id).then(setWf);
  }, [id]);

  async function runSimulation() {
    setRunningSimulation(true);
    try {
      setSim(await api.simulateWorkflow(id));
      setWf(await api.getWorkflow(id));
    } finally {
      setRunningSimulation(false);
    }
  }

  async function execute() {
    setRunningExecution(true);
    try {
      await api.executeWorkflow(id);
      setWf(await api.getWorkflow(id));
    } finally {
      setRunningExecution(false);
    }
  }

  const summary = useMemo(() => {
    if (!wf?.steps) {
      return { total: 0, highRisk: 0, approvals: 0 };
    }

    return {
      total: wf.steps.length,
      highRisk: wf.steps.filter((s: any) => s.risk_level === "HIGH").length,
      approvals: wf.steps.filter((s: any) => s.policy_decision === "APPROVAL_REQUIRED").length,
    };
  }, [wf]);

  if (!wf) {
    return (
      <div className="card">
        <div className="text-base font-semibold text-text">Loading workflow...</div>
        <p className="mt-2 text-sm text-muted">Fetching workflow details and step state.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="page-title">Workflow Details</h1>
        <p className="page-subtitle mt-1">
          Review the request, inspect the plan, simulate outcomes, and execute approved actions.
        </p>
      </div>

      <div className="card space-y-4">
        <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
          <div>
            <div className="text-base font-semibold text-text">{wf.request_text}</div>
            <p className="mt-2 text-sm text-muted">Workflow ID: {wf.id}</p>
          </div>

          <div className={`app-badge ${toneForStatus(wf.status)}`}>
            {wf.status}
          </div>
        </div>

        <div className="grid gap-3 md:grid-cols-3">
          <div className="card-muted">
            <div className="text-sm font-medium text-muted">Total steps</div>
            <div className="mt-2 text-2xl font-semibold text-text">{summary.total}</div>
          </div>

          <div className="card-muted">
            <div className="text-sm font-medium text-muted">High-risk steps</div>
            <div className="mt-2 text-2xl font-semibold text-text">{summary.highRisk}</div>
          </div>

          <div className="card-muted">
            <div className="text-sm font-medium text-muted">Approval-gated steps</div>
            <div className="mt-2 text-2xl font-semibold text-text">{summary.approvals}</div>
          </div>
        </div>
      </div>

      <div className="grid gap-4 xl:grid-cols-2">
        <div className="card">
          <div className="mb-4">
            <h2 className="text-base font-semibold text-text">Plan</h2>
            <p className="mt-1 text-sm text-muted">
              Structured workflow steps with risk and policy decisions.
            </p>
          </div>

          <div className="space-y-3">
            {wf.steps.map((s: any) => (
              <div key={s.id} className="rounded-xl border border-border bg-surfaceAlt/70 p-4 transition-colors duration-200">
                <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
                  <div>
                    <div className="text-sm font-semibold text-text">{s.name}</div>
                    <div className="mt-1 text-sm text-muted">{s.action_type}</div>
                  </div>

                  <div className="flex flex-wrap gap-2">
                    <span className={`app-badge ${toneForRisk(s.risk_level)}`}>
                      {s.risk_level}
                    </span>
                    <span className={`app-badge ${toneForStatus(s.policy_decision)}`}>
                      {s.policy_decision}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="card">
          <div className="mb-4">
            <h2 className="text-base font-semibold text-text">Simulation</h2>
            <p className="mt-1 text-sm text-muted">
              Preview likely outputs, side effects, and approval requirements.
            </p>
          </div>

          {!sim ? (
            <div className="rounded-xl border border-dashed border-border bg-surfaceAlt/50 p-6 text-sm text-muted">
              Run simulation to preview outputs and estimated workflow behavior.
            </div>
          ) : (
            <div className="space-y-4">
              <div className="grid gap-3 md:grid-cols-2">
                <div className="card-muted">
                  <div className="text-sm font-medium text-muted">Estimated latency</div>
                  <div className="mt-2 text-xl font-semibold text-text">
                    {sim.estimated_latency_ms} ms
                  </div>
                </div>

                <div className="card-muted">
                  <div className="text-sm font-medium text-muted">Estimated cost</div>
                  <div className="mt-2 text-xl font-semibold text-text">
                    ${sim.estimated_cost_usd}
                  </div>
                </div>
              </div>

              <div className="rounded-xl border border-border bg-surfaceAlt/70 p-4">
                <div className="text-sm font-medium text-muted">Side-effect summary</div>
                <div className="mt-2 text-sm text-text">{sim.side_effect_summary}</div>
              </div>

              <div className="space-y-3">
                {sim.steps?.map((s: any) => (
                  <div key={s.step_id} className="rounded-xl border border-border bg-surfaceAlt/70 p-4">
                    <div className="mb-2 flex items-center justify-between">
                      <div className="text-sm font-medium text-text">Step preview</div>
                      {s.approval_required && (
                        <span className="app-badge bg-amber-100 text-amber-800 dark:bg-amber-500/20 dark:text-amber-200">
                          Approval required
                        </span>
                      )}
                    </div>

                    <pre className="whitespace-pre-wrap text-xs leading-6 text-text">
                      {s.preview}
                    </pre>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      <div className="flex flex-wrap gap-3">
        <button
          onClick={runSimulation}
          disabled={runningSimulation}
          className="app-button-secondary disabled:cursor-not-allowed disabled:opacity-60"
        >
          {runningSimulation ? "Simulating..." : "Run Simulation"}
        </button>

        <button
          onClick={execute}
          disabled={runningExecution}
          className="app-button-primary disabled:cursor-not-allowed disabled:opacity-60"
        >
          {runningExecution ? "Executing..." : "Execute"}
        </button>

        <Link href={`/workflows/${id}/approvals`} className="app-button-secondary">
          Approvals
        </Link>

        <Link href={`/workflows/${id}/trace`} className="app-button-secondary">
          Trace
        </Link>
      </div>
    </div>
  );
}