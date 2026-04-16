"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  ["/", "Dashboard"],
  ["/workflows", "Workflows"],
  ["/memory", "Memory"],
  ["/policies", "Policies"],
  ["/connectors", "Connectors"],
  ["/evaluations", "Evaluations"],
  ["/settings", "Settings"],
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="hidden w-72 shrink-0 border-r border-border bg-surface px-5 py-6 transition-colors duration-200 md:block">
      <div className="mb-8">
        <div className="text-xs font-semibold uppercase tracking-[0.18em] text-accent">
          LifeOS
        </div>
        <div className="mt-2 text-xl font-semibold tracking-tight text-text">
          Control Plane
        </div>
        <p className="mt-2 text-sm leading-6 text-muted">
          Governed, observable, simulation-first personal assistant orchestration.
        </p>
      </div>

      <nav className="space-y-2">
        {links.map(([href, label]) => {
          const isActive =
            href === "/"
              ? pathname === "/"
              : pathname === href || pathname.startsWith(`${href}/`);

          return (
            <Link
              key={href}
              href={href}
              className={[
                "flex items-center rounded-xl px-3 py-2.5 text-sm font-medium transition-all duration-200",
                isActive
                  ? "bg-accent text-white shadow-soft"
                  : "text-text hover:bg-surfaceAlt hover:text-text",
              ].join(" ")}
            >
              {label}
            </Link>
          );
        })}
      </nav>

      <div className="mt-8 rounded-xl2 border border-border bg-surfaceAlt p-4 transition-colors duration-200">
        <div className="text-xs font-semibold uppercase tracking-[0.16em] text-muted">
          System mode
        </div>
        <div className="mt-2 inline-flex items-center rounded-full bg-violet-100 px-2.5 py-1 text-xs font-medium text-violet-800 dark:bg-violet-500/20 dark:text-violet-200">
          Mock-safe governance
        </div>
        <p className="mt-3 text-sm leading-6 text-muted">
          Safe defaults, approval gates, and traceable multi-step workflows.
        </p>
      </div>
    </aside>
  );
}