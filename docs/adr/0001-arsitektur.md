# ADR 0001 – Arsitektur Awal Wahida

## Status
Disetujui – Sprint 0.

## Konteks
Wahida adalah asisten belajar berbasis RAG dengan kebutuhan fitur chat, materi, kuis, dan eksekusi kode. Tim membutuhkan fondasi monorepo yang mendukung iterasi cepat, pipeline CI/CD, dan infrastruktur dev menyatu.

## Keputusan
- Menggunakan monorepo dengan struktur `apps/api` (FastAPI) dan `apps/frontend` (Next.js).
- Menyediakan docker-compose untuk menjalankan Postgres+pgvector, Redis, Judge0, API, dan web dalam satu perintah.
- Menetapkan pipeline GitHub Actions untuk lint/test backend, lint/build frontend, serta smoke test Playwright opsional.
- Menyusun RAG service sederhana berbasis FAISS yang dapat diperluas ke pgvector.
- Menyediakan konten markdown bertingkat dan skrip ingest untuk proses chunking dan embedding.

## Konsekuensi
- Pengembang memiliki lingkungan lokal standar yang selaras dengan pipeline produksi.
- RAG service dapat diupgrade tanpa mengganti kontrak API.
- Penambahan fitur baru memiliki panduan dokumentasi (ADR, CONTRIBUTING, SECURITY).
