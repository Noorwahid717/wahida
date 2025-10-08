# Kontribusi ke Wahida

## Persiapan Lingkungan

1. Install [Poetry](https://python-poetry.org/) dan jalankan `poetry install` di `apps/api`.
2. Install dependency frontend dengan `pnpm install` di `apps/frontend`.
3. Salin `.env.example` menjadi `.env` dan sesuaikan kredensial jika diperlukan.
4. Gunakan `docker compose up --build` untuk menjalankan Postgres, Redis, Judge0, FastAPI, dan Next.js dalam satu perintah.

## Alur Kerja

- Gunakan branch feature dan buka pull request ke `main`.
- Setiap PR wajib melalui pipeline GitHub Actions: lint (ruff/eslint), mypy, pytest, build Next.js, dan smoke test Playwright.
- Sertakan deskripsi perubahan, langkah uji, serta screenshot bila menyentuh UI.

## Standar Kode

- Backend mengikuti panduan `ruff` dan `mypy`. Hindari logika bisnis di router; gunakan service layer.
- Frontend memakai TypeScript, React Server Components, dan TanStack Query. Kunci query berada di `src/lib/query-keys.ts`.
- Dokumentasikan arsitektur baru melalui ADR di `docs/adr`.

## Testing

- Backend: `poetry run pytest` untuk unit test, `poetry run ruff check .`, dan `poetry run mypy app`.
- Frontend: `pnpm lint`, `pnpm build`, dan `pnpm test:e2e` untuk smoke test Playwright.

Selamat berkontribusi! 🎉
