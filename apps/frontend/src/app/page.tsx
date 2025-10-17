import { Sparkles, MessageCircle, Trophy, Cpu, ChartSpline } from "lucide-react";

import { FeatureCard } from "@/components/feature-card";
import { ProgressChart } from "@/components/progress-chart";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 via-white to-slate-100 px-6 py-16 text-slate-900 dark:from-slate-950 dark:via-slate-950 dark:to-slate-900 dark:text-slate-100">
      <main className="mx-auto flex w-full max-w-6xl flex-col gap-16">
        <section className="rounded-3xl border border-slate-200/80 bg-white/80 p-10 shadow-xl backdrop-blur-lg dark:border-slate-800 dark:bg-slate-900/70">
          <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
            <div className="space-y-4">
              <span className="inline-flex items-center gap-2 rounded-full bg-indigo-100 px-4 py-1 text-sm font-medium text-indigo-700 dark:bg-indigo-500/20 dark:text-indigo-200">
                <Sparkles className="h-4 w-4" /> MVP siap dipakai
              </span>
              <h1 className="text-4xl font-bold sm:text-5xl">Wahidiyah Digital Assistant</h1>
              <p className="max-w-2xl text-lg text-slate-600 dark:text-slate-200/80">
                Tutoring cerdas dengan materi adaptif, latihan interaktif, dan analitik progres real-time.
                Integrasi Next.js, FastAPI, RAG, dan pipeline eksekusi kode siap dikembangkan bertahap.
              </p>
            </div>
            <div className="h-40 w-full max-w-sm rounded-2xl border border-indigo-200 bg-indigo-50/80 p-4 text-indigo-900 shadow-inner dark:border-indigo-800 dark:bg-indigo-500/10 dark:text-indigo-100">
              <p className="text-sm uppercase tracking-wide">Stack highlight</p>
              <ul className="mt-3 space-y-2 text-sm">
                <li>⚡ Next.js App Router + TanStack Query</li>
                <li>🧠 FastAPI + Celery + Redis + Postgres/pgvector</li>
                <li>🤖 OpenAI / OSS LLM + FAISS indexing</li>
                <li>📊 PostHog analytics & feature flags</li>
              </ul>
            </div>
          </div>
        </section>

        <section className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
          <FeatureCard
            title="Chat Tutor"
            description="Streaming respons via SSE/WebSocket dengan pipeline RAG, moderation, dan PostHog logging."
            icon={<MessageCircle className="h-6 w-6" />}
            href="/chat"
          />
          <FeatureCard
            title="Kuis Adaptif"
            description="Bank soal terstruktur dengan penilaian cepat, rekomendasi remedial, dan leaderboard kelas."
            icon={<Trophy className="h-6 w-6" />}
            href="/quiz"
          />
          <FeatureCard
            title="Sandbox Kode"
            description="Eksekusi Python aman via Judge0/Docker + Celery queue dan audit trail di Postgres."
            icon={<Cpu className="h-6 w-6" />}
            href="/run"
          />
          <FeatureCard
            title="Progres & Analitik"
            description="Dashboard real-time dengan streak, badge, dan insight pembelajaran via PostHog."
            icon={<ChartSpline className="h-6 w-6" />}
            href="/progress"
          />
        </section>

        <section className="grid gap-8 lg:grid-cols-[2fr_1fr]">
          <div className="rounded-3xl border border-slate-200 bg-white/80 p-8 shadow-xl backdrop-blur dark:border-slate-800 dark:bg-slate-900/70">
            <h2 className="text-2xl font-semibold text-slate-900 dark:text-slate-100">Alur Integrasi Backend</h2>
            <ol className="mt-6 space-y-4 text-sm text-slate-600 dark:text-slate-200/80">
              <li className="flex gap-3">
                <span className="mt-1 flex h-6 w-6 items-center justify-center rounded-full bg-indigo-500 text-xs font-semibold text-white">
                  1
                </span>
                <div>
                  <p className="font-medium">FastAPI Router</p>
                  <p>Endpoint `/chat`, `/quiz`, `/run`, dan `/progress` sudah terdaftar untuk iterasi berikutnya.</p>
                </div>
              </li>
              <li className="flex gap-3">
                <span className="mt-1 flex h-6 w-6 items-center justify-center rounded-full bg-indigo-500 text-xs font-semibold text-white">
                  2
                </span>
                <div>
                  <p className="font-medium">Queue & Worker</p>
                  <p>Celery + Redis siap dihubungkan untuk eksekusi kode dan batch embedding.</p>
                </div>
              </li>
              <li className="flex gap-3">
                <span className="mt-1 flex h-6 w-6 items-center justify-center rounded-full bg-indigo-500 text-xs font-semibold text-white">
                  3
                </span>
                <div>
                  <p className="font-medium">Observability</p>
                  <p>PostHog, OpenTelemetry, dan guard moderasi dapat dipasang mengikuti struktur ini.</p>
                </div>
              </li>
            </ol>
          </div>
          <div className="flex flex-col gap-4 rounded-3xl border border-slate-200 bg-white/80 p-8 shadow-xl backdrop-blur dark:border-slate-800 dark:bg-slate-900/70">
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Snapshot Progres</h2>
            <ProgressChart />
          </div>
        </section>
      </main>
    </div>
  );
}
