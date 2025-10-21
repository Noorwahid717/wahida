"use client";

import { useState } from "react";

interface HintPanelProps {
  hints: string[];
}

export function HintPanel({ hints }: HintPanelProps) {
  const [revealed, setRevealed] = useState(0);
  const nextHint = () => setRevealed((prev) => Math.min(hints.length, prev + 1));

  return (
    <aside data-testid="hint-panel" className="rounded-lg border bg-card p-4 shadow-sm">
      <header className="flex items-center justify-between">
        <h2 className="font-semibold text-card-foreground">Hint bertahap</h2>
        <button
          type="button"
          className="rounded-md bg-primary px-3 py-1 text-sm font-medium text-primary-foreground hover:bg-primary/90 disabled:opacity-40"
          onClick={nextHint}
          disabled={revealed >= hints.length}
        >
          Tampilkan hint
        </button>
      </header>
      <ol className="mt-3 space-y-2 text-sm text-muted-foreground">
        {hints.slice(0, revealed).map((hint, idx) => (
          <li key={idx} className="rounded-md bg-muted px-3 py-2 text-foreground">
            {hint}
          </li>
        ))}
        {revealed === 0 && <li className="text-xs italic text-muted-foreground">Klik tombol untuk membuka hint pertama.</li>}
      </ol>
    </aside>
  );
}
