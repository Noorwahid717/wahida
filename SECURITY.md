# Keamanan Wahida

## Melaporkan Kerentanan

Laporkan potensi kerentanan ke security@wahida.id. Sertakan deskripsi, langkah reproduksi, dan dampak.

## Kebijakan Patching

- Patches kritis: maksimal 24 jam.
- Patches tinggi: maksimal 72 jam.
- Patches sedang/rendah: digabung dalam rilis minor berikutnya.

## Praktik Keamanan

- Moderasi konten sebelum menjalankan pipeline RAG (`/api/chat`).
- Rate limiting di endpoint sensitif (`/api/chat`, `/api/run`).
- Sandbox eksekusi kode (timeout 3 detik, blokir akses jaringan) sebelum integrasi Judge0 penuh.
- Simpan rahasia hanya melalui environment variable dan secret manager.

## Dependensi

Gunakan `poetry export` dan `pnpm audit` untuk memantau CVE. Update rutin minimal setiap sprint.
