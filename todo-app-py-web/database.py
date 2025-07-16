# file: database.py
import sqlite3
from datetime import datetime

NAMA_DB = "todo_app.db"

def get_db_connection():
    """Membuat dan mengembalikan koneksi ke database."""
    conn = sqlite3.connect(NAMA_DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(app):
    """Membuat tabel database jika belum ada di dalam konteks aplikasi Flask."""
    with app.app_context():
        db = get_db_connection()
        with open('schema.sql', 'r') as f:
            db.executescript(f.read())
        db.commit()

def get_all_tasks():
    """Mengambil semua tugas utama beserta progress sub-tugasnya."""
    conn = get_db_connection()
    query = """
        SELECT 
            t.*,
            (SELECT COUNT(*) FROM subtasks s WHERE s.task_id = t.id) AS total_sub,
            (SELECT COUNT(*) FROM subtasks s WHERE s.task_id = t.id AND s.status = 'Selesai') AS selesai_sub
        FROM tasks t
        ORDER BY CASE t.priority WHEN 'Tinggi' THEN 3 WHEN 'Sedang' THEN 2 ELSE 1 END DESC, 
                 t.due_date ASC, t.id ASC
    """
    tasks = conn.execute(query).fetchall()
    conn.close()
    return tasks

def get_task_with_subtasks(task_id):
    """Mengambil satu tugas utama dan semua sub-tugasnya."""
    conn = get_db_connection()
    task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    subtasks = conn.execute("SELECT * FROM subtasks WHERE task_id = ? ORDER BY id", (task_id,)).fetchall()
    conn.close()
    return task, subtasks

# --- Fungsi untuk memodifikasi data akan ditambahkan di sini nanti ---
# (Kita akan memanggilnya dari app.py)