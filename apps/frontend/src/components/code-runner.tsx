"use client";

import { useMutation } from "@tanstack/react-query";
import { useState } from "react";

import { API_BASE_URL } from "@/lib/api";

interface CodeRunnerProps {
  defaultLanguage?: string;
}

async function runCode(language: string, source: string) {
  const response = await fetch(`${API_BASE_URL}/api/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ language, source }),
  });
  if (!response.ok) {
    const detail = await response.json().catch(() => ({}));
    throw new Error(detail.detail ?? "Gagal menjalankan kode");
  }
  return (await response.json()) as { stdout: string; stderr?: string };
}

export function CodeRunner({ defaultLanguage = "python" }: CodeRunnerProps) {
  const [source, setSource] = useState("print('halo wahida')\n");
  const [language, setLanguage] = useState(defaultLanguage);
  const mutation = useMutation({
    mutationFn: (payload: { language: string; source: string }) => runCode(payload.language, payload.source),
  });

  return (
    <section data-testid="code-runner" className="space-y-3 rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <header className="flex items-center justify-between">
        <h2 className="font-semibold text-slate-800">Latihan kode</h2>
        <select
          className="rounded-md border border-slate-200 px-2 py-1 text-sm"
          value={language}
          onChange={(event) => {
            const newLanguage = event.target.value;
            setLanguage(newLanguage);
          }}
        >
          <option value="python">Python</option>
          <option value="cpp">C++</option>
          <option value="javascript">JavaScript</option>
        </select>
      </header>
      <textarea
        value={source}
        onChange={(event) => setSource(event.target.value)}
        placeholder="Tulis kode di sini"
        className="min-h-[160px] w-full rounded-md border border-slate-200 bg-slate-50 p-3 font-mono text-sm"
      />
      <div className="flex gap-3">
        <button
          type="button"
          className="rounded-md bg-emerald-600 px-4 py-2 text-sm font-medium text-white disabled:opacity-40"
          onClick={() => mutation.mutate({ language, source })}
          disabled={mutation.isPending}
        >
          Jalankan
        </button>
        {mutation.isError && (
          <p className="text-sm text-red-500">
            {mutation.error instanceof Error ? mutation.error.message : "Gagal menjalankan kode"}
          </p>
        )}
      </div>
      {(mutation.data || mutation.isPending) && (
        <pre className="whitespace-pre-wrap rounded-md bg-slate-900 p-3 text-xs text-slate-100">
          {mutation.isPending ? "Menjalankan kode..." : mutation.data?.stdout}
        </pre>
      )}
    </section>
  );
}
