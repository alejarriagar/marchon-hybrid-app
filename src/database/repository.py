import sqlite3
from typing import Dict, Any, List

DB_PATH = "marchon.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Tabla de 1RMs del usuario
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_1rms (
        exercise_key TEXT PRIMARY KEY,
        exercise_name TEXT,
        one_rep_max REAL,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Insertar valores base iniciales si no existen
    default_1rms = [
        ("bench_press", "Barbell Bench Press", 120.0),
        ("back_squat", "Barbell Back Squat", 140.0),
        ("deadlift", "Trap Bar Deadlift", 165.0),
        ("ohp", "Standing Overhead Press", 70.0),
        ("pull_up", "Weighted Pull-up (Total)", 100.0) # 80kg peso + 20kg lastre
    ]
    cursor.executemany("""
    INSERT OR IGNORE INTO user_1rms (exercise_key, exercise_name, one_rep_max)
    VALUES (?, ?, ?)
    """, default_1rms)
    
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

def get_all_user_1rms() -> Dict[str, float]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT exercise_key, one_rep_max FROM user_1rms")
    records = cursor.fetchall()
    conn.close()
    return {k: v for k, v in records}

def update_user_1rm(exercise_key: str, new_1rm: float):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE user_1rms 
    SET one_rep_max = ?, updated_at = CURRENT_TIMESTAMP
    WHERE exercise_key = ?
    """, (new_1rm, exercise_key))
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
