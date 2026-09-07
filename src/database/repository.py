import sqlite3
import pandas as pd
from typing import Dict, Any, List

DB_PATH = "marchon.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Tabla de 1RMs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_1rms (
        exercise_key TEXT PRIMARY KEY,
        exercise_name TEXT,
        one_rep_max REAL,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    default_1rms = [
        ("bench_press", "Barbell Bench Press", 120.0),
        ("back_squat", "Barbell Back Squat", 140.0),
        ("deadlift", "Trap Bar Deadlift", 165.0),
        ("ohp", "Standing Overhead Press", 70.0)
    ]
    cursor.executemany("""
    INSERT OR IGNORE INTO user_1rms (exercise_key, exercise_name, one_rep_max)
    VALUES (?, ?, ?)
    """, default_1rms)
    
    # 2. Tabla de Series Registradas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exercise_set_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        day_id TEXT,
        exercise_name TEXT,
        set_number INTEGER,
        pct_1rm REAL,
        weight REAL,
        reps INTEGER,
        rpe REAL,
        est_1rm REAL,
        logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # 3. Tabla de Sesiones Completadas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS completed_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        day_id TEXT,
        date TEXT,
        session_title TEXT,
        total_volume_kg REAL,
        duration_minutes INTEGER,
        sauna_completed BOOLEAN,
        completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 4. Tabla de Readiness / Estado Diario
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_readiness (
        date TEXT PRIMARY KEY,
        sleep_score INTEGER,
        energy_score INTEGER,
        arm_soreness INTEGER,
        readiness_pct INTEGER,
        logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

def save_full_session_log(day_id: str, date: str, title: str, sets_records: list, sauna: bool = False, duration: int = 55):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    total_volume = sum([s["weight"] * s["reps"] for s in sets_records])
    
    cursor.execute("""
    INSERT INTO completed_sessions (day_id, date, session_title, total_volume_kg, duration_minutes, sauna_completed)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (day_id, date, title, total_volume, duration, sauna))
    
    for s in sets_records:
        cursor.execute("""
        INSERT INTO exercise_set_logs (date, day_id, exercise_name, set_number, pct_1rm, weight, reps, rpe, est_1rm)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (date, day_id, s["exercise_name"], s["set_num"], s["pct_1rm"], s["weight"], s["reps"], s["rpe"], s["est_1rm"]))
        
    conn.commit()
    conn.close()

def log_readiness(date: str, sleep: int, energy: int, arm_soreness: int) -> int:
    # 15 es el máximo (5+5+(6-soreness))
    raw_score = sleep + energy + (6 - arm_soreness)
    readiness_pct = int((raw_score / 15.0) * 100)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO daily_readiness (date, sleep_score, energy_score, arm_soreness, readiness_pct)
    VALUES (?, ?, ?, ?, ?)
    """, (date, sleep, energy, arm_soreness, readiness_pct))
    conn.commit()
    conn.close()
    return readiness_pct

def get_recent_workout_history(limit: int = 15) -> List[Dict[str, Any]]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT date, session_title, total_volume_kg, duration_minutes, sauna_completed, completed_at
    FROM completed_sessions
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [
        {"date": r[0], "title": r[1], "volume_kg": r[2], "duration": r[3], "sauna": bool(r[4]), "timestamp": r[5]}
        for r in rows
    ]

def export_all_logs_dataframe() -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT date, day_id, exercise_name, set_number, pct_1rm, weight, reps, rpe, est_1rm, logged_at
    FROM exercise_set_logs
    ORDER BY id DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_completed_sessions_count() -> int:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM completed_sessions")
    count = cursor.fetchone()[0]
    conn.close()
    return count
