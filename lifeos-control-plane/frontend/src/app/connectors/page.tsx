"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";

export default function ConnectorsPage() {
  const [rows, setRows] = useState<any[]>([]);
  useEffect(() => { api.listConnectors().then(setRows); }, []);
  return (
    <div>
      <h1 className="text-2xl mb-4">Connectors</h1>
      <div className="grid grid-cols-2 gap-3">
        {rows.map((c: any) => <div key={c.name} className="card"><div className="font-semibold">{c.name}</div><div>mode: {c.mode}</div><div>status: {c.status}</div></div>)}
      </div>
    </div>
  );
}
