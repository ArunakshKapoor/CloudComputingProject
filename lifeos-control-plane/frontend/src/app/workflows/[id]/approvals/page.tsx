"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { api } from "@/lib/api";

export default function ApprovalsPage() {
  const { id } = useParams<{ id: string }>();
  const [rows, setRows] = useState<any[]>([]);

  const load = () => api.listApprovals(id).then(setRows);

  useEffect(() => {
    load();
  }, [id]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="page-title">Approval Center</h1>
        <p className="page-subtitle mt-1">
          Review high-risk actions before execution.
        </p>
      </div>

      <div className="space-y-4">
        {rows.map((a) => (
          <div key={a.id} className="card">
            <div className="flex items-start justify-between gap-4">
              <div>
                <div className="text-base font-semibold text-text">
                  {a.step_name || "Unnamed approval step"}
                </div>
                <div className="mt-1 text-sm text-muted">
                  {a.action_type || a.step_id}
                </div>
              </div>

              <div className="app-badge border bg-surfaceAlt text-text">
                {a.risk_level || "UNKNOWN"} · {a.status}
              </div>
            </div>

            <div className="mt-4 flex gap-2">
              <button
                className="app-button-primary"
                onClick={async () => {
                  await api.decideApproval(a.step_id, "APPROVED");
                  load();
                }}
              >
                Approve
              </button>

              <button
                className="app-button-secondary"
                onClick={async () => {
                  await api.decideApproval(a.step_id, "REJECTED");
                  load();
                }}
              >
                Reject
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}