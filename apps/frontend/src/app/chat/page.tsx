"use client";

import { FormEvent, useState, useRef, useEffect } from "react";

import { CodeRunner } from "@/components/code-runner";
import { HintPanel } from "@/components/hint-panel";
import { QuizCard } from "@/components/quiz-card";
import { AuthGuard } from "@/components/auth-guard";
import { API_BASE_URL, authenticatedFetch } from "@/lib/api";
import { Loader2, User, Bot } from "lucide-react";

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
  onChunk: (retrievedChunk: RetrievedChunk) => void,
  onResponse: (llmResponse: LLMResponse) => void
) {
  const response = await authenticatedFetch(`${API_BASE_URL}/api/chat`, {
    method: "POST",
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
  const scrollRef = useRef<HTMLDivElement>(null);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!input.trim()) return;
    setChunks([]);
    setError(null);
    setLoading(true);
    try {
      await streamChat(
        input,
        (chunk) => {
          setChunks((prev) => [...prev, chunk]);
        },
        (response) => {
          setLlmResponse(response.text);
        }
      );
      setLoading(false);
    } catch {
      setError("Gagal menghubungi tutor. Coba lagi nanti.");
      setLoading(false);
    }
  };

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [chunks, llmResponse]);

  return (
    <AuthGuard>
      <div className="mx-auto flex w-full max-w-5xl flex-col gap-6 px-6 py-12">
        <header className="space-y-2">
          <h1 className="text-4xl font-extrabold text-foreground">Chat Tutor</h1>
          <p className="text-base text-muted-foreground">Streaming SSE dari FastAPI dengan moderasi dan rate limit.</p>
        </header>
        <form onSubmit={handleSubmit} className="flex flex-col gap-3 rounded-lg border bg-card p-6 shadow-sm">
          <div className="flex items-start gap-3">
            <User className="h-6 w-6 text-primary mt-1" />
            <textarea
              placeholder="Tulis pertanyaanmu..."
              value={input}
              onChange={(event) => setInput(event.target.value)}
              className="flex-1 min-h-[150px] w-full rounded-md border border-input bg-background p-4 text-sm text-foreground placeholder:text-muted-foreground"
            />
          </div>
          <button
            type="submit"
            className="self-end rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 disabled:opacity-40 flex items-center gap-2"
            disabled={loading}
          >
            {loading && <Loader2 className="h-4 w-4 animate-spin" />}
            {loading ? "Memproses..." : "Kirim"}
          </button>
        </form>
        <div className="grid gap-6 md:grid-cols-[3fr_1fr]" ref={scrollRef}>
          <div className="space-y-6">
            <section className="rounded-lg border bg-card p-6 shadow-sm">
              <h2 className="text-xl font-semibold text-card-foreground flex items-center gap-2">
                <Bot className="h-5 w-5 text-primary" />
                Ringkasan sumber
              </h2>
              {error && <p className="text-xs text-destructive">{error}</p>}
              <ul className="mt-2 space-y-2 text-sm text-muted-foreground">
                {chunks.map((chunk, idx) => (
                  <li key={idx} className="rounded-md bg-muted p-3">
                    <div className="flex items-center gap-2">
                      <Bot className="h-5 w-5 text-muted-foreground" />
                      <p className="font-medium text-foreground">{chunk.metadata.topik ?? "Referensi"}</p>
                    </div>
                    <p className="text-muted-foreground">{chunk.text}</p>
                  </li>
                ))}
                {chunks.length === 0 && !loading && <li className="text-xs text-muted-foreground">Kirim pertanyaan untuk melihat referensi.</li>}
              </ul>
            </section>
            {llmResponse && (
              <section className="rounded-lg border bg-card p-6 shadow-sm">
                <h2 className="text-xl font-semibold text-card-foreground flex items-center gap-2">
                  <Bot className="h-5 w-5 text-primary" />
                  Respons AI
                </h2>
                <p className="mt-3 text-sm text-card-foreground leading-relaxed">{llmResponse}</p>
              </section>
            )}
            <div ref={scrollRef} />
            <CodeRunner />
          </div>
          <div className="space-y-4 bg-muted p-4 rounded-lg">
            <HintPanel hints={hints.length ? hints : ["Mulai dengan memahami apa yang ditanya soalmu."]} />
            <QuizCard
              questionId="intro-python"
              prompt="Apa output dari print(1 + 1)?"
              choices={["11", "2", "'1 + 1'"]}
            />
          </div>
        </div>
      </div>
    </AuthGuard>
  );
}
