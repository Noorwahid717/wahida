---
kelas: X
topik: Struktur Data Python
level: menengah
title: List, Dictionary, dan Loop di Python
tags:
  - python
  - struktur-data
  - loop
  - list
  - dictionary
---

# Struktur Data dan Loop di Python

Pahami cara mengorganisir dan memproses data menggunakan struktur data Python.

## List (Daftar)

List adalah struktur data yang bisa menyimpan banyak item dalam satu variabel.

```python
# Membuat list
buah = ["apel", "jeruk", "mangga", "pisang"]
angka = [1, 2, 3, 4, 5]
campuran = ["teks", 123, True, 45.67]

# Mengakses elemen
print(buah[0])    # Output: apel
print(buah[-1])   # Output: pisang (elemen terakhir)

# Menambah elemen
buah.append("durian")
buah.insert(1, "anggur")

# Menghapus elemen
buah.remove("jeruk")
terakhir = buah.pop()  # Menghapus dan mengembalikan elemen terakhir

# Panjang list
print(len(buah))  # Output: jumlah elemen
```

## Dictionary (Kamus)

Dictionary menyimpan data dalam pasangan key-value.

```python
# Membuat dictionary
siswa = {
    "nama": "Ahmad",
    "kelas": "X IPA",
    "nilai": 85,
    "hobi": ["membaca", "coding"]
}

# Mengakses nilai
print(siswa["nama"])      # Output: Ahmad
print(siswa.get("kelas")) # Output: X IPA

# Menambah/mengubah
siswa["umur"] = 15
siswa["nilai"] = 90

# Menghapus
del siswa["hobi"]

# Iterasi
for key, value in siswa.items():
    print(f"{key}: {value}")
```

## Loop (Perulangan)

### For Loop
```python
# Loop melalui list
buah = ["apel", "jeruk", "mangga"]
for item in buah:
    print(f"Saya suka {item}")

# Loop dengan range
for i in range(5):  # 0, 1, 2, 3, 4
    print(f"Angka: {i}")

# Loop dengan index
for index, item in enumerate(buah):
    print(f"{index}: {item}")
```

### While Loop
```python
# Loop while
counter = 0
while counter < 5:
    print(f"Hitung: {counter}")
    counter += 1

# Loop dengan kondisi
jawaban = ""
while jawaban != "ya":
    jawaban = input("Apakah kamu mengerti? (ya/tidak): ")
```

## List Comprehension

Cara Pythonic untuk membuat list baru dari list yang ada.

```python
# Tanpa comprehension
angka = [1, 2, 3, 4, 5]
kuadrat = []
for x in angka:
    kuadrat.append(x ** 2)

# Dengan comprehension
kuadrat = [x ** 2 for x in angka]

# Dengan kondisi
genap = [x for x in angka if x % 2 == 0]
```

## Studi Kasus: Sistem Manajemen Siswa

```python
# Database siswa sederhana
siswa_db = []

def tambah_siswa(nama, kelas, nilai):
    siswa = {
        "nama": nama,
        "kelas": kelas,
        "nilai": nilai
    }
    siswa_db.append(siswa)
    print(f"Siswa {nama} berhasil ditambahkan")

def tampilkan_semua_siswa():
    for siswa in siswa_db:
        print(f"Nama: {siswa['nama']}, Kelas: {siswa['kelas']}, Nilai: {siswa['nilai']}")

def cari_siswa_terbaik():
    if not siswa_db:
        return None

    terbaik = siswa_db[0]
    for siswa in siswa_db:
        if siswa['nilai'] > terbaik['nilai']:
            terbaik = siswa
    return terbaik

# Penggunaan
tambah_siswa("Ahmad", "X IPA", 85)
tambah_siswa("Budi", "X IPS", 90)
tambah_siswa("Cici", "X IPA", 88)

tampilkan_semua_siswa()

terbaik = cari_siswa_terbaik()
if terbaik:
    print(f"Siswa terbaik: {terbaik['nama']} dengan nilai {terbaik['nilai']}")
```

## Latihan

1. **Manajemen Inventaris**: Buat program untuk mengelola inventaris toko menggunakan list dan dictionary
2. **Kalkulator Nilai**: Buat program yang menghitung rata-rata nilai siswa dari list nilai
3. **Game Tebak Angka**: Buat game tebak angka dengan loop dan kondisi
4. **Pengolah Data**: Buat program yang memproses data siswa dan menampilkan statistik