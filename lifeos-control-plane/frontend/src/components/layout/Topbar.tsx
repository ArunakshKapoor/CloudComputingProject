"use client";

import { useEffect, useState } from "react";

type ThemeMode = "light" | "dark";

export default function Topbar() {
  const [theme, setTheme] = useState<ThemeMode>("light");

  useEffect(() => {
    const root = document.documentElement;
    const savedTheme = localStorage.getItem("lifeos-theme") as ThemeMode | null;

    if (savedTheme === "dark" || savedTheme === "light") {
      root.classList.remove("light", "dark");
      root.classList.add(savedTheme);
      setTheme(savedTheme);
      return;
    }

    root.classList.remove("light", "dark");
    root.classList.add("light");
    setTheme("light");
  }, []);

  function toggleTheme() {
    const root = document.documentElement;
    const nextTheme: ThemeMode = theme === "light" ? "dark" : "light";

    root.classList.remove("light", "dark");
    root.classList.add(nextTheme);
    localStorage.setItem("lifeos-theme", nextTheme);
    setTheme(nextTheme);
  }

  return (
    <header className="sticky top-0 z-20 border-b border-border bg-surface/90 px-6 py-3 backdrop-blur transition-colors duration-200">
      <div className="mx-auto flex w-full max-w-7xl items-center justify-between">
        <div>
          <div className="text-sm font-semibold tracking-tight text-text">
            Governed orchestration dashboard
          </div>
          <p className="mt-1 text-xs text-muted">
            Personal Assistant-as-a-Service with approvals, simulation, and traceability.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <span className="inline-flex items-center rounded-full border border-border bg-surfaceAlt px-3 py-1 text-xs font-medium text-text transition-colors duration-200">
            Mock-safe mode
          </span>

          <button
            type="button"
            onClick={toggleTheme}
            className="app-button-secondary min-w-[96px]"
            aria-label="Toggle theme"
          >
            {theme === "light" ? "Dark mode" : "Light mode"}
          </button>
        </div>
      </div>
    </header>
  );
}