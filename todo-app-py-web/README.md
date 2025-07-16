Tentu, ini adalah `README.md` yang telah diperbarui secara total untuk mencerminkan transformasi aplikasi Anda dari CLI menjadi **Aplikasi Web** berbasis **Flask**.

-----

# Aplikasi To-Do List Web v2.5 (Flask)

Selamat datang di Aplikasi To-Do List Web\! Proyek ini merupakan evolusi dari aplikasi konsol (CLI) menjadi sebuah aplikasi web *full-stack* yang interaktif. Dibangun menggunakan framework **Flask** dan didukung oleh database **SQLite**, aplikasi ini memungkinkan Anda mengelola tugas harian melalui antarmuka browser yang bersih dan responsif.

Proyek ini adalah studi kasus yang sangat baik untuk developer yang ingin bertransisi dari skrip sederhana ke pengembangan aplikasi web terstruktur dengan Python.

### Tampilan Aplikasi

\<p align="center"\>
\<strong\>Halaman Utama\</strong\>\<br\>
\<img src="https://www.google.com/search?q=https://i.imgur.com/K3Gq223.png" alt="Screenshot Halaman Utama Aplikasi To-Do List Web" width="800"/\>
\</p\>
\<p align="center"\>
\<strong\>Halaman Detail & Edit Tugas\</strong\>\<br\>
\<img src="https://www.google.com/search?q=https://i.imgur.com/tYtHkXg.png" alt="Screenshot Halaman Detail Tugas" width="800"/\>
\</p\>

-----

### navigasi

  * [✨ Fitur Utama](https://www.google.com/search?q=%23-fitur-utama)
  * [📋 Prasyarat](https://www.google.com/search?q=%23-prasyarat)
  * [🚀 Instalasi & Penggunaan](https://www.google.com/search?q=%23-instalasi--penggunaan)
  * [🏗️ Struktur Proyek](https://www.google.com/search?q=%23%EF%B8%8F-struktur-proyek)
  * [🤔 Troubleshooting](https://www.google.com/search?q=%23-troubleshooting)
  * [🗺️ Roadmap Pengembangan](https://www.google.com/search?q=%23%EF%B8%8F-roadmap-pengembangan)
  * [📜 Lisensi](https://www.google.com/search?q=%23-lisensi)

-----

## ✨ Fitur Utama

  * 🌐 **Antarmuka Web Penuh**: Semua fungsionalitas kini dapat diakses melalui browser web yang intuitif.
  * ✅ **Manajemen Tugas & Sub-Tugas**: Tambah, edit, hapus, dan kelola *checklist* untuk setiap tugas.
  * ⏰ **Prioritas & Jatuh Tempo**: Tetapkan prioritas dan *deadline* dengan visualisasi status (misalnya, tugas terlambat berwarna merah).
  * 💾 **Backend SQLite**: Didukung oleh database SQLite yang andal dan cepat, menggantikan file JSON.
  * 🎨 **Tampilan Responsif**: Didesain menggunakan Bootstrap 5, aplikasi ini dapat diakses dengan baik di desktop maupun perangkat mobile.
  * ⚡ **Pemberitahuan Instan**: Gunakan sistem *flash message* untuk memberikan umpan balik langsung kepada pengguna setelah setiap aksi.

-----

## 📋 Prasyarat

Sebelum memulai, pastikan sistem Anda telah terinstal:

  * **Python**: Versi 3.8 atau yang lebih baru.
  * **pip**: Package installer untuk Python.

-----

## 🚀 Instalasi & Penggunaan

Ikuti langkah-langkah berikut untuk menjalankan aplikasi web di komputer Anda.

### 1\. Siapkan Struktur Proyek

Pastikan Anda memiliki struktur file dan folder seperti berikut:

```
/todo-list-web/
|-- app.py
|-- database.py
|-- schema.sql
|-- requirements.txt
|-- /templates/
|   |-- base.html
|   |-- index.html
|   `-- task_detail.html
`-- /static/
    `-- style.css
```

*(Salin semua kode dari respons sebelumnya ke dalam file yang sesuai).*

### 2\. Buat `requirements.txt`

File ini akan berisi semua dependensi Python yang dibutuhkan.

```
# file: requirements.txt
Flask
python-dateutil
```

### 3\. Install Dependensi

Buka terminal di dalam direktori proyek Anda dan jalankan perintah berikut (sangat disarankan untuk berada di dalam *virtual environment*).

```bash
pip install -r requirements.txt
```

### 4\. Jalankan Aplikasi

Setelah instalasi selesai, jalankan server Flask:

```bash
python app.py
```

Terminal Anda akan menampilkan output seperti ini:

```
 * Serving Flask app 'app'
 * Running on http://127.0.0.1:5001
Press CTRL+C to quit
```

### 5\. Buka di Browser

Buka browser web Anda (Chrome, Firefox, dll.) dan kunjungi alamat:
**[http://127.0.0.1:5001](https://www.google.com/url?sa=E&source=gmail&q=http://127.0.0.1:5001)**

Sekarang Anda dapat mulai menggunakan aplikasi To-Do List versi web\!

-----

## 🏗️ Struktur Proyek

Aplikasi ini kini dipisahkan menjadi beberapa file dan direktori, sesuai dengan praktik terbaik pengembangan web.

| File / Folder | Deskripsi |
| :--- | :--- |
| `app.py` | **Inti Aplikasi Flask**. Berisi semua *routes* (URL) dan logika untuk menangani permintaan pengguna. |
| `database.py`| **Lapisan Akses Data**. Berisi semua fungsi untuk berinteraksi dengan database SQLite. |
| `schema.sql` | **Definisi Skema Database**. Digunakan untuk membuat struktur tabel `tasks` dan `subtasks`. |
| `requirements.txt`| Daftar semua paket Python yang dibutuhkan oleh proyek. |
| `/templates/` | **Folder Template HTML**. Berisi semua file `.html` yang mendefinisikan tampilan halaman. |
| `/static/` | **Folder Aset Statis**. Berisi file CSS, JavaScript, dan gambar. |

-----

## 🤔 Troubleshooting

  * **Masalah:** Muncul error `ModuleNotFoundError: No module named 'flask'`.

      * **Solusi:** Anda belum menginstal dependensi. Jalankan `pip install -r requirements.txt`.

  * **Masalah:** Saat membuka browser, muncul "This site can’t be reached".

      * **Solusi:** Pastikan server Flask Anda masih berjalan di terminal. Jika tidak, jalankan kembali dengan `python app.py`.

  * **Masalah:** Muncul error `jinja2.exceptions.TemplateNotFound`.

      * **Solusi:** Flask tidak dapat menemukan file HTML Anda. Pastikan struktur direktori Anda benar, terutama folder `/templates` yang harus berada di level yang sama dengan `app.py`.

-----

## 🗺️ Roadmap Pengembangan

Proyek ini telah berkembang pesat, namun masih banyak ruang untuk perbaikan dan fitur baru\!

  - [x] \~\~Prioritas Tugas\~\~
  - [x] \~\~Tanggal Jatuh Tempo\~\~
  - [x] \~\~Sub-Tugas / Checklist\~\~
  - [x] \~\~Migrasi ke Database SQLite\~\~
  - [x] **Antarmuka Web (Flask)**
  - [ ] **Otentikasi Pengguna**: Sistem login dan registrasi agar setiap pengguna hanya bisa melihat tugasnya sendiri.
  - [ ] **Pembaruan Dinamis (AJAX)**: Menggunakan JavaScript untuk menandai tugas selesai atau menambah sub-tugas tanpa perlu me-refresh seluruh halaman.
  - [ ] **Containerisasi dengan Docker**: Membungkus aplikasi ke dalam Docker container untuk mempermudah proses *deployment*.
  - [ ] **Deployment**: Menerbitkan aplikasi ke platform cloud seperti PythonAnywhere, Heroku, atau Vercel agar bisa diakses secara online.

-----

## 📜 Lisensi

Proyek ini dilisensikan di bawah **MIT License**.
