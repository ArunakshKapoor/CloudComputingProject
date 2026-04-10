export default function Topbar() {
  return (
    <div className="h-14 border-b bg-white px-6 flex items-center justify-between">
      <div className="font-medium">Governed orchestration dashboard</div>
      <span className="text-xs px-2 py-1 rounded bg-violet-100 text-violet-800">Mock-safe mode</span>
    </div>
  );
}
