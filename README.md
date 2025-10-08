
# WAHIDA

Wahidiyah Digital Assistant

## Struktur Repositori

* `apps/frontend` – Next.js App Router + TypeScript dengan Tailwind, TanStack Query, Zustand, dan shadcn/ui siap pakai.
* `apps/api` – FastAPI + Poetry yang menyiapkan router `/chat`, `/run`, `/quiz`, dan `/progress` sebagai pondasi integrasi layanan AI.
* `infra` – Direktori kosong untuk skrip infrastruktur (Terraform/Docker/Kubernetes) sesuai roadmap.
* `.pre-commit-config.yaml` – Konfigurasi ruff + mypy sesuai standar kualitas kode Python.

## Menjalankan Proyek

### Pilihan 1 – Docker Compose (disarankan)

```bash
docker compose up --build
```

Setelah perintah di atas:

* FastAPI tersedia di [http://localhost:8000](http://localhost:8000)
* Next.js tersedia di [http://localhost:3000](http://localhost:3000)

### Pilihan 2 – Lokal Manual

Prasyarat: Node.js 18+, pnpm, Python 3.11, Poetry.

```bash
# Backend
cd apps/api
poetry install
poetry run uvicorn app.main:app --reload

# Frontend
cd ../frontend
pnpm install
pnpm dev
```

### Ingest Konten Markdown

```bash
poetry run python scripts/ingest_markdown.py --content-dir content --faiss-path data/faiss/index.bin
```

## Arsitektur MVP → Produksi

### Rencana Implementasi Bertahap

1. **Sprint 0 – Fondasi**

   * Provisioning repositori mono (apps `frontend` & `api`, direktori `infra`).
   * Menyiapkan workflow CI lint/test (Turborepo + GitHub Actions) dan guard konvensi commit.
   * Bootstrap Next.js App Router + TypeScript dengan shadcn/ui, Tailwind, TanStack Query, dan Zustand.
   * Bootstrap FastAPI + Poetry + pre-commit (ruff, mypy) dan konfigurasi env (`.env.example`).
   * Konfigurasi Supabase (Postgres + Auth + Storage) dan membuat skema dasar.

2. **Sprint 1 – Chat & Materi**

   * Implementasi halaman materi (ISR) dan chat tutor di Next.js.
   * Endpoint FastAPI `/chat` dengan pipeline RAG (vector store FAISS) + moderation.
   * Integrasi embedding (OpenAI `text-embedding-3-small`) dan penyusunan proses chunking materi.
   * Sinkronisasi materi → FAISS via Celery worker.

3. **Sprint 2 – Kuis & Progres**

   * Halaman kuis, leaderboard, dan state progres (streak, badges) di frontend.
   * Endpoint `/quiz` untuk bank soal & grading dan `/progress` untuk rekap progres.
   * Persistensi attempts/streak/badges di Postgres + pgvector (opsional migrasi).
   * Integrasi PostHog untuk event pembelajaran.

4. **Sprint 3 – Eksekusi Kode & Observabilitas**

   * Integrasi endpoint `/run` yang memanggil Judge0 atau runner Docker via Celery queue.
   * Implementasi SSE → WebSocket upgrade untuk feedback granular.
   * Observabilitas: OpenTelemetry tracing, logging terstruktur, alert dasar.

5. **Sprint 4 – Hardening Produksi**

   * Scale-up vector index (pgvector/Pinecone) dan opsi model OSS (Llama 3 8B, Mistral 7B).
   * Penambahan re-ranker (Cohere / `bge-reranker-large`).
   * Hardening keamanan (rate limiting, audit log, PII scrubbing otomatis) dan playbook on-call.

6. **Sprint 5 – Ekosistem Guru & Integrasi**

   * Dashboard guru dengan ringkasan progres kelas dan exports.
   * Integrasi LMS eksternal (jika perlu) via webhook/CSV.
   * Evaluasi A/B via feature flag Unleash atau toggle database.

### Frontend

* **Framework**: Next.js (App Router) dengan TypeScript untuk dukungan SSR/ISR pada materi dan kuis, serta komponen client untuk fitur chat.
* **UI**: Tailwind CSS dipadukan dengan shadcn/ui untuk komponen siap pakai.
* **State & Data**: TanStack Query sebagai lapisan data (caching & retry) ditambah Zustand untuk state UI ringan.
* **Visualisasi**: Chart.js atau Recharts guna menampilkan grafik progres belajar.

### Backend

* **Framework**: FastAPI (Python) menyediakan endpoint untuk chat, RAG, eksekusi tes kode, dan kuis sehingga mudah terhubung dengan model serta pustaka Python.
* **Worker/Queue (opsional)**: Celery + Redis untuk mengeksekusi kode dan melakukan scoring secara non-blocking.

### LLM & Embedding

* **MVP**: Menggunakan API komersial (OpenAI/Cohere/Mistral) untuk jawaban dan embedding demi kemudahan serta biaya awal yang efisien.
* **Alternatif OSS**: Model seperti Llama 3 8B, Mistral 7B, atau Phi-3 untuk kebutuhan tutoring ringan pada infrastruktur sendiri.
* **Embedding**: `text-embedding-3-small` (OpenAI) atau `bge-small` (OSS).
* **Re-ranker (scale-up)**: Cohere Rerank atau `bge-reranker-large` saat kebutuhan meningkat.

### Vector Index

* **MVP**: FAISS in-process untuk performa dan biaya rendah.
* **Produksi**: pgvector di PostgreSQL atau layanan terkelola seperti Pinecone.

### Database & Autentikasi

* **Database**: PostgreSQL (Supabase/Railway/Neon) dengan pgvector saat skala menuntut.
* **Auth**: Supabase Auth atau NextAuth (magic link email / Google SSO).
* **Storage**: Supabase Storage untuk aset materi dan contoh CSV.

### Sandbox Eksekusi Python

* **MVP**: Judge0 (SaaS/self-host) dengan batasan runtime 2–3 detik, memori, dan tanpa akses jaringan.
* **Produksi**: Docker jailed runner (Firecracker, gVisor, atau nsjail) dipadukan antrean Celery.

### Hosting

* **Frontend**: Vercel.
* **Backend & Worker**: Railway, Fly.io, atau Render yang andal untuk WebSocket/long-running service.
* **Komunikasi Real-time**: Gunakan Server-Sent Events (SSE) untuk MVP, lalu beralih ke WebSocket untuk feedback yang lebih granular.

### Analytics & Logging

* **Monitoring**: PostHog untuk event & funnel, Plausible untuk analitik ringan, dan OpenTelemetry untuk tracing minimal.
* **Feature Flag**: Unleash atau konfigurasi di database guna mengatur mode latihan/proyek/kebijakan AI.

### Moderation & Safety

* **Moderasi**: API moderasi (OpenAI/Google) dipadu dengan regex/policy lokal, termasuk filter PR otomatis.
* **Privasi**: Pembersihan PII dengan aturan sederhana serta daftar putih (contoh: nama depan tanpa NISN).

## Arsitektur Logis

```
[Next.js App Router]
  ├─ Halaman: /chat, /materi/[id], /quiz/[id], /latihan, /leaderboard
  ├─ State: TanStack Query (server state), Zustand (UI state)
  └─ /api/* proxy → FastAPI backend (SSE/WebSocket untuk chat & progres)

[FastAPI Service]
  ├─ /api/chat      → Router chat (RAG + Prompting + Moderation)
  ├─ /api/run       → Sandbox runner (Judge0/Docker) via Celery task
  ├─ /api/quiz      → Bank soal, auto-grading, rekomendasi remedi
  ├─ /api/progress  → Streak, badges, ringkasan guru, PostHog event hook
  ├─ Background     → Celery worker (batch indexing, scoring) + Redis queue
  └─ Observability  → OpenTelemetry exporter + logging terstruktur

[Data Layer]
  ├─ PostgreSQL: users, classes, contents, content_chunks, embeddings (pgvector), attempts, streaks, badges
  ├─ Vector Index: FAISS (MVP) → pgvector/Pinecone (produksi)
  ├─ Object Storage: materi markdown, media, dataset kuis
  └─ Analytics: PostHog events & funnels

[LLM & AI Layer]
  ├─ LLM Provider: OpenAI/Cohere/Mistral API (MVP) → Llama 3 8B / Mistral 7B self-hosted
  ├─ Embedding: text-embedding-3-small / bge-small
  └─ Re-ranker: Cohere Rerank / bge-reranker-large

[Security & Safety]
  ├─ AuthN/AuthZ: Supabase Auth / NextAuth + role-based guard
  ├─ Moderation API + policy lokal (regex, denylist)
  └─ PII scrubbing + audit log
```

## Skema Data Inti

| Tabel              | Kolom Kunci                                                                                                |
| ------------------ | ---------------------------------------------------------------------------------------------------------- |
| `users`            | `id` (UUID), `name`, `role` (`student`/`teacher`/`parent`), `class_id` (nullable FK `classes.id`), `email` |
| `classes`          | `id` (UUID), `name`, `grade` (X/XI/XII)                                                                    |
| `contents`         | `id` (UUID), `class_id` (nullable FK), `title`, `grade`, `topic`, `level`, `md_url`, `tokens`              |
| `chunks`           | `id` (UUID), `content_id` (FK), `ord`, `text`, `tokens`, `metadata` (JSON: `{kelas, topik, level}`)        |
| `embeddings`       | `chunk_id` (PK & FK `chunks.id`), `vec` (`pgvector`, dimensi 1536 default)                                 |
| `exercises`        | `id` (UUID), `type` (`mcq`/`code`/`short`), `payload` (JSON), `answer_key` (JSON)                          |
| `attempts`         | `id` (UUID), `user_id` (FK), `exercise_id` (FK), `score`, `feedback`, `started_at`, `finished_at`          |
| `streaks`          | `user_id` (PK & FK), `current`, `longest`, `last_day_done`                                                 |
| `badges`           | `id` (UUID), `name`, `rule` (JSON), `icon`                                                                 |
| `user_badges`      | `id` (UUID), `user_id` (FK), `badge_id` (FK), `awarded_at`                                                 |
| `events_analytics` | `id` (UUID), `user_id` (nullable FK), `event_name`, `props` (JSON), `ts`                                   |

Model SQLAlchemy untuk tabel-tabel di atas tersedia pada `apps/api/app/models/core.py` dan siap digunakan oleh lapisan servis maupun migrasi ke depan.

## Alur Data Utama

1. **Chat Tutoring**

   * Pengguna membuka halaman `/chat`; Next.js melakukan prefetch profil & progres via TanStack Query.
   * Permintaan dikirim ke `/api/chat` → FastAPI memoderasi, menjalankan retrieval ke FAISS/pgvector, menyusun prompt, dan memanggil LLM.
   * Respons streaming via SSE/WebSocket ke frontend, disimpan di cache klien serta PostHog event `chat_response`.

2. **Kuis & Leaderboard**

   * Halaman `/quiz/[id]` memuat soal via `/api/quiz`; hasil submission dikirim asinkron ke Celery untuk penilaian kode (bila perlu).
   * Endpoint `/api/progress` mengagregasi attempts → streak/badge di Postgres dan memancarkan ringkasan untuk dashboard guru dan leaderboard.

3. **Eksekusi Kode**

   * Frontend latihan mengirim payload ke `/api/run`.
   * FastAPI mengirim tugas ke Celery + Redis → runner Judge0/Docker mengeksekusi sandbox dan mengembalikan output, lalu ditulis ke Postgres untuk audit.

4. **Indexing Konten**

   * Materi baru diunggah ke Object Storage → webhook memicu worker Celery.
   * Worker melakukan chunking (300–700 token), embedding, dan memperbarui FAISS/pgvector, sekaligus mencatat versi ke tabel `contents`.

### Catatan Infrastruktur

* **Frontend Deployment**: Vercel (preview & produksi) dengan environment secret terhubung ke backend.
* **Backend Deployment**: Railway/Fly.io dengan konfigurasi autoscaling ringan, Redis managed, dan Celery worker terpisah.
* **Pipeline CI/CD**: Otomatis lint/test + deploy preview; gating via review & moderasi konten.
