import { ProgressChart } from "@/components/progress-chart";

export default function ProgressPage() {
  return (
    <div className="mx-auto flex w-full max-w-3xl flex-col gap-6 px-6 py-12">
      <header>
        <h1 className="text-3xl font-bold text-slate-900">Progres & Analitik</h1>
        <p className="text-sm text-slate-600">Pantau perkembangan belajarmu.</p>
      </header>
      <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <ProgressChart />
      </div>
    </div>
  );
}