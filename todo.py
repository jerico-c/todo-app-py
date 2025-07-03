import json
import os
from datetime import datetime
from dateutil import parser # <-- IMPORT BARU
from rich.console import Console
from rich.table import Table

# Inisialisasi Console dari rich
console = Console()
NAMA_FILE = "tasks_data.json"
data = {"tasks": [], "next_id": 1}

def muat_data():
    """Memuat data dan memastikan kompatibilitas dengan field baru."""
    global data
    if os.path.exists(NAMA_FILE):
        try:
            with open(NAMA_FILE, 'r') as f:
                loaded_data = json.load(f)
                # Kompatibilitas untuk data lama
                for task in loaded_data.get("tasks", []):
                    task.setdefault("priority", "Sedang")
                    task.setdefault("due_date", None) # <-- KOMPATIBILITAS BARU
                data = loaded_data
        except (json.JSONDecodeError, KeyError):
            console.print("[bold red]File data rusak! Membuat file baru.[/bold red]")
            data = {"tasks": [], "next_id": 1}
    else:
        console.print("[yellow]File data tidak ditemukan. Akan dibuat file baru saat menyimpan tugas.[/yellow]")

def simpan_data():
    """Menyimpan state aplikasi ke file JSON."""
    with open(NAMA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def tampilkan_tugas(list_tugas=None, judul_tabel="Daftar Tugas Anda"):
    """Menampilkan tugas dalam tabel, kini dengan kolom Jatuh Tempo."""
    tasks_to_show = list_tugas if list_tugas is not None else data['tasks']
    
    console.print(f"\n--- [bold cyan]{judul_tabel}[/bold cyan] ---")
    
    if not tasks_to_show:
        console.print("[yellow]Tidak ada tugas untuk ditampilkan.[/yellow]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=5)
    table.add_column("Judul Tugas", min_width=20)
    table.add_column("Prioritas", min_width=10)
    table.add_column("Jatuh Tempo", min_width=18) # <-- KOLOM BARU
    table.add_column("Status", min_width=15)
    
    priority_styles = {"Tinggi": "bold red", "Sedang": "yellow", "Rendah": "green"}
    now = datetime.now()

    for task in tasks_to_show:
        status_style = "green" if task['status'] == 'Selesai' else "yellow"
        priority = task.get("priority", "Sedang")
        p_style = priority_styles.get(priority, "white")
        
        # Logika pewarnaan untuk Jatuh Tempo
        due_date_str = task.get("due_date")
        due_date_display = "N/A"
        date_style = "dim"
        if due_date_str:
            due_date = parser.parse(due_date_str)
            due_date_display = due_date.strftime('%Y-%m-%d %H:%M')
            if task['status'] != 'Selesai':
                if due_date < now:
                    date_style = "bold red" # Terlambat
                elif (due_date - now).days < 1:
                    date_style = "bold yellow" # Mendekati (kurang dari 1 hari)
        
        table.add_row(
            str(task['id']),
            task['title'],
            f"[{p_style}]{priority}[/{p_style}]",
            f"[{date_style}]{due_date_display}[/{date_style}]", # <-- DATA BARU
            f"[{status_style}]{task['status']}[/{status_style}]"
        )
    
    console.print(table)

def get_due_date_input(due_date_saat_ini=None):
    """Fungsi bantuan untuk mendapatkan input tanggal dan waktu jatuh tempo."""
    display_current = ""
    if due_date_saat_ini:
        try:
            current_dt = parser.parse(due_date_saat_ini).strftime('%Y-%m-%d %H:%M')
            display_current = f" (saat ini: [bold]{current_dt}[/bold], kosongkan untuk hapus)"
        except (parser.ParserError, TypeError):
            display_current = " (saat ini: tidak valid)"
            
    console.print(f"Masukkan Tanggal Jatuh Tempo{display_current}:")
    console.print("Format: YYYY-MM-DD HH:MM (waktu opsional). Contoh: 2024-12-31 atau 2024-12-31 17:00")
    
    while True:
        user_input = input("> ").strip()
        if not user_input:
             # Jika input kosong saat edit, kembalikan nilai saat ini atau None jika ingin menghapus
            return due_date_saat_ini if due_date_saat_ini and not display_current.endswith("hapus)") else None
        try:
            # `parser.parse` akan secara cerdas mengurai berbagai format tanggal
            dt_object = parser.parse(user_input)
            return dt_object.isoformat() # Simpan dalam format ISO standar
        except parser.ParserError:
            console.print("[red]Format tanggal tidak valid. Silakan coba lagi.[/red]")

def tambah_tugas():
    """Menambahkan tugas baru, termasuk Jatuh Tempo."""
    console.print("\n--- [bold green]Tambah Tugas Baru[/bold green] ---")
    
    while True:
        title = input("Masukkan judul tugas: ").strip()
        if title: break
        console.print("[red]Judul tidak boleh kosong.[/red]")

    description = input("Masukkan deskripsi tugas: ").strip()
    priority = pilih_prioritas()
    due_date = get_due_date_input() # <-- LOGIKA BARU

    new_task = {
        "id": data['next_id'], "title": title, "description": description,
        "priority": priority, "status": "Belum Selesai", "due_date": due_date
    }
    data['tasks'].append(new_task)
    data['next_id'] += 1
    simpan_data()
    console.print(f"\n[bold green]✓ Tugas '[white]{title}[/white]' berhasil ditambahkan![/bold green]")

def edit_tugas():
    """Mengedit tugas yang ada, termasuk Jatuh Tempo."""
    tampilkan_tugas()
    if not data['tasks']: return

    try:
        id_to_edit = int(input("Masukkan ID tugas yang ingin diedit: "))
        task_to_edit = next((task for task in data['tasks'] if task['id'] == id_to_edit), None)
        
        if task_to_edit:
            console.print(f"\nMengedit tugas: [bold yellow]'{task_to_edit['title']}'[/bold yellow]")
            console.print("(Tekan Enter untuk melewati, tanpa mengubah nilai)")

            new_title = input(f"Judul baru ({task_to_edit['title']}): ").strip()
            if new_title: task_to_edit['title'] = new_title

            new_desc = input(f"Deskripsi baru ({task_to_edit['description']}): ").strip()
            if new_desc: task_to_edit['description'] = new_desc

            task_to_edit['priority'] = pilih_prioritas(task_to_edit.get("priority", "Sedang"))
            
            # Memperbarui jatuh tempo
            task_to_edit['due_date'] = get_due_date_input(task_to_edit.get("due_date")) # <-- LOGIKA BARU
            
            simpan_data()
            console.print(f"\n[bold green]✓ Tugas dengan ID {id_to_edit} berhasil diperbarui.[/bold green]")
        else:
            console.print(f"[bold red]Tugas dengan ID {id_to_edit} tidak ditemukan.[/bold red]")
    except ValueError:
        console.print("[bold red]Input tidak valid. Harap masukkan ID berupa angka.[/bold red]")

def urutkan_tugas():
    """Menampilkan tugas yang sudah diurutkan, kini dengan opsi Jatuh Tempo."""
    if not data['tasks']:
        console.print("\n[yellow]Tidak ada tugas untuk diurutkan.[/yellow]")
        return
        
    console.print("\nUrutkan tugas berdasarkan:")
    console.print("1. ID")
    console.print("2. Judul")
    console.print("3. Status")
    console.print("4. Prioritas (Tinggi ke Rendah)")
    console.print("5. Jatuh Tempo (Terdekat)") # <-- OPSI BARU
    pilihan = input("Pilihan Anda (1-5): ")

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
    elif pilihan == '4':
        priority_map = {"Tinggi": 3, "Sedang": 2, "Rendah": 1}
        sorted_tasks = sorted(data['tasks'], key=lambda x: priority_map.get(x.get('priority', 'Sedang'), 0), reverse=True)
        judul = "Tugas Terurut berdasarkan Prioritas"
    elif pilihan == '5': # <-- LOGIKA BARU
        # Tugas tanpa tanggal jatuh tempo akan diletakkan di akhir
        max_date = datetime.max
        sorted_tasks = sorted(data['tasks'], key=lambda x: parser.parse(x['due_date']) if x['due_date'] else max_date)
        judul = "Tugas Terurut berdasarkan Jatuh Tempo"
    else:
        console.print("[red]Pilihan tidak valid.[/red]")
        return
        
    tampilkan_tugas(list_tugas=sorted_tasks, judul_tabel=judul)

# --- Fungsi lain (pilih_prioritas, tandai_selesai, hapus_tugas, filter_tugas, menu) ---
# --- bisa disalin dari kode sebelumnya atau gunakan yang ada di bawah ini ---

def pilih_prioritas(prioritas_saat_ini=None):
    """Fungsi bantuan untuk memilih prioritas."""
    console.print("Pilih Prioritas" + (f" (saat ini: [bold]{prioritas_saat_ini}[/bold])" if prioritas_saat_ini else "") + ":")
    console.print("1. Rendah")
    console.print("2. Sedang")
    console.print("3. Tinggi")
    
    map_pilihan = {'1': 'Rendah', '2': 'Sedang', '3': 'Tinggi'}
    while True:
        pilihan = input("Pilihan Anda (1-3): ").strip()
        if pilihan in map_pilihan:
            return map_pilihan[pilihan]
        if prioritas_saat_ini and pilihan == '':
            return prioritas_saat_ini
        console.print("[red]Pilihan tidak valid. Harap masukkan 1, 2, atau 3.[/red]")

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
        task_to_remove = next((task for task in data['tasks'] if task['id'] == id_to_delete), None)
        
        if task_to_remove:
            data['tasks'].remove(task_to_remove)
            simpan_data()
            console.print(f"\n[bold green]✓ Tugas '[white]{task_to_remove['title']}[/white]' telah dihapus.[/bold green]")
        else:
            console.print(f"[bold red]Tugas dengan ID {id_to_delete} tidak ditemukan.[/bold red]")
    except ValueError:
        console.print("[bold red]Input tidak valid. Harap masukkan ID berupa angka.[/bold red]")

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
    muat_data()
    
    console.print("\n==============================================", style="bold blue")
    console.print("   Selamat Datang di Aplikasi To-Do List v2.2", style="bold blue")
    console.print("==============================================", style="bold blue")
    
    while True:
        console.print("\n--- [bold]Menu Utama[/bold] ---")
        menu_options = {
            "1": "Lihat Semua Tugas", "2": "Tambah Tugas", "3": "Edit Tugas",
            "4": "Tandai Tugas Selesai", "5": "Hapus Tugas", "6": "Urutkan Tugas",
            "7": "Filter Tugas", "8": "Keluar"
        }
        for key, value in menu_options.items():
            console.print(f"[cyan]{key}[/cyan]. {value}")

        pilihan = input("Masukkan pilihan Anda (1-8): ")

        actions = {
            '1': tampilkan_tugas, '2': tambah_tugas, '3': edit_tugas,
            '4': tandai_selesai, '5': hapus_tugas, '6': urutkan_tugas, '7': filter_tugas
        }
        
        if pilihan in actions:
            actions[pilihan]()
        elif pilihan == '8':
            console.print("\n[bold magenta]Terima kasih telah menggunakan aplikasi ini! Sampai jumpa![/bold magenta]")
            break
        else:
            console.print("\n[bold red]Pilihan tidak valid. Silakan coba lagi.[/bold red]")

if __name__ == "__main__":
    menu()
