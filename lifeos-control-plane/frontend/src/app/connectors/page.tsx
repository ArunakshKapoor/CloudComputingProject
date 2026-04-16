"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";

function toneForMode(mode?: string) {
  const value = (mode || "").toLowerCase();

  if (value.includes("live")) {
    return "bg-emerald-100 text-emerald-800 dark:bg-emerald-500/20 dark:text-emerald-200";
  }
  if (value.includes("mock")) {
    return "bg-amber-100 text-amber-800 dark:bg-amber-500/20 dark:text-amber-200";
  }
  return "bg-surfaceAlt text-text";
}

function toneForStatus(status?: string) {
  const value = (status || "").toLowerCase();

  if (value === "ok") {
    return "bg-blue-100 text-blue-800 dark:bg-blue-500/20 dark:text-blue-200";
  }
  if (value === "error") {
    return "bg-red-100 text-red-800 dark:bg-red-500/20 dark:text-red-200";
  }
  return "bg-surfaceAlt text-text";
}

export default function ConnectorsPage() {
  const [rows, setRows] = useState<any[]>([]);

  useEffect(() => {
    api.listConnectors().then(setRows);
  }, []);

  const liveCount = rows.filter((c) => String(c.mode || "").toLowerCase().includes("live")).length;
  const mockCount = rows.filter((c) => String(c.mode || "").toLowerCase().includes("mock")).length;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="page-title">Connectors</h1>
        <p className="page-subtitle mt-1">
          Monitor service connectors and see which integrations are live versus mock-backed.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <div className="card">
          <div className="text-sm font-medium text-muted">Total connectors</div>
          <div className="mt-2 text-3xl font-semibold text-text">{rows.length}</div>
        </div>

        <div className="card">
          <div className="text-sm font-medium text-muted">Live connectors</div>
          <div className="mt-2 text-3xl font-semibold text-text">{liveCount}</div>
        </div>

        <div className="card">
          <div className="text-sm font-medium text-muted">Mock connectors</div>
          <div className="mt-2 text-3xl font-semibold text-text">{mockCount}</div>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        {rows.map((c: any) => (
          <div key={c.name} className="card space-y-4">
            <div className="flex items-start justify-between gap-4">
              <div>
                <div className="text-base font-semibold text-text capitalize">{c.name}</div>
                <div className="mt-1 text-sm text-muted">
                  External capability wrapped behind a stable connector interface.
                </div>
              </div>

              <span className={`app-badge ${toneForStatus(c.status)}`}>
                {c.status}
              </span>
            </div>

            <div className="flex flex-wrap gap-2">
              <span className={`app-badge ${toneForMode(c.mode)}`}>
                {c.mode}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}