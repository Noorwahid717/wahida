"use client";

import { useState } from "react";

interface HintPanelProps {
  hints: string[];
}

export function HintPanel({ hints }: HintPanelProps) {
  const [revealed, setRevealed] = useState(0);
  const nextHint = () => setRevealed((prev) => Math.min(hints.length, prev + 1));

  return (
    <aside data-testid="hint-panel" className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <header className="flex items-center justify-between">
        <h2 className="font-semibold text-slate-800">Hint bertahap</h2>
        <button
          type="button"
          className="rounded-md bg-indigo-600 px-3 py-1 text-sm font-medium text-white disabled:opacity-40"
          onClick={nextHint}
          disabled={revealed >= hints.length}
        >
          Tampilkan hint
        </button>
      </header>
      <ol className="mt-3 space-y-2 text-sm text-slate-600">
        {hints.slice(0, revealed).map((hint, idx) => (
          <li key={idx} className="rounded-md bg-slate-100 px-3 py-2">
            {hint}
          </li>
        ))}
        {revealed === 0 && <li className="text-xs italic text-slate-400">Klik tombol untuk membuka hint pertama.</li>}
      </ol>
    </aside>
  );
}
