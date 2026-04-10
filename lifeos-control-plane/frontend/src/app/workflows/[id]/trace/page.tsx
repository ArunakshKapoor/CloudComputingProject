"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { api } from "@/lib/api";

export default function TracePage() {
  const { id } = useParams<{ id: string }>();
  const [events, setEvents] = useState<any[]>([]);

  useEffect(() => {
    api.trace(id).then(setEvents);
  }, [id]);

  return (
    <div>
      <h1 className="text-2xl mb-4">Trace</h1>
      {events.map((e) => (
        <div key={e.id} className="card mb-2">
          <div className="text-sm font-medium">{e.stage} · {e.event_type}</div>
          <div className="text-sm">{e.message}</div>
        </div>
      ))}
    </div>
  );
}
