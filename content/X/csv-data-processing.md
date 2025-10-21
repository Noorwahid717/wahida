---
kelas: X
topik: Pemrosesan Data
level: menengah
title: Membaca dan Memproses File CSV dengan Python
tags:
  - python
  - csv
  - data-processing
  - file-handling
---

# Pemrosesan File CSV di Python

Pelajari cara membaca, memproses, dan menganalisis data dari file CSV.

## Apa itu CSV?

CSV (Comma-Separated Values) adalah format file untuk menyimpan data tabular dalam bentuk teks. Setiap baris mewakili satu record, dan kolom dipisahkan oleh koma.

Contoh file `siswa.csv`:
```
nama,kelas,matematika,ipa,ips
Ahmad,X IPA,85,88,82
Budi,X IPS,78,75,90
Cici,X IPA,92,89,85
```

## Membaca File CSV

### Menggunakan Built-in CSV Module

```python
import csv

# Membaca file CSV
def baca_csv(nama_file):
    data = []
    with open(nama_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)

        # Baca header
        header = next(csv_reader)
        print(f"Header: {header}")

        # Baca data
        for row in csv_reader:
            data.append(row)

    return header, data

# Penggunaan
header, data = baca_csv('siswa.csv')
print(f"Jumlah siswa: {len(data)}")
```

### Menggunakan CSV sebagai Dictionary

```python
import csv

def baca_csv_dict(nama_file):
    data = []
    with open(nama_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            data.append(dict(row))

    return data

# Penggunaan
siswa = baca_csv_dict('siswa.csv')
for s in siswa:
    print(f"Nama: {s['nama']}, Rata-rata: {(int(s['matematika']) + int(s['ipa']) + int(s['ips'])) / 3:.1f}")
```

## Menulis File CSV

```python
import csv

def tulis_csv(nama_file, header, data):
    with open(nama_file, 'w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)

        # Tulis header
        csv_writer.writerow(header)

        # Tulis data
        for row in data:
            csv_writer.writerow(row)

# Contoh penggunaan
header = ['nama', 'kelas', 'nilai']
data = [
    ['Ahmad', 'X IPA', 85],
    ['Budi', 'X IPS', 90],
    ['Cici', 'X IPA', 88]
]

tulis_csv('hasil.csv', header, data)
```

## Menggunakan Pandas (Alternatif Modern)

```python
import pandas as pd

# Membaca CSV dengan pandas
df = pd.read_csv('siswa.csv')

# Menampilkan info dasar
print(df.head())      # 5 baris pertama
print(df.info())      # Info kolom dan tipe data
print(df.describe())  # Statistik deskriptif

# Mengakses kolom
print(df['nama'])           # Kolom nama
print(df['matematika'].mean())  # Rata-rata matematika

# Filter data
siswa_ipa = df[df['kelas'] == 'X IPA']
print(siswa_ipa)

# Menyimpan hasil
df.to_csv('hasil_analisis.csv', index=False)
```

## Analisis Data Sederhana

```python
import csv

def analisis_nilai(nama_file):
    matematika = []
    ipa = []
    ips = []

    with open(nama_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            matematika.append(int(row['matematika']))
            ipa.append(int(row['ipa']))
            ips.append(int(row['ips']))

    # Hitung statistik
    def rata_rata(data):
        return sum(data) / len(data) if data else 0

    def maksimum(data):
        return max(data) if data else 0

    def minimum(data):
        return min(data) if data else 0

    print("=== ANALISIS NILAI ===")
    print(f"Rata-rata Matematika: {rata_rata(matematika):.1f}")
    print(f"Rata-rata IPA: {rata_rata(ipa):.1f}")
    print(f"Rata-rata IPS: {rata_rata(ips):.1f}")
    print()
    print(f"Nilai Tertinggi Matematika: {maksimum(matematika)}")
    print(f"Nilai Tertinggi IPA: {maksimum(ipa)}")
    print(f"Nilai Tertinggi IPS: {maksimum(ips)}")

# Penggunaan
analisis_nilai('siswa.csv')
```

## Studi Kasus: Sistem Report Nilai

```python
import csv

class SistemNilai:
    def __init__(self, file_csv):
        self.file_csv = file_csv
        self.data = self.load_data()

    def load_data(self):
        data = []
        try:
            with open(self.file_csv, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    # Konversi nilai ke integer
                    row['matematika'] = int(row['matematika'])
                    row['ipa'] = int(row['ipa'])
                    row['ips'] = int(row['ips'])
                    data.append(row)
        except FileNotFoundError:
            print(f"File {self.file_csv} tidak ditemukan")
        return data

    def hitung_rata_rata(self, siswa):
        return (siswa['matematika'] + siswa['ipa'] + siswa['ips']) / 3

    def generate_report(self):
        if not self.data:
            print("Tidak ada data siswa")
            return

        print("=== REPORT NILAI KELAS ===")
        print(f"Total Siswa: {len(self.data)}")
        print()

        # Urutkan berdasarkan rata-rata (tertinggi ke terendah)
        sorted_data = sorted(self.data,
                           key=lambda x: self.hitung_rata_rata(x),
                           reverse=True)

        for i, siswa in enumerate(sorted_data, 1):
            rata_rata = self.hitung_rata_rata(siswa)
            status = "Lulus" if rata_rata >= 75 else "Remedial"

            print(f"{i}. {siswa['nama']} ({siswa['kelas']})")
            print(f"   Matematika: {siswa['matematika']}")
            print(f"   IPA: {siswa['ipa']}")
            print(f"   IPS: {siswa['ips']}")
            print(f"   Rata-rata: {rata_rata:.1f}")
            print(f"   Status: {status}")
            print()

# Penggunaan
sistem = SistemNilai('siswa.csv')
sistem.generate_report()
```

## Tips Kerja dengan CSV

1. **Selalu gunakan encoding utf-8** untuk dukungan karakter Indonesia
2. **Handle error file tidak ditemukan** dengan try-except
3. **Konversi tipe data** saat diperlukan (string ke int/float)
4. **Gunakan DictReader** untuk kemudahan akses kolom
5. **Validasi data** sebelum diproses
6. **Backup file asli** sebelum melakukan perubahan

## Latihan

1. **Import Data Siswa**: Buat program yang membaca data siswa dari CSV dan menampilkan statistik
2. **Export Hasil**: Buat program yang menghitung nilai akhir dan menyimpan ke CSV baru
3. **Filter Data**: Buat program yang memfilter siswa berdasarkan kriteria tertentu
4. **Data Cleaning**: Buat program yang membersihkan dan memvalidasi data CSV