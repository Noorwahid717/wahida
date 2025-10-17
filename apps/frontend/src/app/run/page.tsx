export default function RunPage() {
  return (
    <div className="mx-auto flex w-full max-w-3xl flex-col gap-6 px-6 py-12">
      <header>
        <h1 className="text-3xl font-bold text-slate-900">Sandbox Kode</h1>
        <p className="text-sm text-slate-600">Jalankan kode Python dengan aman.</p>
      </header>
      <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <p className="text-slate-600">Fitur ini sedang dalam pengembangan. Gunakan MSW mock untuk testing.</p>
      </div>
    </div>
  );
}