import { ProgressChart } from "@/components/progress-chart";
import { AuthGuard } from "@/components/auth-guard";

export default function ProgressPage() {
  return (
    <AuthGuard>
      <div className="mx-auto flex w-full max-w-3xl flex-col gap-6 px-6 py-12">
        <header>
          <h1 className="text-3xl font-bold text-foreground">Progres & Analitik</h1>
          <p className="text-sm text-muted-foreground">Pantau perkembangan belajarmu.</p>
        </header>
        <div className="rounded-lg border bg-card p-6 shadow-sm">
          <ProgressChart />
        </div>
      </div>
    </AuthGuard>
  );
}