import json
import os
from datetime import datetime
from dateutil import parser
from rich.console import Console
from rich.table import Table

# Inisialisasi
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
                    task.setdefault("due_date", None)
                    task.setdefault("subtasks", []) # <-- KOMPATIBILITAS BARU
                data = loaded_data
        except (json.JSONDecodeError, KeyError):
            console.print("[bold red]File data rusak! Membuat file baru.[/bold red]")
            data = {"tasks": [], "next_id": 1}

def simpan_data():
    """Menyimpan state aplikasi ke file JSON."""
    with open(NAMA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def tampilkan_tugas(list_tugas=None, judul_tabel="Daftar Tugas Anda"):
    """Menampilkan tugas dalam tabel, kini dengan kolom progress Sub-Tugas."""
    tasks_to_show = list_tugas if list_tugas is not None else data['tasks']
    console.print(f"\n--- [bold cyan]{judul_tabel}[/bold cyan] ---")
    if not tasks_to_show:
        console.print("[yellow]Tidak ada tugas untuk ditampilkan.[/yellow]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=5)
    table.add_column("Judul Tugas", min_width=20)
    table.add_column("Sub-Tugas", width=12, justify="center") # <-- KOLOM BARU
    table.add_column("Prioritas", min_width=10)
    table.add_column("Jatuh Tempo", min_width=18)
    table.add_column("Status", min_width=15)
    
    priority_styles = {"Tinggi": "bold red", "Sedang": "yellow", "Rendah": "green"}
    now = datetime.now()

    for task in tasks_to_show:
        # ... (logika status, prioritas, dan jatuh tempo tetap sama)
        status_style = "green" if task['status'] == 'Selesai' else "yellow"
        priority = task.get("priority", "Sedang")
        p_style = priority_styles.get(priority, "white")
        due_date_str = task.get("due_date")
        due_date_display, date_style = "N/A", "dim"
        if due_date_str:
            due_date = parser.parse(due_date_str)
            due_date_display = due_date.strftime('%Y-%m-%d %H:%M')
            if task['status'] != 'Selesai' and due_date < now: date_style = "bold red"
            elif task['status'] != 'Selesai' and (due_date - now).days < 1: date_style = "bold yellow"
        
        # Logika untuk menampilkan progress sub-tugas
        subtasks = task.get("subtasks", [])
        sub_display = "-"
        if subtasks:
            selesai = sum(1 for st in subtasks if st['status'] == 'Selesai')
            total = len(subtasks)
            emoji = "✅" if selesai == total else "📝"
            sub_display = f"{emoji} {selesai}/{total}"
        
        table.add_row(
            str(task['id']), task['title'], sub_display, # <-- DATA BARU
            f"[{p_style}]{priority}[/{p_style}]", f"[{date_style}]{due_date_display}[/{date_style}]",
            f"[{status_style}]{task['status']}[/{status_style}]"
        )
    
    console.print(table)

def tambah_tugas():
    """Menambahkan tugas baru, diinisialisasi dengan list sub-tugas kosong."""
    console.print("\n--- [bold green]Tambah Tugas Baru[/bold green] ---")
    title = ""
    while not title:
        title = input("Masukkan judul tugas: ").strip()
        if not title: console.print("[red]Judul tidak boleh kosong.[/red]")

    description = input("Masukkan deskripsi tugas: ").strip()
    priority = pilih_prioritas()
    due_date = get_due_date_input()

    new_task = {
        "id": data['next_id'], "title": title, "description": description,
        "priority": priority, "status": "Belum Selesai", "due_date": due_date,
        "subtasks": [] # <-- FIELD BARU
    }
    data['tasks'].append(new_task)
    data['next_id'] += 1
    simpan_data()
    console.print(f"\n[bold green]✓ Tugas '[white]{title}[/white]' berhasil ditambahkan![/bold green]")

def kelola_sub_tugas():
    """Menu utama untuk semua operasi yang berhubungan dengan sub-tugas."""
    tampilkan_tugas()
    if not data['tasks']: return

    try:
        id_to_manage = int(input("Masukkan ID tugas utama yang ingin dikelola sub-tugasnya: "))
        main_task = next((task for task in data['tasks'] if task['id'] == id_to_manage), None)

        if not main_task:
            console.print(f"[bold red]Tugas dengan ID {id_to_manage} tidak ditemukan.[/bold red]")
            return

        while True:
            console.print(f"\n--- Mengelola Sub-Tugas untuk: [bold yellow]'{main_task['title']}'[/bold yellow] ---")
            subtasks = main_task.get("subtasks", [])
            if not subtasks:
                console.print("[yellow]Belum ada sub-tugas.[/yellow]")
            else:
                for i, st in enumerate(subtasks):
                    emoji = "✅" if st['status'] == 'Selesai' else "📝"
                    console.print(f"{i+1}. {emoji} {st['title']}")

            console.print("\n--- Menu Sub-Tugas ---")
            console.print("1. Tambah Sub-Tugas")
            console.print("2. Tandai Sub-Tugas Selesai")
            console.print("3. Hapus Sub-Tugas")
            console.print("4. Kembali ke Menu Utama")
            pilihan = input("Pilihan Anda (1-4): ")

            if pilihan == '1':
                sub_title = input("Masukkan judul sub-tugas baru: ").strip()
                if sub_title:
                    main_task['subtasks'].append({"title": sub_title, "status": "Belum Selesai"})
                    simpan_data()
                    console.print("[green]Sub-tugas berhasil ditambahkan.[/green]")
            elif pilihan == '2':
                if not subtasks:
                    console.print("[yellow]Tidak ada sub-tugas untuk ditandai.[/yellow]")
                    continue
                try:
                    idx_to_mark = int(input(f"Masukkan nomor sub-tugas yang selesai (1-{len(subtasks)}): ")) - 1
                    if 0 <= idx_to_mark < len(subtasks):
                        subtasks[idx_to_mark]['status'] = 'Selesai'
                        simpan_data()
                        console.print("[green]Status sub-tugas diperbarui.[/green]")
                    else:
                        console.print("[red]Nomor tidak valid.[/red]")
                except ValueError:
                    console.print("[red]Input harus berupa angka.[/red]")
            elif pilihan == '3':
                if not subtasks:
                    console.print("[yellow]Tidak ada sub-tugas untuk dihapus.[/yellow]")
                    continue
                try:
                    idx_to_del = int(input(f"Masukkan nomor sub-tugas yang ingin dihapus (1-{len(subtasks)}): ")) - 1
                    if 0 <= idx_to_del < len(subtasks):
                        removed = subtasks.pop(idx_to_del)
                        simpan_data()
                        console.print(f"[green]Sub-tugas '[white]{removed['title']}[/white]' berhasil dihapus.[/green]")
                    else:
                        console.print("[red]Nomor tidak valid.[/red]")
                except ValueError:
                    console.print("[red]Input harus berupa angka.[/red]")
            elif pilihan == '4':
                break
            else:
                console.print("[red]Pilihan tidak valid.[/red]")

    except ValueError:
        console.print("[bold red]Input ID harus berupa angka.[/bold red]")

def menu():
    """Fungsi utama untuk menampilkan menu dan mengatur alur aplikasi."""
    muat_data()
    console.print("\n" + "="*46, style="bold blue")
    console.print("   Selamat Datang di Aplikasi To-Do List v2.3", style="bold blue")
    console.print("="*46, style="bold blue")
    
    while True:
        console.print("\n--- [bold]Menu Utama[/bold] ---")
        menu_options = {
            "1": "Lihat Semua Tugas", "2": "Tambah Tugas", "3": "Edit Tugas",
            "4": "Kelola Sub-Tugas", # <-- MENU BARU
            "5": "Tandai Tugas Selesai", "6": "Hapus Tugas", "7": "Urutkan Tugas",
            "8": "Filter Tugas", "9": "Keluar"
        }
        for key, value in menu_options.items():
            console.print(f"[cyan]{key}[/cyan]. {value}")

        pilihan = input("Masukkan pilihan Anda (1-9): ")
        actions = {'1': tampilkan_tugas, '2': tambah_tugas, '3': edit_tugas,
                   '4': kelola_sub_tugas, '5': tandai_selesai, '6': hapus_tugas,
                   '7': urutkan_tugas, '8': filter_tugas }
        
        if pilihan in actions:
            actions[pilihan]()
        elif pilihan == '9':
            console.print("\n[bold magenta]Terima kasih telah menggunakan aplikasi ini! Sampai jumpa![/bold magenta]")
            break
        else:
            console.print("\n[bold red]Pilihan tidak valid. Silakan coba lagi.[/bold red]")

# --- Fungsi-fungsi lain yang tidak berubah signifikan ---
# (Fungsi-fungsi seperti edit_tugas, urutkan_tugas, pilih_prioritas, dll.
#  bisa disalin dari kode versi sebelumnya)
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
        if not user_input: return None if display_current.endswith("hapus)") else due_date_saat_ini
        try:
            dt_object = parser.parse(user_input)
            return dt_object.isoformat()
        except parser.ParserError: console.print("[red]Format tanggal tidak valid.[/red]")

def pilih_prioritas(prioritas_saat_ini=None):
    """Fungsi bantuan untuk memilih prioritas."""
    console.print("Pilih Prioritas" + (f" (saat ini: [bold]{prioritas_saat_ini}[/bold])" if prioritas_saat_ini else "") + ":")
    console.print("1. Rendah\n2. Sedang\n3. Tinggi")
    map_pilihan = {'1': 'Rendah', '2': 'Sedang', '3': 'Tinggi'}
    while True:
        pilihan = input("Pilihan Anda (1-3): ").strip()
        if pilihan in map_pilihan: return map_pilihan[pilihan]
        if prioritas_saat_ini and pilihan == '': return prioritas_saat_ini
        console.print("[red]Pilihan tidak valid.[/red]")

def edit_tugas():
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
            new_desc = input(f"Deskripsi baru ({task_to_edit.get('description', '')}): ").strip()
            if new_desc: task_to_edit['description'] = new_desc
            task_to_edit['priority'] = pilih_prioritas(task_to_edit.get("priority", "Sedang"))
            task_to_edit['due_date'] = get_due_date_input(task_to_edit.get("due_date"))
            simpan_data()
            console.print(f"\n[bold green]✓ Tugas dengan ID {id_to_edit} berhasil diperbarui.[/bold green]")
        else: console.print(f"[bold red]Tugas dengan ID {id_to_edit} tidak ditemukan.[/bold red]")
    except ValueError: console.print("[bold red]Input tidak valid.[/bold red]")

def tandai_selesai():
    """Menandai sebuah tugas utama sebagai 'Selesai'."""
    tampilkan_tugas(list_tugas=[t for t in data['tasks'] if t['status'] == 'Belum Selesai'], judul_tabel="Tugas yang Belum Selesai")
    if not any(t['status'] == 'Belum Selesai' for t in data['tasks']): return
    try:
        id_to_mark = int(input("Masukkan ID tugas yang ingin ditandai selesai: "))
        task = next((t for t in data['tasks'] if t['id'] == id_to_mark), None)
        if task:
            if task['status'] == 'Selesai': console.print(f"[yellow]Tugas '{task['title']}' sudah selesai.[/yellow]")
            else:
                task['status'] = "Selesai"
                simpan_data()
                console.print(f"\n[bold green]✓ Tugas '[white]{task['title']}[/white]' telah ditandai selesai.[/bold green]")
        else: console.print(f"[bold red]Tugas dengan ID {id_to_mark} tidak ditemukan.[/bold red]")
    except ValueError: console.print("[bold red]Input ID harus berupa angka.[/bold red]")

def hapus_tugas():
    tampilkan_tugas()
    if not data['tasks']: return
    try:
        id_to_delete = int(input("Masukkan ID tugas yang ingin dihapus: "))
        task_to_remove = next((task for task in data['tasks'] if task['id'] == id_to_delete), None)
        if task_to_remove:
            data['tasks'].remove(task_to_remove)
            simpan_data()
            console.print(f"\n[bold green]✓ Tugas '[white]{task_to_remove['title']}[/white]' telah dihapus.[/bold green]")
        else: console.print(f"[bold red]Tugas dengan ID {id_to_delete} tidak ditemukan.[/bold red]")
    except ValueError: console.print("[bold red]Input ID harus berupa angka.[/bold red]")

def urutkan_tugas():
    if not data['tasks']: console.print("\n[yellow]Tidak ada tugas untuk diurutkan.[/yellow]"); return
    console.print("\nUrutkan tugas berdasarkan:\n1. ID\n2. Judul\n3. Status\n4. Prioritas\n5. Jatuh Tempo")
    pilihan = input("Pilihan Anda (1-5): ")
    judul = "Tugas Terurut"
    if pilihan == '1': sorted_tasks = sorted(data['tasks'], key=lambda x: x['id'])
    elif pilihan == '2': sorted_tasks = sorted(data['tasks'], key=lambda x: x['title'].lower())
    elif pilihan == '3': sorted_tasks = sorted(data['tasks'], key=lambda x: x['status'])
    elif pilihan == '4':
        priority_map = {"Tinggi": 3, "Sedang": 2, "Rendah": 1}
        sorted_tasks = sorted(data['tasks'], key=lambda x: priority_map.get(x.get('priority', 'Sedang'), 0), reverse=True)
    elif pilihan == '5':
        max_date = datetime.max
        sorted_tasks = sorted(data['tasks'], key=lambda x: parser.parse(x['due_date']) if x['due_date'] else max_date)
    else: console.print("[red]Pilihan tidak valid.[/red]"); return
    tampilkan_tugas(list_tugas=sorted_tasks, judul_tabel=judul)

def filter_tugas():
    if not data['tasks']: console.print("\n[yellow]Tidak ada tugas untuk difilter.[/yellow]"); return
    console.print("\nTampilkan tugas dengan status:\n1. Selesai\n2. Belum Selesai")
    pilihan = input("Pilihan Anda (1-2): ")
    if pilihan == '1': filtered_tasks = [t for t in data['tasks'] if t['status'] == 'Selesai']
    elif pilihan == '2': filtered_tasks = [t for t in data['tasks'] if t['status'] == 'Belum Selesai']
    else: console.print("[red]Pilihan tidak valid.[/red]"); return
    tampilkan_tugas(list_tugas=filtered_tasks)

if __name__ == "__main__":
    menu()
