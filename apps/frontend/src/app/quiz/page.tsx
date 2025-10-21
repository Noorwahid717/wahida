"use client";

import { useQuery } from "@tanstack/react-query";

import { QuizCard } from "@/components/quiz-card";
import { AuthGuard } from "@/components/auth-guard";
import { authenticatedFetch, API_BASE_URL } from "@/lib/api";
import { queryKeys } from "@/lib/query-keys";

interface QuizQuestion {
  id: string;
  prompt: string;
  choices: string[];
  answer_index: number;
}

async function fetchQuiz(): Promise<QuizQuestion> {
  const response = await authenticatedFetch(`${API_BASE_URL}/api/quiz/550e8400-e29b-41d4-a716-446655440001`);
  if (!response.ok) {
    throw new Error("Gagal memuat kuis");
  }
  return response.json();
}

export default function QuizPage() {
  const { data, isLoading, error } = useQuery({ queryKey: queryKeys.quiz("550e8400-e29b-41d4-a716-446655440001"), queryFn: fetchQuiz });

  return (
    <AuthGuard>
      <div className="mx-auto flex w-full max-w-3xl flex-col gap-6 px-6 py-12">
        <header>
          <h1 className="text-3xl font-bold text-foreground">Kuis Adaptif</h1>
          <p className="text-sm text-muted-foreground">Latih pemahamanmu dan dapatkan feedback instan.</p>
        </header>
        {isLoading && <p className="text-sm text-muted-foreground">Memuat soal...</p>}
        {error && <p className="text-sm text-destructive">{String(error)}</p>}
        {data && <QuizCard questionId={data.id} prompt={data.prompt} choices={data.choices} />}
      </div>
    </AuthGuard>
  );
}
