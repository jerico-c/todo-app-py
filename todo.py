import sqlite3
import os
from datetime import datetime
from dateutil import parser
from rich.console import Console
from rich.table import Table
import json # Hanya untuk migrasi

# --- Inisialisasi Global ---
console = Console()
NAMA_DB = "todo_app.db"
JSON_LAMA = "tasks_data.json"

# --- Fungsi Database ---
def get_db_connection():
    """Membuat dan mengembalikan koneksi ke database."""
    conn = sqlite3.connect(NAMA_DB)
    conn.row_factory = sqlite3.Row # Mengembalikan baris sebagai dictionary
    return conn

def init_db():
    """Membuat tabel database jika belum ada."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # Tabel tugas utama
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT DEFAULT 'Sedang' CHECK(priority IN ('Rendah', 'Sedang', 'Tinggi')),
            status TEXT DEFAULT 'Belum Selesai' CHECK(status IN ('Belum Selesai', 'Selesai')),
            due_date TEXT
        )
    ''')
    # Tabel sub-tugas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subtasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            status TEXT DEFAULT 'Belum Selesai' CHECK(status IN ('Belum Selesai', 'Selesai')),
            FOREIGN KEY (task_id) REFERENCES tasks (id) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()

def migrasi_dari_json():
    """Fungsi sekali jalan untuk memigrasikan data dari JSON ke SQLite."""
    if os.path.exists(JSON_LAMA) and os.path.getsize(NAMA_DB) == 0:
        console.print(f"[yellow]Mendeteksi file '{JSON_LAMA}'. Memulai migrasi data ke SQLite...[/yellow]")
        with open(JSON_LAMA, 'r') as f:
            data_lama = json.load(f)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        for task in data_lama.get("tasks", []):
            cursor.execute(
                "INSERT INTO tasks (title, description, priority, status, due_date) VALUES (?, ?, ?, ?, ?)",
                (task.get('title', ''), task.get('description', ''), task.get('priority', 'Sedang'), task.get('status', 'Belum Selesai'), task.get('due_date'))
            )
            task_id_baru = cursor.lastrowid
            for subtask in task.get("subtasks", []):
                cursor.execute(
                    "INSERT INTO subtasks (task_id, title, status) VALUES (?, ?, ?)",
                    (task_id_baru, subtask['title'], subtask['status'])
                )
        
        conn.commit()
        conn.close()
        os.rename(JSON_LAMA, JSON_LAMA + ".migrated")
        console.print("[bold green]✓ Migrasi data berhasil![/bold green]")

# --- Fungsi Tampilan ---
def tampilkan_tugas(where_clause="", params=(), order_by="ORDER BY id ASC", judul_tabel="Daftar Tugas Anda"):
    """Menampilkan tugas dari database dengan query yang fleksibel."""
    conn = get_db_connection()
    query = f'''
        SELECT 
            t.id, t.title, t.priority, t.due_date, t.status,
            (SELECT COUNT(*) FROM subtasks s WHERE s.task_id = t.id) AS total_sub,
            (SELECT COUNT(*) FROM subtasks s WHERE s.task_id = t.id AND s.status = 'Selesai') AS selesai_sub
        FROM tasks t
        {where_clause}
        {order_by}
    '''
    tasks = conn.execute(query, params).fetchall()
    conn.close()

    console.print(f"\n--- [bold cyan]{judul_tabel}[/bold cyan] ---")
    if not tasks:
        console.print("[yellow]Tidak ada tugas untuk ditampilkan.[/yellow]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=5)
    table.add_column("Judul Tugas", min_width=20)
    table.add_column("Sub-Tugas", width=12, justify="center")
    table.add_column("Prioritas", min_width=10)
    table.add_column("Jatuh Tempo", min_width=18)
    table.add_column("Status", min_width=15)
    
    priority_styles = {"Tinggi": "bold red", "Sedang": "yellow", "Rendah": "green"}
    now = datetime.now()

    for task in tasks:
        status_style = "green" if task['status'] == 'Selesai' else "yellow"
        p_style = priority_styles.get(task['priority'], "white")
        
        due_date_display, date_style = "N/A", "dim"
        if task['due_date']:
            due_date = parser.parse(task['due_date'])
            due_date_display = due_date.strftime('%Y-%m-%d %H:%M')
            if task['status'] != 'Selesai':
                if due_date < now: date_style = "bold red"
                elif (due_date - now).days < 1: date_style = "bold yellow"
        
        sub_display = "-"
        if task['total_sub'] > 0:
            emoji = "✅" if task['selesai_sub'] == task['total_sub'] else "📝"
            sub_display = f"{emoji} {task['selesai_sub']}/{task['total_sub']}"
        
        table.add_row(
            str(task['id']), task['title'], sub_display,
            f"[{p_style}]{task['priority']}[/{p_style}]", f"[{date_style}]{due_date_display}[/{date_style}]",
            f"[{status_style}]{task['status']}[/{status_style}]"
        )
    console.print(table)

# --- Fungsi Helper Input ---
def pilih_prioritas(prioritas_saat_ini=None):
    """Fungsi bantuan untuk memilih prioritas dari menu."""
    prompt = "Pilih Prioritas"
    if prioritas_saat_ini:
        prompt += f" (saat ini: [bold]{prioritas_saat_ini}[/bold], Enter untuk lewati)"
    
    console.print(prompt + ":")
    console.print("1. Rendah\n2. Sedang\n3. Tinggi")
    
    map_pilihan = {'1': 'Rendah', '2': 'Sedang', '3': 'Tinggi'}
    while True:
        pilihan = input("Pilihan Anda (1-3): ").strip()
        if pilihan in map_pilihan: return map_pilihan[pilihan]
        if prioritas_saat_ini and pilihan == '': return prioritas_saat_ini
        console.print("[red]Pilihan tidak valid. Harap masukkan 1, 2, atau 3.[/red]")

def get_due_date_input(due_date_saat_ini=None):
    """Fungsi bantuan untuk mendapatkan input tanggal jatuh tempo."""
    prompt = "Masukkan Tanggal Jatuh Tempo"
    if due_date_saat_ini:
        try:
            current_dt = parser.parse(due_date_saat_ini).strftime('%Y-%m-%d %H:%M')
            prompt += f" (saat ini: [bold]{current_dt}[/bold])"
        except (parser.ParserError, TypeError):
            prompt += " (saat ini: tidak valid)"
    
    console.print(prompt + ":")
    console.print("Format: YYYY-MM-DD HH:MM (waktu opsional). Kosongkan untuk hapus/lewati.")
    
    while True:
        user_input = input("> ").strip()
        if not user_input: return due_date_saat_ini
        try:
            return parser.parse(user_input).isoformat()
        except parser.ParserError:
            console.print("[red]Format tanggal tidak valid. Silakan coba lagi.[/red]")

# --- Fungsi Logika Utama ---
def tambah_tugas():
    """Menambahkan tugas baru ke database."""
    console.print("\n--- [bold green]Tambah Tugas Baru[/bold green] ---")
    title = ""
    while not title:
        title = input("Masukkan judul tugas: ").strip()
        if not title: console.print("[red]Judul tidak boleh kosong.[/red]")

    description = input("Masukkan deskripsi tugas: ").strip()
    priority = pilih_prioritas()
    due_date = get_due_date_input()

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO tasks (title, description, priority, due_date) VALUES (?, ?, ?, ?)",
        (title, description, priority, due_date)
    )
    conn.commit()
    conn.close()
    console.print(f"\n[bold green]✓ Tugas '[white]{title}[/white]' berhasil ditambahkan![/bold green]")

def edit_tugas():
    """Mengedit tugas yang ada di database."""
    tampilkan_tugas()
    try:
        id_to_edit = int(input("Masukkan ID tugas yang ingin diedit: "))
        conn = get_db_connection()
        task_to_edit = conn.execute("SELECT * FROM tasks WHERE id = ?", (id_to_edit,)).fetchone()
        
        if task_to_edit:
            console.print(f"\nMengedit tugas: [bold yellow]'{task_to_edit['title']}'[/bold yellow]")
            
            new_title = input(f"Judul baru ({task_to_edit['title']}): ").strip() or task_to_edit['title']
            new_desc = input(f"Deskripsi baru ({task_to_edit['description']}): ").strip() or task_to_edit['description']
            new_priority = pilih_prioritas(task_to_edit['priority'])
            new_due_date = get_due_date_input(task_to_edit['due_date'])
            
            conn.execute(
                "UPDATE tasks SET title = ?, description = ?, priority = ?, due_date = ? WHERE id = ?",
                (new_title, new_desc, new_priority, new_due_date, id_to_edit)
            )
            conn.commit()
            console.print(f"\n[bold green]✓ Tugas dengan ID {id_to_edit} berhasil diperbarui.[/bold green]")
        else:
            console.print(f"[bold red]Tugas dengan ID {id_to_edit} tidak ditemukan.[/bold red]")
        conn.close()
    except ValueError:
        console.print("[bold red]Input tidak valid.[/bold red]")

def kelola_sub_tugas():
    """Menu untuk mengelola sub-tugas dari sebuah tugas utama."""
    tampilkan_tugas()
    try:
        id_to_manage = int(input("Masukkan ID tugas utama yang ingin dikelola: "))
        conn = get_db_connection()
        main_task = conn.execute("SELECT id, title FROM tasks WHERE id = ?", (id_to_manage,)).fetchone()

        if not main_task:
            console.print(f"[bold red]Tugas dengan ID {id_to_manage} tidak ditemukan.[/bold red]")
            conn.close()
            return
        
        while True:
            console.print(f"\n--- Mengelola Sub-Tugas untuk: [bold yellow]'{main_task['title']}'[/bold yellow] ---")
            subtasks = conn.execute("SELECT id, title, status FROM subtasks WHERE task_id = ? ORDER BY id", (id_to_manage,)).fetchall()
            
            if not subtasks: console.print("[yellow]Belum ada sub-tugas.[/yellow]")
            else:
                for i, st in enumerate(subtasks):
                    emoji = "✅" if st['status'] == 'Selesai' else "📝"
                    console.print(f"{i+1}. {emoji} {st['title']}")

            console.print("\n[bold]Menu Sub-Tugas:[/bold] 1. Tambah | 2. Tandai Selesai | 3. Hapus | 4. Kembali")
            pilihan = input("> ")

            try:
                if pilihan == '1':
                    sub_title = input("Judul sub-tugas baru: ").strip()
                    if sub_title:
                        conn.execute("INSERT INTO subtasks (task_id, title) VALUES (?, ?)", (id_to_manage, sub_title))
                        conn.commit()
                elif pilihan == '2' and subtasks:
                    idx = int(input(f"No. sub-tugas selesai (1-{len(subtasks)}): ")) - 1
                    if 0 <= idx < len(subtasks):
                        conn.execute("UPDATE subtasks SET status = 'Selesai' WHERE id = ?", (subtasks[idx]['id'],))
                        conn.commit()
                elif pilihan == '3' and subtasks:
                    idx = int(input(f"No. sub-tugas hapus (1-{len(subtasks)}): ")) - 1
                    if 0 <= idx < len(subtasks):
                        conn.execute("DELETE FROM subtasks WHERE id = ?", (subtasks[idx]['id'],))
                        conn.commit()
                elif pilihan == '4':
                    break
            except (ValueError, IndexError):
                console.print("[red]Input nomor tidak valid.[/red]")
        conn.close()
    except ValueError:
        console.print("[red]Input ID harus berupa angka.[/red]")

def tandai_selesai():
    """Menandai tugas utama sebagai 'Selesai'."""
    tampilkan_tugas("WHERE status = ?", ('Belum Selesai',), judul_tabel="Tugas yang Belum Selesai")
    try:
        id_to_mark = int(input("Masukkan ID tugas yang selesai: "))
        conn = get_db_connection()
        result = conn.execute("UPDATE tasks SET status = 'Selesai' WHERE id = ? AND status = 'Belum Selesai'", (id_to_mark,))
        conn.commit()
        conn.close()
        if result.rowcount > 0:
            console.print("[green]Tugas ditandai selesai.[/green]")
        else:
            console.print("[yellow]Tugas tidak ditemukan atau sudah selesai.[/yellow]")
    except ValueError:
        console.print("[red]Input ID harus berupa angka.[/red]")

def hapus_tugas():
    """Menghapus tugas utama (dan sub-tugasnya) dari database."""
    tampilkan_tugas()
    try:
        id_to_delete = int(input("Masukkan ID tugas yang ingin dihapus: "))
        conn = get_db_connection()
        result = conn.execute("DELETE FROM tasks WHERE id = ?", (id_to_delete,))
        conn.commit()
        conn.close()
        if result.rowcount > 0:
            console.print(f"\n[bold green]✓ Tugas dengan ID {id_to_delete} berhasil dihapus.[/bold green]")
        else:
            console.print(f"[bold red]Tugas dengan ID {id_to_delete} tidak ditemukan.[/bold red]")
    except ValueError:
        console.print("[red]Input ID harus berupa angka.[/red]")

def urutkan_tugas():
    """Mengurutkan tugas menggunakan ORDER BY di SQL."""
    console.print("\nUrutkan tugas berdasarkan:\n1. ID\n2. Judul\n3. Status\n4. Prioritas\n5. Jatuh Tempo")
    pilihan = input("Pilihan Anda (1-5): ")
    order_clause = ""
    if pilihan == '1': order_clause = "ORDER BY id ASC"
    elif pilihan == '2': order_clause = "ORDER BY title ASC"
    elif pilihan == '3': order_clause = "ORDER BY status ASC"
    elif pilihan == '4': order_clause = "ORDER BY CASE priority WHEN 'Tinggi' THEN 3 WHEN 'Sedang' THEN 2 WHEN 'Rendah' THEN 1 END DESC, id ASC"
    elif pilihan == '5': order_clause = "ORDER BY due_date ASC, id ASC"
    else: console.print("[red]Pilihan tidak valid.[/red]"); return
    tampilkan_tugas(order_by=order_clause, judul_tabel="Tugas Terurut")

def filter_tugas():
    """Memfilter tugas menggunakan WHERE di SQL."""
    console.print("\nTampilkan tugas dengan status:\n1. Selesai\n2. Belum Selesai")
    pilihan = input("Pilihan Anda (1-2): ")
    if pilihan == '1':
        tampilkan_tugas("WHERE status = ?", ('Selesai',), judul_tabel="Tugas yang Sudah Selesai")
    elif pilihan == '2':
        tampilkan_tugas("WHERE status = ?", ('Belum Selesai',), judul_tabel="Tugas yang Belum Selesai")
    else:
        console.print("[red]Pilihan tidak valid.[/red]")

# --- Fungsi Menu Utama ---
def menu():
    """Fungsi utama yang menjalankan aplikasi."""
    init_db()
    migrasi_dari_json()

    console.print("\n" + "="*46, style="bold blue")
    console.print("   Selamat Datang di Aplikasi To-Do List v2.4", style="bold blue")
    console.print("         (Backend: Database SQLite)", style="blue")
    console.print("="*46, style="bold blue")
    
    actions = {'1': tampilkan_tugas, '2': tambah_tugas, '3': edit_tugas,
               '4': kelola_sub_tugas, '5': tandai_selesai, '6': hapus_tugas,
               '7': urutkan_tugas, '8': filter_tugas}
    
    while True:
        console.print("\n--- [bold]Menu Utama[/bold] ---")
        menu_options = { "1": "Lihat Tugas", "2": "Tambah Tugas", "3": "Edit Tugas", "4": "Kelola Sub-Tugas", "5": "Tandai Tugas Selesai", "6": "Hapus Tugas", "7": "Urutkan Tugas", "8": "Filter Tugas", "9": "Keluar" }
        for k, v in menu_options.items(): console.print(f"[cyan]{k}[/cyan]. {v}")
        
        pilihan = input("Pilihan Anda (1-9): ")
        
        if pilihan in actions:
            actions[pilihan]()
        elif pilihan == '9':
            console.print("\n[bold magenta]Terima kasih telah menggunakan aplikasi ini! Sampai jumpa![/bold magenta]")
            break
        else:
            console.print("\n[bold red]Pilihan tidak valid.[/bold red]")

if __name__ == "__main__":
    menu()
