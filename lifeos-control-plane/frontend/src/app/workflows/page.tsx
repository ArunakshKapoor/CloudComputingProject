"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { api } from "@/lib/api";

export default function WorkflowsPage() {
  const [rows, setRows] = useState<any[]>([]);
  useEffect(() => {
    api.listWorkflows().then(setRows);
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">Workflows</h1>
      <div className="space-y-3">
        {rows.map((w) => (
          <Link key={w.id} href={`/workflows/${w.id}`} className="card block">
            <div className="font-medium">{w.request_text}</div>
            <div className="text-sm text-slate-600">{w.status}</div>
          </Link>
        ))}
      </div>
    </div>
  );
}
