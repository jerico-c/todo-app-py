# file: app.py
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import database
from datetime import datetime
from dateutil import parser

app = Flask(__name__)
app.secret_key = 'kunci_rahasia_anda_yang_sangat_aman' # Ganti dengan kunci Anda sendiri

# Inisialisasi Database
database.init_db(app)

# Helper function untuk Jinja2 template
@app.template_filter('dt')
def format_datetime(value, format='%d %b %Y, %H:%M'):
    if value is None:
        return ""
    return parser.parse(value).strftime(format)

@app.template_filter('is_overdue')
def is_overdue(value):
    if value is None:
        return False
    return parser.parse(value) < datetime.now()

# === Routes Utama ===
@app.route('/')
def index():
    tasks = database.get_all_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/task/<int:task_id>')
def task_detail(task_id):
    task, subtasks = database.get_task_with_subtasks(task_id)
    if task is None:
        flash('Tugas tidak ditemukan!', 'error')
        return redirect(url_for('index'))
    return render_template('task_detail.html', task=task, subtasks=subtasks)


# === Routes untuk Aksi (Tasks) ===
@app.route('/task/add', methods=['POST'])
def add_task():
    conn = database.get_db_connection()
    conn.execute(
        "INSERT INTO tasks (title, priority, due_date) VALUES (?, ?, ?)",
        (request.form['title'], request.form['priority'], request.form['due_date'] or None)
    )
    conn.commit()
    conn.close()
    flash('Tugas baru berhasil ditambahkan!', 'success')
    return redirect(url_for('index'))

@app.route('/task/<int:task_id>/update', methods=['POST'])
def update_task(task_id):
    conn = database.get_db_connection()
    conn.execute(
        "UPDATE tasks SET title = ?, description = ?, priority = ?, due_date = ? WHERE id = ?",
        (request.form['title'], request.form['description'], request.form['priority'], request.form['due_date'] or None, task_id)
    )
    conn.commit()
    conn.close()
    flash('Tugas berhasil diperbarui!', 'success')
    return redirect(url_for('task_detail', task_id=task_id))

@app.route('/task/<int:task_id>/status', methods=['POST'])
def update_task_status(task_id):
    new_status = request.form['status']
    conn = database.get_db_connection()
    conn.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
    conn.commit()
    conn.close()
    flash('Status tugas berhasil diperbarui!', 'success')
    return redirect(request.referrer or url_for('index')) # Kembali ke halaman sebelumnya

@app.route('/task/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    conn = database.get_db_connection()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    flash('Tugas berhasil dihapus!', 'success')
    return redirect(url_for('index'))


# === Routes untuk Aksi (Sub-Tasks) ===
@app.route('/task/<int:task_id>/subtask/add', methods=['POST'])
def add_subtask(task_id):
    conn = database.get_db_connection()
    conn.execute(
        "INSERT INTO subtasks (task_id, title) VALUES (?, ?)",
        (task_id, request.form['title'])
    )
    conn.commit()
    conn.close()
    flash('Sub-tugas berhasil ditambahkan!', 'success')
    return redirect(url_for('task_detail', task_id=task_id))

@app.route('/subtask/<int:subtask_id>/status', methods=['POST'])
def update_subtask_status(subtask_id):
    new_status = request.form['status']
    conn = database.get_db_connection()
    conn.execute("UPDATE subtasks SET status = ? WHERE id = ?", (new_status, subtask_id))
    conn.commit()
    conn.close()
    flash('Status sub-tugas diperbarui!', 'success')
    return redirect(request.referrer)

@app.route('/subtask/<int:subtask_id>/delete', methods=['POST'])
def delete_subtask(subtask_id):
    conn = database.get_db_connection()
    conn.execute("DELETE FROM subtasks WHERE id = ?", (subtask_id,))
    conn.commit()
    conn.close()
    flash('Sub-tugas berhasil dihapus!', 'success')
    return redirect(request.referrer)


if __name__ == '__main__':
    app.run(debug=True, port=5001)