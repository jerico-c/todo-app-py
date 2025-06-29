# Aplikasi To-Do List CLI

Selamat datang di Aplikasi To-Do List berbasis Command-Line (CLI)\! Ini adalah sebuah proyek sederhana yang dibuat dengan Python, dirancang untuk membantu Anda mengelola tugas harian langsung dari terminal. Aplikasi ini sangat cocok bagi developer pemula yang ingin memahami konsep dasar Python seperti manipulasi data, input/output, penggunaan modul eksternal, dan persistensi data.

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
  * 💅 **Tampilan Modern**: Antarmuka tabel yang rapi dan berwarna berkat library `rich`.
  * 💾 **Penyimpanan Permanen**: Tugas Anda akan otomatis disimpan dalam file `tasks_data.json`, jadi tidak akan hilang saat aplikasi ditutup.
  * 🔍 **Urutkan & Filter**: Lihat tugas berdasarkan urutan ID, Judul, Status, atau filter hanya yang sudah/belum selesai.
  * 🔒 **Validasi Input**: Mencegah input yang tidak valid (misalnya, judul kosong atau estimasi non-numerik).
  * 💻 **Lintas Platform**: Berjalan di Windows, macOS, dan Linux.

## 📋 Prasyarat

Sebelum memulai, pastikan sistem Anda telah terinstal:

  * **Python**: Versi 3.8 atau yang lebih baru. Anda bisa mengunduhnya dari [python.org](https://www.python.org/downloads/).
  * **pip**: Package installer untuk Python (biasanya sudah terinstal bersama Python).

## 🚀 Instalasi

Ikuti langkah-langkah berikut untuk menjalankan aplikasi di komputer Anda:

1.  **Clone Repositori**
    Buka terminal Anda dan clone repositori ini (atau cukup unduh dan ekstrak file `todo_app.py`).

    ```bash
    git clone https://github.com/jerico-c/todo-app-py.git
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
    Aplikasi ini memerlukan library `rich`. Buat file bernama `requirements.txt` dan isi dengan:

    ```
    rich
    ```

    Kemudian, install dependensi menggunakan pip:

    ```bash
    pip install -r requirements.txt
    ```

## 🛠️ Cara Penggunaan

Setelah instalasi selesai, jalankan aplikasi dengan perintah:

```bash
python todo_app.py
```

Anda akan disambut dengan menu utama. Cukup masukkan nomor pilihan Anda dan ikuti instruksi di layar.

#### Contoh Sesi Penggunaan

**1. Menambah Tugas Baru**
Pilih opsi `2`, lalu masukkan detail tugas.

```bash
> Masukkan pilihan Anda (1-8): 2

--- Tambah Tugas Baru ---
Masukkan judul tugas: Belajar Membuat README
Masukkan deskripsi tugas: Latihan membuat dokumentasi proyek di GitHub
Masukkan estimasi waktu pengerjaan (dalam menit): 60

✓ Tugas 'Belajar Membuat README' berhasil ditambahkan!
```

**2. Melihat Semua Tugas**
Pilih opsi `1` untuk melihat daftar tugas dalam format tabel yang rapi.

```bash
> Masukkan pilihan Anda (1-8): 1
 
--- Daftar Tugas Anda ---
┏━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ ID  ┃ Judul Tugas              ┃ Deskripsi                            ┃ Status          ┃ Estimasi (menit) ┃
┡━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ 1   │ Belajar Membuat README   │ Latihan membuat dokumentasi proyek … │ Belum Selesai   │               60 │
│ 2   │ Refactor Kode Python     │ Membersihkan dan merapikan kode      │ Belum Selesai   │              120 │
└─────┴──────────────────────────┴──────────────────────────────────────┴─────────────────┴──────────────────┘
```

**3. Menandai Tugas Selesai**
Pilih opsi `4`, lalu masukkan ID tugas yang ingin ditandai.

```bash
> Masukkan pilihan Anda (1-8): 4

Masukkan ID tugas yang ingin ditandai selesai: 1

✓ Tugas 'Belajar Membuat README' telah ditandai selesai.
```

Tampilan status akan berubah menjadi hijau.

## 🏗️ Struktur Kode

Meskipun saat ini hanya terdiri dari satu file (`todo_app.py`), kode ini diorganisir secara modular menggunakan fungsi-fungsi dengan tanggung jawab yang jelas.

| Fungsi | Deskripsi |
| :--- | :--- |
| `menu()` | Fungsi utama yang menjadi titik masuk aplikasi, menampilkan menu, dan mengelola alur program. |
| `muat_data()` | Memuat data tugas dari file `tasks_data.json` saat aplikasi dimulai. |
| `simpan_data()`| Menyimpan semua perubahan ke `tasks_data.json` secara otomatis. |
| `tampilkan_tugas()`| Bertanggung jawab untuk merender dan menampilkan data tugas dalam format tabel `rich`.|
| `tambah_tugas()`| Mengelola logika untuk menambahkan tugas baru, termasuk validasi input. |
| `edit_tugas()` | Mengelola logika untuk memperbarui detail tugas yang ada. |
| `tandai_selesai()`| Mengubah status tugas menjadi "Selesai". |
| `hapus_tugas()`| Menghapus tugas dari daftar. |
| `urutkan_tugas()`| Menampilkan tugas dalam urutan yang dipilih (ID, Judul, Status). |
| `filter_tugas()`| Menampilkan tugas berdasarkan status (Selesai / Belum Selesai). |

## 🤔 Troubleshooting

Berikut adalah beberapa masalah umum yang mungkin Anda temui:

  * **Masalah:** Muncul error `ModuleNotFoundError: No module named 'rich'`.

      * **Solusi:** Anda belum menginstal dependensi yang diperlukan. Pastikan Anda sudah menjalankan `pip install -r requirements.txt` di dalam virtual environment Anda.

  * **Masalah:** Muncul pesan `File data rusak! Membuat file baru.`

      * **Solusi:** Ini berarti file `tasks_data.json` Anda tidak sengaja terhapus sebagian atau formatnya salah. Aplikasi ini sudah menanganinya dengan membuat file baru. Jika Anda ingin memulai dari awal, Anda bisa menghapus file `tasks_data.json` secara manual.

  * **Masalah:** Perintah `python` atau `pip` tidak ditemukan di terminal.

      * **Solusi:** Kemungkinan besar instalasi Python Anda belum ditambahkan ke `PATH` sistem. Coba install ulang Python dan pastikan Anda mencentang opsi "Add Python to PATH" saat proses instalasi.

## 🗺️ Roadmap Pengembangan

Proyek ini masih bisa dikembangkan lebih lanjut\! Berikut adalah beberapa ide untuk masa depan:

  - [ ] **Prioritas Tugas**: Menambahkan level prioritas (misal: Rendah, Sedang, Tinggi) pada setiap tugas.
  - [ ] **Tanggal Jatuh Tempo**: Menambahkan fungsionalitas tanggal dan waktu jatuh tempo.
  - [ ] **Unit Tests**: Menulis pengujian otomatis menggunakan `pytest` untuk memastikan setiap fungsi bekerja dengan benar.
  - [ ] **Database**: Migrasi dari file JSON ke database yang lebih kuat seperti SQLite untuk skalabilitas yang lebih baik.
  - [ ] **Antarmuka Web**: Membuat versi web dari aplikasi ini menggunakan framework seperti Flask atau FastAPI.
  - [ ] **Paket Instalasi**: Mengemas aplikasi menjadi paket Python yang dapat diinstal melalui `pip`.

Merasa tertantang? Kontribusi sangat diterima\!

## 📜 Lisensi

Proyek ini dilisensikan di bawah **MIT License**. Lihat file `LICENSE` untuk detail lebih lanjut.

-----

