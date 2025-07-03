# Aplikasi To-Do List CLI v2.2

Selamat datang di Aplikasi To-Do List berbasis Command-Line (CLI)\! Ini adalah sebuah proyek sederhana yang dibuat dengan Python, dirancang untuk membantu Anda mengelola tugas harian langsung dari terminal. Aplikasi ini sangat cocok bagi developer pemula yang ingin memahami konsep dasar Python seperti manipulasi data, input/output, penggunaan modul eksternal, dan persistensi data.

\<p align="center"\>
\<img src="[https://i.imgur.com/vHq9rZK.png](https://www.google.com/search?q=https://i.imgur.com/vHq9rZK.png)" alt="Screenshot Aplikasi To-Do List v2.2" width="800"/\>
\</p\>

-----

### navigasi

  * [✨ Fitur Utama](https://www.google.com/search?q=%23-fitur-utama)
  * [📋 Prasyarat](https://www.google.com/search?q=%23-prasyarat)
  * [🚀 Instalasi](https://www.google.com/search?q=%23-instalasi)
  * [🛠️ Cara Penggunaan](https://www.google.com/search?q=%23%EF%B8%8F-cara-penggunaan)
  * [🏗️ Struktur Kode](https://www.google.com/search?q=%23%EF%B8%8F-struktur-kode)
  * [🤔 Troubleshooting](https://www.google.com/search?q=%23-troubleshooting)
  * [🗺️ Roadmap Pengembangan](https://www.google.com/search?q=%23%EF%B8%8F-roadmap-pengembangan)
  * [📜 Lisensi](https://www.google.com/search?q=%23-lisensi)

-----

## ✨ Fitur Utama

Aplikasi ini dilengkapi dengan berbagai fitur untuk meningkatkan produktivitas Anda:

  * ✅ **Manajemen Tugas Lengkap**: Tambah, Edit, Hapus, dan Tandai tugas sebagai selesai.
  * приоритет **Prioritas Tugas**: Tetapkan prioritas (Tinggi, Sedang, Rendah) untuk setiap tugas dengan pewarnaan yang jelas.
  * ⏰ **Tanggal Jatuh Tempo**: Tambahkan *deadline* untuk setiap tugas, dengan visualisasi status (Terlambat, Mendekati).
  * 💅 **Tampilan Modern**: Antarmuka tabel yang rapi dan berwarna berkat library `rich`.
  * 💾 **Penyimpanan Permanen**: Tugas Anda akan otomatis disimpan dalam file `tasks_data.json`, jadi tidak akan hilang saat aplikasi ditutup.
  * 🔍 **Urutkan & Filter**: Lihat tugas berdasarkan ID, Judul, Status, Prioritas, atau tanggal Jatuh Tempo.
  * 🔒 **Validasi Input**: Mencegah input yang tidak valid (misalnya, judul kosong atau format tanggal salah).
  * 💻 **Lintas Platform**: Berjalan di Windows, macOS, dan Linux.

-----

## 📋 Prasyarat

Sebelum memulai, pastikan sistem Anda telah terinstal:

  * **Python**: Versi 3.8 atau yang lebih baru. Anda bisa mengunduhnya dari [python.org](https://www.python.org/downloads/).
  * **pip**: Package installer untuk Python (biasanya sudah terinstal bersama Python).

-----

## 🚀 Instalasi

Ikuti langkah-langkah berikut untuk menjalankan aplikasi di komputer Anda:

1.  **Clone Repositori**
    Buka terminal Anda dan clone repositori ini (atau cukup unduh dan ekstrak file `.py`).

    ```bash
    git clone https://github.com/nama-anda/todo-list-cli.git
    cd todo-list-cli
    ```

2.  **(Opsional, Sangat Direkomendasikan) Buat Virtual Environment**
    Ini akan mengisolasi dependensi proyek Anda dari instalasi Python global.

      * **Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
      * **macOS / Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install Dependensi**
    Aplikasi ini memerlukan library `rich` dan `python-dateutil`. Buat file bernama `requirements.txt` dan isi dengan:

    ```
    rich
    python-dateutil
    ```

    Kemudian, install dependensi menggunakan pip:

    ```bash
    pip install -r requirements.txt
    ```

-----

## 🛠️ Cara Penggunaan

Setelah instalasi selesai, jalankan aplikasi dengan perintah:

```bash
python todo_app.py
```

Anda akan disambut dengan menu utama. Cukup masukkan nomor pilihan Anda dan ikuti instruksi di layar.

#### Contoh Sesi Penggunaan

**1. Menambah Tugas Baru**
Pilih opsi `2`, lalu masukkan semua detail tugas yang diminta, termasuk prioritas dan tanggal jatuh tempo.

```bash
> Masukkan pilihan Anda (1-8): 2

--- Tambah Tugas Baru ---
Masukkan judul tugas: Siapkan Presentasi Proyek
Masukkan deskripsi tugas: Buat slide untuk demo aplikasi
Pilih Prioritas:
1. Rendah
2. Sedang
3. Tinggi
Pilihan Anda (1-3): 3
Masukkan Tanggal Jatuh Tempo:
Format: YYYY-MM-DD HH:MM (waktu opsional). Contoh: 2024-12-31 atau 2024-12-31 17:00
> 2025-07-04 15:00

✓ Tugas 'Siapkan Presentasi Proyek' berhasil ditambahkan!
```

**2. Melihat Semua Tugas**
Pilih opsi `1` untuk melihat daftar tugas dalam format tabel yang telah diperbarui. Perhatikan kolom **Prioritas** dan **Jatuh Tempo** dengan pewarnaannya.

```bash
> Masukkan pilihan Anda (1-8): 1
 
--- Daftar Tugas Anda ---
┏━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ ID  ┃ Judul Tugas                  ┃ Prioritas ┃ Jatuh Tempo          ┃ Status          ┃
┡━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ 1   │ Siapkan Presentasi Proyek    │ Tinggi    │ 2025-07-04 15:00     │ Belum Selesai   │
│ 2   │ Perbaiki bug di halaman login│ Sedang    │ 2025-07-02 10:00     │ Selesai         │
│ 3   │ Belajar unit testing         │ Rendah    │ N/A                  │ Belum Selesai   │
└─────┴──────────────────────────────┴───────────┴──────────────────────┴─────────────────┘
```

*(Contoh di atas mengasumsikan tanggal saat ini adalah 3 Juli 2025. Tugas yang terlambat akan berwarna merah).*

-----

## 🏗️ Struktur Kode

Kode diorganisir secara modular menggunakan fungsi-fungsi dengan tanggung jawab yang jelas.

| Fungsi | Deskripsi |
| :--- | :--- |
| `menu()` | Titik masuk utama aplikasi, menampilkan menu, dan mengelola alur program. |
| `muat_data()` & `simpan_data()`| Menangani persistensi data (baca/tulis) ke file `tasks_data.json` dan memastikan kompatibilitas data lama. |
| `tampilkan_tugas()`| Merender tabel `rich`, kini dengan logika pewarnaan untuk Prioritas dan status Jatuh Tempo. |
| `pilih_prioritas()`| Fungsi bantuan untuk menampilkan menu pilihan prioritas dan memvalidasi input. |
| `get_due_date_input()`| Fungsi bantuan untuk mendapatkan input tanggal jatuh tempo yang fleksibel dari pengguna. |
| `tambah_tugas()`| Mengelola logika penambahan tugas baru, termasuk Prioritas dan Jatuh Tempo. |
| `edit_tugas()` | Mengelola logika pembaruan tugas, termasuk Prioritas dan Jatuh Tempo. |
| `urutkan_tugas()`| Menampilkan tugas yang diurutkan, sekarang dengan opsi pengurutan berdasarkan Prioritas dan Jatuh Tempo. |

-----

## 🤔 Troubleshooting

Berikut adalah beberapa masalah umum yang mungkin Anda temui:

  * **Masalah:** Muncul error `ModuleNotFoundError: No module named 'rich'` atau `No module named 'dateutil'`.

      * **Solusi:** Anda belum menginstal dependensi yang diperlukan. Pastikan Anda sudah menjalankan `pip install -r requirements.txt` di dalam virtual environment Anda.

  * **Masalah:** Muncul pesan `File data rusak! Membuat file baru.`

      * **Solusi:** Ini berarti file `tasks_data.json` Anda tidak sengaja terhapus sebagian atau formatnya salah. Aplikasi ini sudah menanganinya dengan membuat file baru. Jika Anda ingin memulai dari awal, Anda bisa menghapus file `tasks_data.json` secara manual.

  * **Masalah:** Perintah `python` atau `pip` tidak ditemukan di terminal.

      * **Solusi:** Kemungkinan besar instalasi Python Anda belum ditambahkan ke `PATH` sistem. Coba install ulang Python dan pastikan Anda mencentang opsi "Add Python to PATH" saat proses instalasi.

-----

## 🗺️ Roadmap Pengembangan

Proyek ini masih bisa dikembangkan lebih lanjut\! Berikut adalah beberapa ide untuk masa depan:

  - [x] **Prioritas Tugas**: Menambahkan level prioritas (misal: Rendah, Sedang, Tinggi) pada setiap tugas.
  - [x] **Tanggal Jatuh Tempo**: Menambahkan fungsionalitas tanggal dan waktu jatuh tempo.
  - [ ] **Sub-Tugas**: Kemampuan untuk menambahkan "sub-tugas" atau *checklist* di dalam sebuah tugas utama.
  - [ ] **Unit Tests**: Menulis pengujian otomatis menggunakan `pytest` untuk memastikan setiap fungsi bekerja dengan benar.
  - [ ] **Database**: Migrasi dari file JSON ke database yang lebih kuat seperti SQLite untuk skalabilitas yang lebih baik.
  - [ ] **Antarmuka Web**: Membuat versi web dari aplikasi ini menggunakan framework seperti Flask atau FastAPI.
  - [ ] **Paket Instalasi**: Mengemas aplikasi menjadi paket Python yang dapat diinstal melalui `pip`.

Merasa tertantang? Kontribusi sangat diterima\!

-----

## 📜 Lisensi

Proyek ini dilisensikan di bawah **MIT License**.

-----

Dibuat dengan ❤️ menggunakan Python.
