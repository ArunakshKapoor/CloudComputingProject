"use client";
import { useEffect, useMemo, useState } from "react";
import { useParams } from "next/navigation";
import { api } from "@/lib/api";

function formatTimestamp(value?: string) {
  if (!value) return "Unknown time";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleString();
}

function stageTone(stage?: string) {
  const value = (stage || "").toLowerCase();

  if (value.includes("workflow")) return "bg-violet-100 text-violet-800 dark:bg-violet-500/20 dark:text-violet-200";
  if (value.includes("planning")) return "bg-blue-100 text-blue-800 dark:bg-blue-500/20 dark:text-blue-200";
  if (value.includes("simulation")) return "bg-amber-100 text-amber-800 dark:bg-amber-500/20 dark:text-amber-200";
  if (value.includes("approval")) return "bg-orange-100 text-orange-800 dark:bg-orange-500/20 dark:text-orange-200";
  if (value.includes("execution")) return "bg-emerald-100 text-emerald-800 dark:bg-emerald-500/20 dark:text-emerald-200";
  if (value.includes("memory")) return "bg-slate-200 text-slate-800 dark:bg-slate-700 dark:text-slate-200";

  return "bg-surfaceAlt text-text";
}

export default function TracePage() {
  const { id } = useParams<{ id: string }>();
  const [events, setEvents] = useState<any[]>([]);

  useEffect(() => {
    api.trace(id).then(setEvents);
  }, [id]);

  const summary = useMemo(() => {
    const stages = new Set(events.map((e) => e.stage).filter(Boolean));
    return {
      total: events.length,
      stages: stages.size,
    };
  }, [events]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="page-title">Trace</h1>
        <p className="page-subtitle mt-1">
          Inspect the workflow lifecycle across planning, simulation, approvals, and execution.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <div className="card">
          <div className="text-sm font-medium text-muted">Total events</div>
          <div className="mt-2 text-3xl font-semibold text-text">{summary.total}</div>
        </div>

        <div className="card">
          <div className="text-sm font-medium text-muted">Distinct stages</div>
          <div className="mt-2 text-3xl font-semibold text-text">{summary.stages}</div>
        </div>
      </div>

      {events.length === 0 ? (
        <div className="card">
          <div className="text-base font-semibold text-text">No trace events yet</div>
          <p className="mt-2 text-sm text-muted">
            Run planning, simulation, approvals, or execution to populate the workflow trace.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {events.map((e, index) => (
            <div key={e.id} className="card">
              <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
                <div className="space-y-3">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className={`app-badge ${stageTone(e.stage)}`}>
                      {e.stage || "unknown-stage"}
                    </span>
                    <span className="app-badge border bg-surfaceAlt text-text">
                      {e.event_type || "unknown-event"}
                    </span>
                  </div>

                  <div>
                    <div className="text-base font-semibold text-text">
                      {e.message || "No message"}
                    </div>
                    <div className="mt-1 text-sm text-muted">
                      Event #{index + 1}
                    </div>
                  </div>

                  {e.metadata_json && e.metadata_json !== "{}" && (
                    <details className="rounded-lg border border-border bg-surfaceAlt/70 p-3 transition-colors duration-200">
                      <summary className="cursor-pointer text-sm font-medium text-text">
                        View metadata
                      </summary>
                      <pre className="mt-3 overflow-x-auto whitespace-pre-wrap text-xs text-muted">
                        {typeof e.metadata_json === "string"
                          ? e.metadata_json
                          : JSON.stringify(e.metadata_json, null, 2)}
                      </pre>
                    </details>
                  )}
                </div>

                <div className="shrink-0 text-sm text-muted">
                  {formatTimestamp(e.timestamp)}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}