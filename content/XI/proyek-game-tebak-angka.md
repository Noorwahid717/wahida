---
kelas: XI
topik: Proyek Mini
level: lanjutan
title: Membuat Game Tebak Angka dengan Python
tags:
  - python
  - proyek
  - game
  - loop
  - kondisi
---

# Proyek Mini: Game Tebak Angka Interaktif

Buat game tebak angka yang menarik dengan fitur scoring dan level kesulitan.

## Deskripsi Proyek

Kamu akan membuat game tebak angka di mana:
- Komputer memilih angka random antara 1-100
- Player harus menebak angka tersebut
- Ada petunjuk "terlalu tinggi" atau "terlalu rendah"
- Ada sistem scoring berdasarkan jumlah tebakan
- Ada level kesulitan (mudah, sedang, sulit)
- Ada statistik permainan

## Fitur yang Harus Ada

### 1. Menu Utama
```
=== GAME TEBAK ANGKA ===
1. Main Game
2. Lihat Statistik
3. Pengaturan
4. Keluar

Pilih menu (1-4):
```

### 2. Level Kesulitan
- **Mudah**: Angka 1-50, unlimited guesses
- **Sedang**: Angka 1-100, max 10 guesses
- **Sulit**: Angka 1-200, max 7 guesses

### 3. Sistem Scoring
```python
def hitung_score(jumlah_tebakan, level):
    base_score = {
        'mudah': 100,
        'sedang': 200,
        'sulit': 500
    }

    # Kurangi poin untuk setiap tebakan tambahan
    penalty = (jumlah_tebakan - 1) * 10

    score = base_score[level] - penalty
    return max(score, 10)  # Minimum score 10
```

### 4. Statistik Permainan
- Total permainan dimainkan
- Total menang/kalah
- Rata-rata tebakan per menang
- Score tertinggi
- Level favorit

## Struktur Kode

### File Utama: `game_tebak_angka.py`

```python
import random
import json
import os
from datetime import datetime

class GameTebakAngka:
    def __init__(self):
        self.stats_file = 'game_stats.json'
        self.stats = self.load_stats()

    def load_stats(self):
        if os.path.exists(self.stats_file):
            with open(self.stats_file, 'r') as f:
                return json.load(f)
        return {
            'total_games': 0,
            'wins': 0,
            'losses': 0,
            'total_guesses': 0,
            'best_score': 0,
            'level_stats': {'mudah': 0, 'sedang': 0, 'sulit': 0}
        }

    def save_stats(self):
        with open(self.stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)

    def get_random_number(self, level):
        ranges = {
            'mudah': 50,
            'sedang': 100,
            'sulit': 200
        }
        return random.randint(1, ranges[level])

    def get_max_guesses(self, level):
        limits = {
            'mudah': float('inf'),  # unlimited
            'sedang': 10,
            'sulit': 7
        }
        return limits[level]

    def calculate_score(self, guesses, level):
        base_scores = {'mudah': 100, 'sedang': 200, 'sulit': 500}
        penalty = (guesses - 1) * 10
        return max(base_scores[level] - penalty, 10)

    def play_game(self, level):
        target = self.get_random_number(level)
        max_guesses = self.get_max_guesses(level)
        guesses = 0
        guessed_numbers = []

        print(f"\n=== LEVEL {level.upper()} ===")
        print(f"Saya telah memilih angka antara 1-{target if level == 'mudah' else (100 if level == 'sedang' else 200)}")
        if max_guesses != float('inf'):
            print(f"Kamu punya {max_guesses} kesempatan menebak")

        while guesses < max_guesses:
            try:
                guess = int(input(f"\nTebakan ke-{guesses + 1}: "))

                if guess in guessed_numbers:
                    print("Kamu sudah menebak angka ini sebelumnya!")
                    continue

                guessed_numbers.append(guess)
                guesses += 1

                if guess == target:
                    score = self.calculate_score(guesses, level)
                    print(f"\n🎉 SELAMAT! Kamu menebak dengan benar!")
                    print(f"Angka yang benar adalah: {target}")
                    print(f"Jumlah tebakan: {guesses}")
                    print(f"Score kamu: {score} poin")

                    # Update stats
                    self.stats['total_games'] += 1
                    self.stats['wins'] += 1
                    self.stats['total_guesses'] += guesses
                    self.stats['best_score'] = max(self.stats['best_score'], score)
                    self.stats['level_stats'][level] += 1

                    return True

                elif guess < target:
                    print("📉 Terlalu kecil!")
                else:
                    print("📈 Terlalu besar!")

                # Hint untuk membantu
                if guesses >= 3:
                    diff = abs(guess - target)
                    if diff <= 5:
                        print("🔥 Kamu sudah sangat dekat!")
                    elif diff <= 15:
                        print("⚡ Kamu semakin dekat!")

            except ValueError:
                print("❌ Masukkan angka yang valid!")

        # Kalah
        print(f"\n😞 Kamu kehabisan kesempatan!")
        print(f"Angka yang benar adalah: {target}")

        self.stats['total_games'] += 1
        self.stats['losses'] += 1
        self.stats['level_stats'][level] += 1

        return False

    def show_stats(self):
        if self.stats['total_games'] == 0:
            print("\n📊 Belum ada statistik permainan")
            return

        win_rate = (self.stats['wins'] / self.stats['total_games']) * 100
        avg_guesses = self.stats['total_guesses'] / self.stats['wins'] if self.stats['wins'] > 0 else 0

        print("\n📊 STATISTIK PERMAINAN")
        print("=" * 30)
        print(f"Total Permainan: {self.stats['total_games']}")
        print(f"Menang: {self.stats['wins']}")
        print(f"Kalah: {self.stats['losses']}")
        print(f"Win Rate: {win_rate:.1f}%")
        print(f"Rata-rata Tebakan: {avg_guesses:.1f}")
        print(f"Score Tertinggi: {self.stats['best_score']}")

        print("\n📈 Statistik per Level:")
        for level, count in self.stats['level_stats'].items():
            if count > 0:
                print(f"  {level.title()}: {count} kali")

    def show_menu(self):
        while True:
            print("\n" + "="*40)
            print("🎮 GAME TEBAK ANGKA INTERAKTIF")
            print("="*40)
            print("1. 🎯 Main Game")
            print("2. 📊 Lihat Statistik")
            print("3. ⚙️  Pengaturan")
            print("4. 🚪 Keluar")
            print("="*40)

            try:
                choice = input("Pilih menu (1-4): ").strip()

                if choice == '1':
                    self.game_menu()
                elif choice == '2':
                    self.show_stats()
                elif choice == '3':
                    self.settings_menu()
                elif choice == '4':
                    print("\n👋 Terima kasih sudah bermain!")
                    self.save_stats()
                    break
                else:
                    print("❌ Pilihan tidak valid!")

            except KeyboardInterrupt:
                print("\n\n👋 Permainan dihentikan oleh pemain")
                self.save_stats()
                break

    def game_menu(self):
        while True:
            print("\n" + "-"*30)
            print("🎯 PILIH LEVEL KESULITAN")
            print("-"*30)
            print("1. 🟢 Mudah (1-50, unlimited tebakan)")
            print("2. 🟡 Sedang (1-100, max 10 tebakan)")
            print("3. 🔴 Sulit (1-200, max 7 tebakan)")
            print("4. ↩️  Kembali ke menu utama")
            print("-"*30)

            choice = input("Pilih level (1-4): ").strip()

            if choice == '1':
                self.play_game('mudah')
            elif choice == '2':
                self.play_game('sedang')
            elif choice == '3':
                self.play_game('sulit')
            elif choice == '4':
                break
            else:
                print("❌ Pilihan tidak valid!")

    def settings_menu(self):
        print("\n⚙️  PENGATURAN")
        print("Fitur pengaturan akan ditambahkan nanti...")
        print("Misalnya: Reset statistik, Ubah tema, dll.")

# Jalankan game
if __name__ == "__main__":
    game = GameTebakAngka()
    game.show_menu()
```

## File Data: `game_stats.json`

```json
{
  "total_games": 0,
  "wins": 0,
  "losses": 0,
  "total_guesses": 0,
  "best_score": 0,
  "level_stats": {
    "mudah": 0,
    "sedang": 0,
    "sulit": 0
  }
}
```

## Fitur Tambahan yang Bisa Dikembangkan

### 1. Sistem Achievement
```python
ACHIEVEMENTS = {
    "first_win": {"name": "First Victory", "desc": "Menangkan game pertama"},
    "speed_demon": {"name": "Speed Demon", "desc": "Menangkan dalam 3 tebakan"},
    "perfectionist": {"name": "Perfectionist", "desc": "Tebak benar di tebakan pertama"},
    "persistent": {"name": "Persistent", "desc": "Main 10 game"},
    "high_scorer": {"name": "High Scorer", "desc": "Dapat score 400+"},
}
```

### 2. Mode Multiplayer
- Player vs Player
- Leaderboard online
- Tournament mode

### 3. Tema dan Customization
- Dark/Light theme
- Custom range angka
- Sound effects
- Animasi

## Testing dan Debugging

### Test Cases
1. **Input Validation**: Test dengan input string, angka negatif, dll
2. **Edge Cases**: Test dengan angka tepi (1, 50, 100, 200)
3. **Statistics**: Pastikan statistik tersimpan dengan benar
4. **Error Handling**: Test ketika file stats corrupt atau tidak ada

### Debug Tips
```python
# Tambahkan logging untuk debug
import logging
logging.basicConfig(level=logging.DEBUG)

# Untuk melihat angka target (hanya saat development)
print(f"[DEBUG] Target number: {target}")
```

## Deployment dan Distribusi

### Membuat Executable
```bash
# Install PyInstaller
pip install pyinstaller

# Buat executable
pyinstaller --onefile --name game-tebak-angka game_tebak_angka.py

# Hasil ada di folder dist/
```

### Packaging untuk Distribusi
```
game-tebak-angka/
├── game_tebak_angka.exe  # Windows
├── game_tebak_angka      # Linux/Mac
├── README.md
├── game_stats.json
└── assets/               # Untuk gambar, sound, dll
```

## Evaluasi Proyek

### Kriteria Penilaian
- ✅ **Fungsionalitas** (40%): Semua fitur bekerja dengan baik
- ✅ **User Experience** (25%): Interface mudah digunakan
- ✅ **Code Quality** (20%): Code readable dan well-structured
- ✅ **Error Handling** (10%): Menangani error dengan baik
- ✅ **Documentation** (5%): README dan komentar code lengkap

### Self-Assessment Checklist
- [ ] Game bisa dimainkan dari awal sampai akhir
- [ ] Semua level kesulitan bekerja
- [ ] Statistik tersimpan dengan benar
- [ ] Input validation lengkap
- [ ] Code mudah dibaca dan dimengerti
- [ ] Error handling proper
- [ ] UI/UX user-friendly

## Kesimpulan

Proyek Game Tebak Angka ini mencakup:
- **Konsep Programming**: Variables, loops, conditions, functions
- **Data Structures**: Lists, dictionaries, file I/O
- **User Experience**: Interactive menu, feedback, scoring
- **Best Practices**: Error handling, code organization, documentation

Proyek ini bisa dijadikan template untuk proyek programming lainnya dan membantu siswa memahami konsep programming melalui game yang menyenangkan!