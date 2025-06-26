import json
import os
from rich.console import Console
from rich.table import Table

# Inisialisasi Console dari rich untuk output yang lebih baik
console = Console()

# Nama file untuk menyimpan data
NAMA_FILE = "tasks_data.json"

# Struktur data utama
data = {
    "tasks": [],
    "next_id": 1
}

def muat_data():
    """Memuat tugas dan next_id dari file JSON saat aplikasi dimulai."""
    global data
    if os.path.exists(NAMA_FILE):
        try:
            with open(NAMA_FILE, 'r') as f:
                data = json.load(f)
        except (json.JSONDecodeError, KeyError):
            console.print("[bold red]File data rusak! Membuat file baru.[/bold red]")
            # Jika file rusak, mulai dengan data default
            data = {"tasks": [], "next_id": 1}
    else:
        console.print("[yellow]File data tidak ditemukan. Akan dibuat file baru saat menyimpan tugas.[/yellow]")

def simpan_data():
    """Menyimpan state aplikasi (tugas dan next_id) ke file JSON."""
    with open(NAMA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def tampilkan_tugas(list_tugas=None, judul_tabel="Daftar Tugas Anda"):
    """
    Menampilkan tugas dalam format tabel yang rapi menggunakan rich.
    Menerima list tugas opsional untuk fitur filter dan urut.
    """
    tasks_to_show = list_tugas if list_tugas is not None else data['tasks']
    
    console.print(f"\n--- [bold cyan]{judul_tabel}[/bold cyan] ---")
    
    if not tasks_to_show:
        console.print("[yellow]Tidak ada tugas untuk ditampilkan.[/yellow]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=5)
    table.add_column("Judul Tugas", min_width=20)
    table.add_column("Deskripsi", min_width=20)
    table.add_column("Status", min_width=15)
    table.add_column("Estimasi (menit)", justify="right")

    for task in tasks_to_show:
        status_style = "green" if task['status'] == 'Selesai' else "yellow"
        table.add_row(
            str(task['id']),
            task['title'],
            task['description'],
            f"[{status_style}]{task['status']}[/{status_style}]",
            str(task['estimasi_waktu_pengerjaan']).replace(" menit", "")
        )
    
    console.print(table)

def tambah_tugas():
    """Menambahkan tugas baru dengan validasi input."""
    console.print("\n--- [bold green]Tambah Tugas Baru[/bold green] ---")
    
    # Validasi judul tidak boleh kosong
    while True:
        title = input("Masukkan judul tugas: ").strip()
        if title:
            break
        console.print("[red]Judul tidak boleh kosong. Silakan coba lagi.[/red]")

    description = input("Masukkan deskripsi tugas: ").strip()
    
    # Validasi estimasi harus berupa angka
    while True:
        try:
            estimasi = int(input("Masukkan estimasi waktu pengerjaan (dalam menit): "))
            break
        except ValueError:
            console.print("[red]Input tidak valid. Harap masukkan angka untuk estimasi waktu.[/red]")

    new_task = {
        "id": data['next_id'],
        "title": title,
        "description": description,
        "status": "Belum Selesai",
        "estimasi_waktu_pengerjaan": f"{estimasi} menit"
    }
    data['tasks'].append(new_task)
    data['next_id'] += 1
    simpan_data()
    console.print(f"\n[bold green]✓ Tugas '[white]{title}[/white]' berhasil ditambahkan![/bold green]")

def edit_tugas():
    """Mengedit judul, deskripsi, atau estimasi tugas yang ada."""
    tampilkan_tugas()
    if not data['tasks']:
        return

    try:
        id_to_edit = int(input("Masukkan ID tugas yang ingin diedit: "))
        task_to_edit = None
        for task in data['tasks']:
            if task['id'] == id_to_edit:
                task_to_edit = task
                break
        
        if task_to_edit:
            console.print(f"\nMengedit tugas: [bold yellow]'{task_to_edit['title']}'[/bold yellow]")
            console.print("(Tekan Enter untuk melewati, tanpa mengubah nilai)")

            new_title = input(f"Judul baru ({task_to_edit['title']}): ").strip()
            if new_title:
                task_to_edit['title'] = new_title

            new_desc = input(f"Deskripsi baru ({task_to_edit['description']}): ").strip()
            if new_desc:
                task_to_edit['description'] = new_desc

            while True:
                try:
                    new_estimasi_str = input(f"Estimasi baru ({task_to_edit['estimasi_waktu_pengerjaan']}): ").strip()
                    if new_estimasi_str:
                        new_estimasi = int(new_estimasi_str)
                        task_to_edit['estimasi_waktu_pengerjaan'] = f"{new_estimasi} menit"
                    break
                except ValueError:
                    console.print("[red]Input tidak valid. Harap masukkan angka.[/red]")
            
            simpan_data()
            console.print(f"\n[bold green]✓ Tugas dengan ID {id_to_edit} berhasil diperbarui.[/bold green]")
        else:
            console.print(f"[bold red]Tugas dengan ID {id_to_edit} tidak ditemukan.[/bold red]")
    except ValueError:
        console.print("[bold red]Input tidak valid. Harap masukkan ID berupa angka.[/bold red]")


def tandai_selesai():
    """Menandai sebuah tugas sebagai 'Selesai' berdasarkan ID."""
    tampilkan_tugas(list_tugas=[t for t in data['tasks'] if t['status'] == 'Belum Selesai'], judul_tabel="Tugas yang Belum Selesai")
    if not any(t['status'] == 'Belum Selesai' for t in data['tasks']):
        return
        
    try:
        id_to_mark = int(input("Masukkan ID tugas yang ingin ditandai selesai: "))
        task_found = False
        for task in data['tasks']:
            if task['id'] == id_to_mark:
                if task['status'] == 'Selesai':
                    console.print(f"[yellow]Tugas '{task['title']}' sudah selesai.[/yellow]")
                else:
                    task['status'] = "Selesai"
                    simpan_data()
                    console.print(f"\n[bold green]✓ Tugas '[white]{task['title']}[/white]' telah ditandai selesai.[/bold green]")
                task_found = True
                break
        
        if not task_found:
            console.print(f"[bold red]Tugas dengan ID {id_to_mark} tidak ditemukan.[/bold red]")
    except ValueError:
        console.print("[bold red]Input tidak valid. Harap masukkan ID berupa angka.[/bold red]")

def hapus_tugas():
    """Menghapus sebuah tugas dari list berdasarkan ID."""
    tampilkan_tugas()
    if not data['tasks']:
        return

    try:
        id_to_delete = int(input("Masukkan ID tugas yang ingin dihapus: "))
        task_to_remove = None
        for task in data['tasks']:
            if task['id'] == id_to_delete:
                task_to_remove = task
                break
        
        if task_to_remove:
            data['tasks'].remove(task_to_remove)
            simpan_data()
            console.print(f"\n[bold green]✓ Tugas '[white]{task_to_remove['title']}[/white]' telah dihapus.[/bold green]")
        else:
            console.print(f"[bold red]Tugas dengan ID {id_to_delete} tidak ditemukan.[/bold red]")
    except ValueError:
        console.print("[bold red]Input tidak valid. Harap masukkan ID berupa angka.[/bold red]")

def urutkan_tugas():
    """Menampilkan tugas yang sudah diurutkan berdasarkan pilihan pengguna."""
    if not data['tasks']:
        console.print("\n[yellow]Tidak ada tugas untuk diurutkan.[/yellow]")
        return
        
    console.print("\nUrutkan tugas berdasarkan:")
    console.print("1. ID")
    console.print("2. Judul")
    console.print("3. Status")
    pilihan = input("Pilihan Anda (1-3): ")

    sorted_tasks = []
    judul = "Daftar Tugas (Terurut)"
    if pilihan == '1':
        sorted_tasks = sorted(data['tasks'], key=lambda x: x['id'])
        judul = "Tugas Terurut berdasarkan ID"
    elif pilihan == '2':
        sorted_tasks = sorted(data['tasks'], key=lambda x: x['title'].lower())
        judul = "Tugas Terurut berdasarkan Judul"
    elif pilihan == '3':
        sorted_tasks = sorted(data['tasks'], key=lambda x: x['status'])
        judul = "Tugas Terurut berdasarkan Status"
    else:
        console.print("[red]Pilihan tidak valid.[/red]")
        return
        
    tampilkan_tugas(list_tugas=sorted_tasks, judul_tabel=judul)

def filter_tugas():
    """Menampilkan tugas yang sudah difilter berdasarkan status."""
    if not data['tasks']:
        console.print("\n[yellow]Tidak ada tugas untuk difilter.[/yellow]")
        return

    console.print("\nTampilkan tugas dengan status:")
    console.print("1. Selesai")
    console.print("2. Belum Selesai")
    pilihan = input("Pilihan Anda (1-2): ")

    filtered_tasks = []
    judul = "Hasil Filter"
    if pilihan == '1':
        filtered_tasks = [t for t in data['tasks'] if t['status'] == 'Selesai']
        judul = "Tugas yang Sudah Selesai"
    elif pilihan == '2':
        filtered_tasks = [t for t in data['tasks'] if t['status'] == 'Belum Selesai']
        judul = "Tugas yang Belum Selesai"
    else:
        console.print("[red]Pilihan tidak valid.[/red]")
        return

    tampilkan_tugas(list_tugas=filtered_tasks, judul_tabel=judul)

def menu():
    """Fungsi utama untuk menampilkan menu dan mengatur alur aplikasi."""
    muat_data() # Muat data saat aplikasi pertama kali dijalankan
    
    console.print("\n==============================================", style="bold blue")
    console.print("   Selamat Datang di Aplikasi To-Do List v2.0", style="bold blue")
    console.print("==============================================", style="bold blue")
    
    while True:
        console.print("\n--- [bold]Menu Utama[/bold] ---")
        menu_options = {
            "1": "Lihat Semua Tugas",
            "2": "Tambah Tugas",
            "3": "Edit Tugas",
            "4": "Tandai Tugas Selesai",
            "5": "Hapus Tugas",
            "6": "Urutkan Tugas",
            "7": "Filter Tugas",
            "8": "Keluar"
        }
        for key, value in menu_options.items():
            console.print(f"[cyan]{key}[/cyan]. {value}")

        pilihan = input("Masukkan pilihan Anda (1-8): ")

        if pilihan == '1':
            tampilkan_tugas()
        elif pilihan == '2':
            tambah_tugas()
        elif pilihan == '3':
            edit_tugas()
        elif pilihan == '4':
            tandai_selesai()
        elif pilihan == '5':
            hapus_tugas()
        elif pilihan == '6':
            urutkan_tugas()
        elif pilihan == '7':
            filter_tugas()
        elif pilihan == '8':
            console.print("\n[bold magenta]Terima kasih telah menggunakan aplikasi ini! Sampai jumpa![/bold magenta]")
            break
        else:
            console.print("\n[bold red]Pilihan tidak valid. Silakan coba lagi.[/bold red]")

if __name__ == "__main__":
    menu()
