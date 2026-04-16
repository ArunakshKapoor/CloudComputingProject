"use client";

import { useState } from "react";
import { api } from "@/lib/api";

const DATASETS = [
  {
    key: "productivity_prompts",
    label: "Run Productivity Dataset",
    description: "Normal productivity-oriented workflows.",
  },
  {
    key: "risky_action_prompts",
    label: "Run Risky Action Dataset",
    description: "Prompts that should trigger blocking or approval gates.",
  },
  {
    key: "failure_injection_prompts",
    label: "Run Failure Injection Dataset",
    description: "Prompts designed to test failure handling and resilience.",
  },
];

export default function EvaluationsPage() {
  const [result, setResult] = useState<any>();
  const [running, setRunning] = useState(false);
  const [activeDataset, setActiveDataset] = useState("productivity_prompts");

  async function runEvaluation(dataset: string) {
    setRunning(true);
    setActiveDataset(dataset);
    try {
      setResult(await api.runEval(dataset));
    } finally {
      setRunning(false);
    }
  }

  const metrics = result?.metrics || {};

  return (
    <div className="space-y-6">
      <div>
        <h1 className="page-title">Evaluations</h1>
        <p className="page-subtitle mt-1">
          Run benchmark datasets and inspect summary metrics for workflow quality.
        </p>
      </div>

      <div className="grid gap-4 xl:grid-cols-3">
        {DATASETS.map((dataset) => {
          const isActive = activeDataset === dataset.key;
          return (
            <div key={dataset.key} className="card">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <div className="text-base font-semibold text-text">{dataset.label}</div>
                  <p className="mt-1 text-sm text-muted">{dataset.description}</p>
                </div>
                {isActive && (
                  <span className="app-badge bg-accent text-white">Active</span>
                )}
              </div>

              <div className="mt-4">
                <button
                  onClick={() => runEvaluation(dataset.key)}
                  disabled={running}
                  className="app-button-primary disabled:cursor-not-allowed disabled:opacity-60"
                >
                  {running && isActive ? "Running..." : dataset.label}
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {result && (
        <div className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            <div className="card">
              <div className="text-sm font-medium text-muted">Run ID</div>
              <div className="mt-2 break-all text-sm font-semibold text-text">
                {result.run_id}
              </div>
            </div>

            <div className="card">
              <div className="text-sm font-medium text-muted">Status</div>
              <div className="mt-2 text-xl font-semibold text-text">{result.status}</div>
            </div>

            <div className="card">
              <div className="text-sm font-medium text-muted">Dataset</div>
              <div className="mt-2 text-sm font-semibold text-text">
                {result.dataset || activeDataset}
              </div>
            </div>

            <div className="card">
              <div className="text-sm font-medium text-muted">Metric count</div>
              <div className="mt-2 text-3xl font-semibold text-text">
                {Object.keys(metrics).length}
              </div>
            </div>
          </div>

          <div className="card">
            <div className="mb-4">
              <h2 className="text-base font-semibold text-text">Metrics summary</h2>
              <p className="mt-1 text-sm text-muted">
                Aggregated metrics for the selected evaluation dataset.
              </p>
            </div>

            <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
              {Object.entries(metrics).map(([key, value]) => (
                <div key={key} className="card-muted">
                  <div className="text-sm font-medium text-muted">
                    {key.replaceAll("_", " ")}
                  </div>
                  <div className="mt-2 text-2xl font-semibold text-text">
                    {String(value)}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <details className="card">
            <summary className="cursor-pointer text-sm font-semibold text-text">
              View raw evaluation output
            </summary>
            <pre className="mt-4 overflow-x-auto whitespace-pre-wrap text-xs text-muted">
              {JSON.stringify(result, null, 2)}
            </pre>
          </details>
        </div>
      )}
    </div>
  );
}