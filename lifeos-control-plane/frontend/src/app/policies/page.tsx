"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";

export default function PoliciesPage() {
  const [rows, setRows] = useState<any[]>([]);
  useEffect(() => {
    api.listPolicies().then(setRows);
  }, []);
  return (
    <div>
      <h1 className="text-2xl mb-4">Policies</h1>
      <div className="card">
        <table className="w-full text-sm">
          <thead><tr><th>Action</th><th>Risk</th><th>Allowed</th><th>Approval</th></tr></thead>
          <tbody>{rows.map((r) => <tr key={r.action_type}><td>{r.action_type}</td><td>{r.risk_level}</td><td>{String(r.allowed)}</td><td>{String(r.requires_approval)}</td></tr>)}</tbody>
        </table>
      </div>
    </div>
  );
}
