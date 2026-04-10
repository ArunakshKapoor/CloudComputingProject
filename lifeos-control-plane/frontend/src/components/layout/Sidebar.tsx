import Link from "next/link";

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
  return (
    <aside className="w-64 border-r bg-white p-4">
      <div className="font-bold mb-4">LifeOS Control Plane</div>
      {links.map(([href, label]) => (
        <Link key={href} className="block py-2 text-sm" href={href}>
          {label}
        </Link>
      ))}
    </aside>
  );
}
