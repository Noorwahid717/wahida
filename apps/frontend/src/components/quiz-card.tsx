"use client";

import { useMutation } from "@tanstack/react-query";

import { API_BASE_URL, authenticatedFetch } from "@/lib/api";

interface QuizCardProps {
  questionId: string;
  prompt: string;
  choices: string[];
}

async function submitAnswer(questionId: string, selectedIndex: number) {
  const response = await authenticatedFetch(`${API_BASE_URL}/api/quiz/${questionId}`, {
    method: "POST",
    body: JSON.stringify({ question_id: questionId, selected_index: selectedIndex }),
  });
  if (!response.ok) {
    throw new Error("Gagal mengirim jawaban");
  }
  return (await response.json()) as { correct: boolean };
}

export function QuizCard({ questionId, prompt, choices }: QuizCardProps) {
  const mutation = useMutation({
    mutationFn: ({ choice }: { choice: number }) => submitAnswer(questionId, choice),
  });

  return (
    <article className="rounded-lg border bg-card p-6 shadow-sm">
      <h3 className="text-lg font-semibold text-card-foreground">{prompt}</h3>
      <ul className="mt-4 space-y-3">
        {choices.map((choice, idx) => (
          <li key={idx}>
            <button
              type="button"
              onClick={() => mutation.mutate({ choice: idx })}
              className="w-full rounded-md border bg-background px-4 py-3 text-left text-sm text-foreground hover:bg-accent hover:text-accent-foreground transition-colors"
            >
              {choice}
            </button>
          </li>
        ))}
      </ul>
      {mutation.isSuccess && (
        <p className={`mt-4 text-sm font-medium ${mutation.data.correct ? "text-green-600 dark:text-green-400" : "text-destructive"}`}>
          {mutation.data.correct ? "Jawaban benar!" : "Belum tepat, coba lagi."}
        </p>
      )}
      {mutation.isError && <p className="mt-4 text-xs text-destructive">Gagal menilai jawaban.</p>}
    </article>
  );
}
