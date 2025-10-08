# Infrastruktur Lokal

Gunakan `docker compose up --build` untuk menyalakan seluruh layanan pengembangan:

- **postgres**: Postgres + pgvector dengan konfigurasi khusus pada `infra/postgresql/postgresql.conf`.
- **redis**: cache & antrean untuk Celery.
- **judge0**: sandbox eksekusi kode.
- **api**: FastAPI berjalan di port 8000.
- **web**: Next.js berjalan di port 3000.

Semua layanan membaca file `.env` (untuk backend) dan variabel environment bawaan dari `docker-compose.yml`.
