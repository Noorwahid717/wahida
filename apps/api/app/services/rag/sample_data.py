from __future__ import annotations

from .types import ModuleDocument

SAMPLE_MODULES: list[ModuleDocument] = [
    ModuleDocument(
        module_id="math-limit-derivative",
        title="Limit dan Turunan Dasar",
        grade="XI",
        topic="Kalkulus",
        level="menengah",
        collection="default",
        markdown="""
# Limit Fungsi
Limit menggambarkan perilaku suatu fungsi saat variabel mendekati nilai tertentu. Untuk fungsi f(x), limit ditulis sebagai lim_{x->a} f(x). Jika nilai f(x) semakin mendekati L ketika x mendekati a, maka limitnya adalah L.

## Aturan Limit Penting
- Limit jumlah adalah jumlah dari limit.
- Limit hasil kali adalah hasil kali limit.
- Limit dari fungsi pecahan bergantung pada limit pembilang dan penyebut, selama penyebut tidak menuju 0.

## Contoh Soal
Hitung limit berikut:
```math
lim_{x->2} (3x^2 - 5x + 2)
```
Solusi: substitusi langsung menghasilkan 3(4) - 10 + 2 = 4.

# Turunan Pertama
Turunan pertama menyatakan laju perubahan fungsi. Definisi turunan: f'(x) = lim_{h->0} (f(x+h) - f(x)) / h.

## Aturan Turunan
- Turunan konstanta adalah 0.
- Turunan x^n adalah n * x^{n-1}.
- Turunan dari hasil kali dan hasil bagi mengikuti aturan khusus.

## Latihan Kode Python
```python
import sympy as sp
x = sp.symbols('x')
expr = 3*x**2 - 5*x + 2
print(sp.diff(expr, x))
```
""",
    ),
    ModuleDocument(
        module_id="ai-literacy-ethics",
        title="Etika AI dan Bias",
        grade="X",
        topic="AI Literacy",
        level="dasar",
        collection="ai_literacy",
        markdown="""
# Etika AI
Penggunaan AI harus mempertimbangkan prinsip keadilan, transparansi, dan akuntabilitas. Guru dan siswa perlu memahami bagaimana model dilatih dan data apa yang digunakan.

## Bias dalam Model
Bias dapat muncul dari data yang tidak seimbang atau asumsi desain. Dampaknya adalah keputusan yang tidak adil terhadap kelompok tertentu.

## Privasi dan Data
Selalu pastikan data pribadi dilindungi. Terapkan minimisasi data dan izin eksplisit sebelum mengumpulkan informasi sensitif.

## Latihan Diskusi
Tuliskan dua contoh risiko privasi ketika menggunakan aplikasi bertenaga AI di sekolah dan bagaimana cara mitigasinya.
""",
    ),
]
