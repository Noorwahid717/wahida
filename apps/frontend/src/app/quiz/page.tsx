"use client";

import { useQuery } from "@tanstack/react-query";

import { QuizCard } from "@/components/quiz-card";
import { API_BASE_URL } from "@/lib/api";
import { queryKeys } from "@/lib/query-keys";

interface QuizQuestion {
  id: string;
  prompt: string;
  choices: string[];
  answer_index: number;
}

async function fetchQuiz(): Promise<QuizQuestion> {
  const response = await fetch(`${API_BASE_URL}/api/quiz/intro-python`);
  if (!response.ok) {
    throw new Error("Gagal memuat kuis");
  }
  return response.json();
}

export default function QuizPage() {
  const { data, isLoading, error } = useQuery({ queryKey: queryKeys.quiz("intro-python"), queryFn: fetchQuiz });

  return (
    <div className="mx-auto flex w-full max-w-3xl flex-col gap-6 px-6 py-12">
      <header>
        <h1 className="text-3xl font-bold text-slate-900">Kuis Adaptif</h1>
        <p className="text-sm text-slate-600">Latih pemahamanmu dan dapatkan feedback instan.</p>
      </header>
      {isLoading && <p className="text-sm text-slate-500">Memuat soal...</p>}
      {error && <p className="text-sm text-red-500">{String(error)}</p>}
      {data && <QuizCard questionId={data.id} prompt={data.prompt} choices={data.choices} />}
    </div>
  );
}
