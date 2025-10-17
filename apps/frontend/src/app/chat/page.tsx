"use client";

import { FormEvent, useState } from "react";

import { CodeRunner } from "@/components/code-runner";
import { HintPanel } from "@/components/hint-panel";
import { QuizCard } from "@/components/quiz-card";
import { API_BASE_URL } from "@/lib/api";

interface RetrievedChunk {
  text: string;
  metadata: Record<string, string>;
  score: number;
  hintsRevealed: number;
}

interface LLMResponse {
  text: string;
}

async function streamChat(
  message: string,
  onChunk: (chunk: RetrievedChunk) => void,
  onResponse: (response: LLMResponse) => void
) {
  const response = await fetch(`${API_BASE_URL}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
  if (!response.body) {
    throw new Error("Tidak ada stream dari server");
  }
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const events = buffer.split("\n\n");
    buffer = events.pop() ?? "";
    for (const event of events) {
      if (event.startsWith("data:")) {
        const payload = JSON.parse(event.replace(/^data:\s*/, ""));
        if (payload.type === "chunk") {
          onChunk(payload as RetrievedChunk);
        } else if (payload.type === "response") {
          onResponse(payload as LLMResponse);
        }
      }
    }
  }
}

export default function ChatPage() {
  const [input, setInput] = useState("");
  const [chunks, setChunks] = useState<RetrievedChunk[]>([]);
  const [llmResponse, setLlmResponse] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const hints = chunks.map((chunk) => chunk.text.slice(0, 120));

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!input.trim()) return;
    setChunks([]);
    setError(null);
    setLoading(true);
    try {
      let emitted = false;
      await streamChat(
        input,
        (chunk) => {
          setChunks((prev) => [...prev, chunk]);
        },
        (response) => {
          setLlmResponse(response.text);
        }
      );
      if (!emitted) {
        setChunks([
          {
            text: "Tidak ada respons dari server. Gunakan konsep dasar: bentukkan persamaan dan susun ulang variabel.",
            metadata: { topik: "Fallback" },
            score: 0,
            hintsRevealed: 1,
          },
        ]);
      }
    } catch {
      setError("Gagal menghubungi tutor. Coba lagi nanti.");
      setChunks([
        {
          text: "Gunakan sifat distributif dan kumpulkan variabel di satu sisi persamaan.",
          metadata: { topik: "Fallback" },
          score: 0,
          hintsRevealed: 1,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto flex w-full max-w-5xl flex-col gap-6 px-6 py-12">
      <header className="space-y-2">
        <h1 className="text-3xl font-bold text-slate-900">Chat Tutor</h1>
        <p className="text-sm text-slate-600">Streaming SSE dari FastAPI dengan moderasi dan rate limit.</p>
      </header>
      <form onSubmit={handleSubmit} className="flex flex-col gap-3 rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
        <textarea
          placeholder="Tulis pertanyaanmu..."
          value={input}
          onChange={(event) => setInput(event.target.value)}
          className="min-h-[120px] w-full rounded-md border border-slate-200 p-3 text-sm"
        />
        <button
          type="submit"
          className="self-end rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white disabled:opacity-40"
          disabled={loading}
        >
          {loading ? "Memproses..." : "Kirim"}
        </button>
      </form>
      <div className="grid gap-4 md:grid-cols-[2fr_1fr]">
        <div className="space-y-4">
          <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-800">Ringkasan sumber</h2>
            {error && <p className="text-xs text-red-500">{error}</p>}
            <ul className="mt-2 space-y-2 text-sm text-slate-600">
              {chunks.map((chunk, idx) => (
                <li key={idx} className="rounded-md bg-slate-100 p-3">
                  <p className="font-medium text-slate-700">{chunk.metadata.topik ?? "Referensi"}</p>
                  <p>{chunk.text}</p>
                </li>
              ))}
              {chunks.length === 0 && !loading && <li className="text-xs text-slate-400">Kirim pertanyaan untuk melihat referensi.</li>}
            </ul>
          </section>
          {llmResponse && (
            <section className="rounded-lg border border-green-200 bg-green-50 p-4 shadow-sm">
              <h2 className="text-lg font-semibold text-green-800">Respons AI</h2>
              <p className="mt-2 text-sm text-green-700">{llmResponse}</p>
            </section>
          )}
          <CodeRunner />
        </div>
        <div className="space-y-4">
          <HintPanel hints={hints.length ? hints : ["Mulai dengan memahami apa yang ditanya soalmu."]} />
          <QuizCard
            questionId="intro-python"
            prompt="Apa output dari print(1 + 1)?"
            choices={["11", "2", "'1 + 1'"]}
          />
        </div>
      </div>
    </div>
  );
}
