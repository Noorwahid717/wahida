"use client";

import { useQuery } from "@tanstack/react-query";

import { StreakBadge } from "@/components/streak-badge";
import { API_BASE_URL } from "@/lib/api";
import { queryKeys } from "@/lib/query-keys";

interface ProgressSummary {
  user_id: string;
  streak_days: number;
  badges: string[];
  last_active: string;
}

async function fetchProgress(userId: string): Promise<ProgressSummary> {
  const response = await fetch(`${API_BASE_URL}/api/progress/${userId}`);
  if (!response.ok) {
    throw new Error("Gagal memuat progres");
  }
  return response.json();
}

export default function TeacherDashboard() {
  const userId = "demo-user";
  const { data, isLoading, error } = useQuery({ queryKey: queryKeys.progress(userId), queryFn: () => fetchProgress(userId) });

  return (
    <div className="mx-auto flex w-full max-w-5xl flex-col gap-6 px-6 py-12">
      <header>
        <h1 className="text-3xl font-bold text-foreground">Dashboard Guru</h1>
        <p className="text-sm text-muted-foreground">Pantau progres siswa dan badge yang sudah diraih.</p>
      </header>
      {isLoading && <p className="text-sm text-muted-foreground">Memuat data...</p>}
      {error && <p className="text-sm text-destructive">{String(error)}</p>}
      {data && (
        <div className="space-y-4">
          <StreakBadge current={data.streak_days} longest={Math.max(data.streak_days, 7)} name="Streak Juara" icon="🔥" />
          <section className="rounded-lg border bg-card p-4 shadow-sm">
            <h2 className="text-lg font-semibold text-card-foreground">Badge siswa</h2>
            <ul className="mt-2 flex flex-wrap gap-2 text-sm text-muted-foreground">
              {data.badges.map((badge) => (
                <li key={badge} className="rounded-full bg-accent px-3 py-1 text-accent-foreground">
                  {badge}
                </li>
              ))}
            </ul>
            <p className="mt-4 text-xs text-muted-foreground">Aktif terakhir {new Date(data.last_active).toLocaleDateString("id-ID")}.</p>
          </section>
        </div>
      )}
    </div>
  );
}
