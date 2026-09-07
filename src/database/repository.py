import sqlite3
from typing import Dict, Any, List

DB_PATH = "marchon.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Tabla para logs de ejercicios detallados por serie
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exercise_set_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        day_id TEXT,
        exercise_name TEXT,
        set_number INTEGER,
        weight REAL,
        reps INTEGER,
        rpe REAL,
        completed BOOLEAN DEFAULT 1
    )
    """)
    
    # Tabla para registro de sesiones
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS completed_sessions (
        day_id TEXT PRIMARY KEY,
        date TEXT,
        completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        duration_minutes INTEGER,
        sauna_completed BOOLEAN
    )
    """)
    
    conn.commit()
    conn.close()

def save_exercise_sets(day_id: str, date: str, exercise_name: str, sets_list: list):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for s in sets_list:
        cursor.execute("""
        INSERT INTO exercise_set_logs (date, day_id, exercise_name, set_number, weight, reps, rpe, completed)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (date, day_id, exercise_name, s["set_num"], s["weight"], s["reps"], s["rpe"], s["completed"]))
    conn.commit()
    conn.close()

def log_session(day_id: str, date: str, duration: int = 55, sauna: bool = False):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO completed_sessions (day_id, date, duration_minutes, sauna_completed)
    VALUES (?, ?, ?, ?)
    """, (day_id, date, duration, sauna))
    conn.commit()
    conn.close()

def get_completed_sessions_count() -> int:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM completed_sessions")
    count = cursor.fetchone()[0]
    conn.close()
    return count
