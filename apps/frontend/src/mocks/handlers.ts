import { http, HttpResponse } from "msw";

export const handlers = [
  // Mock Chat API
  http.post("http://localhost:8000/api/chat", async () => {
    // Simulate streaming chunks
    const chunks = [
      {
        type: "chunk",
        text: "Persamaan linear adalah bentuk ax + b = c.",
        metadata: { kelas: "X", topik: "Persamaan Linear" },
        score: 0.9,
        hintsRevealed: 0,
      },
      {
        type: "chunk",
        text: "Untuk menyelesaikan, kurangkan b dari kedua sisi.",
        metadata: { kelas: "X", topik: "Persamaan Linear" },
        score: 0.8,
        hintsRevealed: 1,
      },
    ];

    // Simulate delay for streaming
    await new Promise((resolve) => setTimeout(resolve, 1000));

    // Return LLM response
    return HttpResponse.json({
      type: "response",
      text: "Untuk menyelesaikan persamaan linear ax + b = c, kurangkan b dari kedua sisi: ax = c - b. Kemudian bagi kedua sisi dengan a: x = (c - b)/a. Pastikan a tidak nol!",
    });
  }),

  // Mock Quiz API
  http.get("http://localhost:8000/api/quiz/:questionId", () => {
    return HttpResponse.json({
      id: "intro-python",
      prompt: "Apa output dari print(1 + 1)?",
      choices: ["11", "2", "'1 + 1'"],
      answer_index: 1,
    });
  }),

  http.post("http://localhost:8000/api/quiz/:questionId", async ({ request }) => {
    const body = await request.json();
    const isCorrect = body.selected_index === 1; // Mock correct answer
    return HttpResponse.json({
      correct: isCorrect,
      submitted_at: new Date().toISOString(),
    });
  }),

  // Mock Progress API
  http.get("http://localhost:8000/api/progress/:userId", () => {
    return HttpResponse.json({
      user_id: "user123",
      streak_days: 5,
      badges: ["starter", "consistent-learner"],
      last_active: "2025-10-17",
    });
  }),

  // Mock Run API
  http.post("http://localhost:8000/api/run", async ({ request }) => {
    const body = await request.json();
    // Mock code execution
    return HttpResponse.json({
      stdout: `Executed ${body.language} safely: ${body.source.slice(0, 50)}...`,
      status: "completed",
      execution_time_ms: 150,
    });
  }),

  // Mock Health Check
  http.get("http://localhost:8000/healthz", () => {
    return HttpResponse.json({ status: "ok" });
  }),
];