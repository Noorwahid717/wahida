---
kelas: XI
topik: Algoritma Lanjutan
level: lanjutan
title: Algoritma Sorting dan Searching
tags:
  - algoritma
  - sorting
  - searching
  - python
  - kompleksitas
---

# Algoritma Sorting dan Searching

Pelajari algoritma fundamental untuk mengurutkan dan mencari data dengan efisien.

## Konsep Dasar Kompleksitas

Sebelum mempelajari algoritma, pahami konsep kompleksitas waktu:

- **O(1)** - Waktu konstan
- **O(log n)** - Logaritmik (sangat efisien)
- **O(n)** - Linear
- **O(n log n)** - Linear logaritmik (baik untuk sorting)
- **O(n²)** - Kuadratik (lambat untuk data besar)

## Algoritma Sorting

### Bubble Sort (O(n²))
```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        # Flag untuk optimasi
        swapped = False
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        # Jika tidak ada swap, array sudah terurut
        if not swapped:
            break
    return arr

# Contoh penggunaan
data = [64, 34, 25, 12, 22, 11, 90]
print("Sebelum:", data)
bubble_sort(data)
print("Sesudah:", data)
```

### Selection Sort (O(n²))
```python
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        # Cari elemen terkecil di sisa array
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j

        # Swap elemen terkecil dengan posisi i
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

    return arr

# Contoh
data = [64, 25, 12, 22, 11]
selection_sort(data)
print(data)  # [11, 12, 22, 25, 64]
```

### Insertion Sort (O(n²))
```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        # Geser elemen yang lebih besar dari key
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key

    return arr

# Contoh
data = [12, 11, 13, 5, 6]
insertion_sort(data)
print(data)  # [5, 6, 11, 12, 13]
```

### Quick Sort (O(n log n) rata-rata)
```python
def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    # Pilih pivot (elemen tengah)
    pivot = arr[len(arr) // 2]

    # Bagi menjadi 3 bagian
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    # Rekursi
    return quick_sort(left) + middle + quick_sort(right)

# Contoh
data = [3, 6, 8, 10, 1, 2, 1]
print(quick_sort(data))  # [1, 1, 2, 3, 6, 8, 10]
```

### Merge Sort (O(n log n))
```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    # Bagi array menjadi dua
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0

    # Gabungkan kedua array
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Tambahkan sisa elemen
    result.extend(left[i:])
    result.extend(right[j:])

    return result

# Contoh
data = [38, 27, 43, 3, 9, 82, 10]
print(merge_sort(data))  # [3, 9, 10, 27, 38, 43, 82]
```

## Algoritma Searching

### Linear Search (O(n))
```python
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i  # Return index
    return -1  # Not found

# Contoh
data = [2, 3, 4, 10, 40]
target = 10
result = linear_search(data, target)
print(f"Elemen ditemukan di index: {result}")
```

### Binary Search (O(log n))
*Hanya untuk array terurut*
```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1

# Contoh
data = [2, 3, 4, 10, 40, 50, 60]  # Harus terurut
target = 10
result = binary_search(data, target)
print(f"Elemen ditemukan di index: {result}")
```

### Binary Search Rekursif
```python
def binary_search_recursive(arr, target, left=0, right=None):
    if right is None:
        right = len(arr) - 1

    if left > right:
        return -1

    mid = (left + right) // 2

    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)

# Contoh
data = [2, 3, 4, 10, 40]
target = 10
result = binary_search_recursive(data, target)
print(f"Elemen ditemukan di index: {result}")
```

## Perbandingan Algoritma

| Algoritma | Best Case | Average Case | Worst Case | Stable? |
|-----------|-----------|--------------|------------|---------|
| Bubble Sort | O(n) | O(n²) | O(n²) | Yes |
| Selection Sort | O(n²) | O(n²) | O(n²) | No |
| Insertion Sort | O(n) | O(n²) | O(n²) | Yes |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | No |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | Yes |
| Linear Search | O(1) | O(n) | O(n) | - |
| Binary Search | O(1) | O(log n) | O(log n) | - |

## Studi Kasus: Sistem Manajemen Siswa

```python
class Siswa:
    def __init__(self, nama, nilai):
        self.nama = nama
        self.nilai = nilai

    def __str__(self):
        return f"{self.nama}: {self.nilai}"

class SistemManajemenSiswa:
    def __init__(self):
        self.siswa = []

    def tambah_siswa(self, nama, nilai):
        siswa_baru = Siswa(nama, nilai)
        self.siswa.append(siswa_baru)

    def urutkan_berdasarkan_nilai(self):
        # Bubble sort berdasarkan nilai (descending)
        n = len(self.siswa)
        for i in range(n):
            for j in range(0, n-i-1):
                if self.siswa[j].nilai < self.siswa[j+1].nilai:
                    self.siswa[j], self.siswa[j+1] = self.siswa[j+1], self.siswa[j]

    def cari_siswa(self, nama):
        # Linear search
        for i, siswa in enumerate(self.siswa):
            if siswa.nama == nama:
                return i
        return -1

    def tampilkan_semua(self):
        for siswa in self.siswa:
            print(siswa)

# Penggunaan
sistem = SistemManajemenSiswa()

# Tambah data siswa
sistem.tambah_siswa("Ahmad", 85)
sistem.tambah_siswa("Budi", 92)
sistem.tambah_siswa("Cici", 78)
sistem.tambah_siswa("Dedi", 88)

print("=== Sebelum Sorting ===")
sistem.tampilkan_semua()

sistem.urutkan_berdasarkan_nilai()

print("\n=== Sesudah Sorting (Nilai Tertinggi) ===")
sistem.tampilkan_semua()

print("\n=== Pencarian Siswa ===")
index = sistem.cari_siswa("Cici")
if index != -1:
    print(f"Cici ditemukan di posisi {index + 1}")
else:
    print("Cici tidak ditemukan")
```

## Latihan

1. **Implementasi Algoritma**: Buat implementasi lengkap dari semua algoritma sorting
2. **Perbandingan Performa**: Bandingkan waktu eksekusi berbagai algoritma sorting dengan data berbeda ukuran
3. **Optimasi**: Modifikasi algoritma untuk performa lebih baik
4. **Aplikasi Nyata**: Buat sistem yang menggunakan sorting dan searching untuk kasus dunia nyata

## Kesimpulan

- **Pilih algoritma berdasarkan kasus penggunaan**
- **Untuk data kecil**: Bubble, Selection, atau Insertion Sort cukup
- **Untuk data besar**: Quick Sort atau Merge Sort
- **Binary Search** jauh lebih efisien dari Linear Search untuk data terurut
- **Pahami kompleksitas** untuk memilih algoritma yang tepat