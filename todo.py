# Inisialisasi list tugas di luar fungsi agar tidak ter-reset
tasks = []
# ID unik untuk setiap tugas, dimulai dari 1
next_id = 1

def lihat_tugas():
    """Menampilkan semua tugas yang ada."""
    print("\n--- Daftar Tugas Anda ---")
    if not tasks:
        print("Belum ada tugas. Silakan tambahkan tugas baru!")
    else:
        # Tampilan tabel sederhana untuk keterbacaan
        print(f"{'ID':<5} | {'Judul Tugas':<20} | {'Deskripsi':<30} | {'Status':<15} | {'Estimasi (menit)':<20}")
        print("-" * 100)
        for task in tasks:
            print(f"{task['id']:<5} | {task['title']:<20} | {task['description']:<30} | {task['status']:<15} | {task['estimasi_waktu_pengerjaan']:<20}")
    print("-" * 100)

def tambah_tugas():
    """Menambahkan tugas baru ke dalam list tugas."""
    global next_id
    print("\n--- Tambah Tugas Baru ---")
    title = input("Masukkan judul tugas: ")
    description = input("Masukkan deskripsi tugas: ")
    while True:
        try:
            estimasi = int(input("Masukkan estimasi waktu pengerjaan (dalam menit): "))
            break
        except ValueError:
            print("Input tidak valid. Harap masukkan angka untuk estimasi waktu.")

    new_task = {
        "id": next_id,
        "title": title,
        "description": description,
        "status": "Belum Selesai",
        "estimasi_waktu_pengerjaan": f"{estimasi} menit"
    }
    tasks.append(new_task)
    next_id += 1 # Inkrementasi ID untuk tugas berikutnya
    print(f"Tugas '{title}' berhasil ditambahkan!")

def tandai_selesai():
    """Menandai sebuah tugas sebagai 'Selesai' berdasarkan ID."""
    lihat_tugas() # Tampilkan tugas agar pengguna tahu ID mana yang harus dipilih
    if not tasks:
        return # Keluar dari fungsi jika tidak ada tugas

    try:
        id_to_mark = int(input("Masukkan ID tugas yang ingin ditandai selesai: "))
        task_found = False
        for task in tasks:
            if task['id'] == id_to_mark:
                task['status'] = "Selesai"
                task_found = True
                print(f"Tugas dengan ID {id_to_mark} ('{task['title']}') telah ditandai selesai.")
                break
        
        if not task_found:
            print(f"Tugas dengan ID {id_to_mark} tidak ditemukan.")
    except ValueError:
        print("Input tidak valid. Harap masukkan ID berupa angka.")

def hapus_tugas():
    """Menghapus sebuah tugas dari list berdasarkan ID."""
    lihat_tugas() # Tampilkan tugas agar pengguna tahu ID mana yang harus dipilih
    if not tasks:
        return # Keluar dari fungsi jika tidak ada tugas

    try:
        id_to_delete = int(input("Masukkan ID tugas yang ingin dihapus: "))
        task_to_remove = None
        for task in tasks:
            if task['id'] == id_to_delete:
                task_to_remove = task
                break
        
        if task_to_remove:
            tasks.remove(task_to_remove)
            print(f"Tugas dengan ID {id_to_delete} ('{task_to_remove['title']}') telah dihapus.")
        else:
            print(f"Tugas dengan ID {id_to_delete} tidak ditemukan.")
    except ValueError:
        print("Input tidak valid. Harap masukkan ID berupa angka.")

def menu():
    """Fungsi utama untuk menampilkan menu dan mengatur alur aplikasi."""
    print("\n========================================")
    print(" Selamat Datang di Aplikasi To-Do List")
    print("========================================")
    
    while True:
        print("\n--- Menu Utama ---")
        print("1. Lihat Semua Tugas")
        print("2. Tambah Tugas")
        print("3. Tandai Tugas Selesai")
        print("4. Hapus Tugas")
        print("5. Keluar")

        pilihan = input("Masukkan pilihan Anda (1-5): ")

        if pilihan == '1':
            lihat_tugas()
        elif pilihan == '2':
            tambah_tugas()
        elif pilihan == '3':
            tandai_selesai()
        elif pilihan == '4':
            hapus_tugas()
        elif pilihan == '5':
            print("\nTerima kasih telah menggunakan aplikasi ini!")
            break
        else:
            print("\nPilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    menu()
