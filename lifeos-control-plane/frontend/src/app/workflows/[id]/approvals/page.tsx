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
    <div>
      <h1 className="text-2xl font-semibold mb-4">Approval Center</h1>
      <div className="space-y-3">
        {rows.map((a) => (
          <div key={a.id} className="card">
            <div>Step: {a.step_id}</div>
            <div>Status: {a.status}</div>
            <div className="flex gap-2 mt-2">
              <button className="px-3 py-1 bg-green-600 text-white rounded" onClick={async () => { await api.decideApproval(a.step_id, "APPROVED"); load(); }}>
                Approve
              </button>
              <button className="px-3 py-1 bg-red-600 text-white rounded" onClick={async () => { await api.decideApproval(a.step_id, "REJECTED"); load(); }}>
                Reject
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
