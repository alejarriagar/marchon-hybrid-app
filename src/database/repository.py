import datetime as dt
from typing import Any, Dict, List, Optional, Set, Tuple

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text

DB_PATH = "marchon.db"

DEFAULT_1RMS = [
    ("bench_press", "Barbell Bench Press", 120.0),
    ("back_squat", "Barbell Back Squat", 140.0),
    ("deadlift", "Trap Bar Deadlift", 165.0),
    ("ohp", "Standing Overhead Press", 70.0),
]

SCHEMA = [
    """CREATE TABLE IF NOT EXISTS app_settings (
        setting_key TEXT PRIMARY KEY,
        setting_value TEXT
    )""",
    """CREATE TABLE IF NOT EXISTS one_rms (
        exercise_key TEXT PRIMARY KEY,
        exercise_name TEXT,
        one_rep_max DOUBLE PRECISION,
        updated_at TEXT
    )""",
    """CREATE TABLE IF NOT EXISTS set_logs (
        session_date TEXT NOT NULL,
        day_id TEXT NOT NULL,
        block_week INTEGER,
        exercise_key TEXT,
        exercise_name TEXT NOT NULL,
        set_number INTEGER NOT NULL,
        pct_1rm DOUBLE PRECISION,
        weight DOUBLE PRECISION,
        reps INTEGER,
        rpe DOUBLE PRECISION,
        est_1rm DOUBLE PRECISION,
        logged_at TEXT,
        PRIMARY KEY (session_date, day_id, exercise_name, set_number)
    )""",
    """CREATE TABLE IF NOT EXISTS sessions (
        session_date TEXT NOT NULL,
        day_id TEXT NOT NULL,
        title TEXT,
        total_volume_kg DOUBLE PRECISION,
        duration_minutes INTEGER,
        sauna INTEGER,
        completed_at TEXT,
        PRIMARY KEY (session_date, day_id)
    )""",
    """CREATE TABLE IF NOT EXISTS readiness (
        session_date TEXT PRIMARY KEY,
        sleep INTEGER,
        energy INTEGER,
        soreness INTEGER,
        score INTEGER,
        logged_at TEXT
    )""",
]

UPSERT_1RM = """
INSERT INTO one_rms (exercise_key, exercise_name, one_rep_max, updated_at)
VALUES (:key, :name, :value, :ts)
ON CONFLICT (exercise_key) DO UPDATE SET
    one_rep_max = excluded.one_rep_max,
    updated_at = excluded.updated_at
"""

INSERT_DEFAULT_1RM = """
INSERT INTO one_rms (exercise_key, exercise_name, one_rep_max, updated_at)
VALUES (:key, :name, :value, :ts)
ON CONFLICT (exercise_key) DO NOTHING
"""


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def _database_url() -> Optional[str]:
    try:
        url = str(st.secrets["DATABASE_URL"]).strip()
    except Exception:
        return None
    if url.startswith("postgres://"):
        url = "postgresql+psycopg2://" + url[len("postgres://"):]
    elif url.startswith("postgresql://"):
        url = "postgresql+psycopg2://" + url[len("postgresql://"):]
    return url or None


@st.cache_resource
def get_engine():
    url = _database_url()
    if url:
        return create_engine(url, pool_pre_ping=True)
    return create_engine(f"sqlite:///{DB_PATH}")


def using_external_db() -> bool:
    return get_engine().dialect.name != "sqlite"


@st.cache_resource
def ensure_schema() -> bool:
    engine = get_engine()
    with engine.begin() as conn:
        for statement in SCHEMA:
            conn.execute(text(statement))
        existing = conn.execute(text("SELECT COUNT(*) FROM one_rms")).scalar() or 0
        if existing == 0:
            legacy = []
            if engine.dialect.name == "sqlite":
                try:
                    legacy = conn.execute(
                        text("SELECT exercise_key, exercise_name, one_rep_max FROM user_1rms")
                    ).fetchall()
                except Exception:
                    legacy = []
            for key, name, value in legacy:
                conn.execute(text(UPSERT_1RM), {"key": key, "name": name, "value": float(value), "ts": _now()})
            for key, name, value in DEFAULT_1RMS:
                conn.execute(text(INSERT_DEFAULT_1RM), {"key": key, "name": name, "value": value, "ts": _now()})
    return True


def get_setting(key: str, default: Optional[str] = None, persist: bool = False) -> Optional[str]:
    with get_engine().connect() as conn:
        row = conn.execute(
            text("SELECT setting_value FROM app_settings WHERE setting_key = :k"), {"k": key}
        ).fetchone()
    if row is not None:
        return row[0]
    if persist and default is not None:
        set_setting(key, default)
    return default


def set_setting(key: str, value: Any) -> None:
    with get_engine().begin() as conn:
        conn.execute(
            text(
                "INSERT INTO app_settings (setting_key, setting_value) VALUES (:k, :v) "
                "ON CONFLICT (setting_key) DO UPDATE SET setting_value = excluded.setting_value"
            ),
            {"k": key, "v": str(value)},
        )


def get_all_user_1rms() -> Dict[str, float]:
    with get_engine().connect() as conn:
        rows = conn.execute(text("SELECT exercise_key, one_rep_max FROM one_rms")).fetchall()
    return {r[0]: float(r[1] or 0) for r in rows}


def update_user_1rm(exercise_key: str, new_1rm: float, exercise_name: Optional[str] = None) -> None:
    with get_engine().begin() as conn:
        conn.execute(
            text(UPSERT_1RM),
            {"key": exercise_key, "name": exercise_name or exercise_key, "value": float(new_1rm), "ts": _now()},
        )


def save_single_set(session_date: str, day_id: str, block_week: int, exercise_key: Optional[str],
                    exercise_name: str, set_number: int, pct_1rm: float, weight: float,
                    reps: int, rpe: float, est_1rm: float) -> None:
    with get_engine().begin() as conn:
        conn.execute(
            text(
                """
                INSERT INTO set_logs (session_date, day_id, block_week, exercise_key, exercise_name,
                    set_number, pct_1rm, weight, reps, rpe, est_1rm, logged_at)
                VALUES (:d, :day, :bw, :key, :name, :s, :pct, :w, :r, :rpe, :est, :ts)
                ON CONFLICT (session_date, day_id, exercise_name, set_number) DO UPDATE SET
                    block_week = excluded.block_week,
                    exercise_key = excluded.exercise_key,
                    pct_1rm = excluded.pct_1rm,
                    weight = excluded.weight,
                    reps = excluded.reps,
                    rpe = excluded.rpe,
                    est_1rm = excluded.est_1rm,
                    logged_at = excluded.logged_at
                """
            ),
            {
                "d": session_date, "day": day_id, "bw": int(block_week), "key": exercise_key or None,
                "name": exercise_name, "s": int(set_number), "pct": float(pct_1rm), "w": float(weight),
                "r": int(reps), "rpe": float(rpe), "est": float(est_1rm), "ts": _now(),
            },
        )


def get_day_logged_sets(session_date: str, day_id: str) -> Dict[Tuple[str, int], Dict[str, Any]]:
    with get_engine().connect() as conn:
        rows = conn.execute(
            text(
                "SELECT exercise_name, set_number, pct_1rm, weight, reps, rpe, est_1rm "
                "FROM set_logs WHERE session_date = :d AND day_id = :day"
            ),
            {"d": session_date, "day": day_id},
        ).fetchall()
    return {
        (r[0], int(r[1])): {
            "pct_1rm": float(r[2] or 0), "weight": float(r[3] or 0), "reps": int(r[4] or 0),
            "rpe": float(r[5] or 8), "est_1rm": float(r[6] or 0),
        }
        for r in rows
    }


def finalize_session(session_date: str, day_id: str, title: str, sauna: bool, duration: int) -> None:
    with get_engine().begin() as conn:
        volume = conn.execute(
            text("SELECT COALESCE(SUM(weight * reps), 0) FROM set_logs WHERE session_date = :d AND day_id = :day"),
            {"d": session_date, "day": day_id},
        ).scalar() or 0
        conn.execute(
            text(
                """
                INSERT INTO sessions (session_date, day_id, title, total_volume_kg, duration_minutes, sauna, completed_at)
                VALUES (:d, :day, :t, :v, :dur, :sauna, :ts)
                ON CONFLICT (session_date, day_id) DO UPDATE SET
                    title = excluded.title,
                    total_volume_kg = excluded.total_volume_kg,
                    duration_minutes = excluded.duration_minutes,
                    sauna = excluded.sauna,
                    completed_at = excluded.completed_at
                """
            ),
            {"d": session_date, "day": day_id, "t": title, "v": float(volume), "dur": int(duration),
             "sauna": 1 if sauna else 0, "ts": _now()},
        )


def get_completed_dates() -> Set[str]:
    with get_engine().connect() as conn:
        rows = conn.execute(text("SELECT session_date FROM sessions")).fetchall()
    return {r[0] for r in rows}


def get_session_stats() -> Tuple[int, int]:
    with get_engine().connect() as conn:
        row = conn.execute(text("SELECT COUNT(*), COALESCE(SUM(duration_minutes), 0) FROM sessions")).fetchone()
    return int(row[0] or 0), int(row[1] or 0)


def get_recent_sessions(limit: int = 10) -> List[Dict[str, Any]]:
    with get_engine().connect() as conn:
        rows = conn.execute(
            text(
                "SELECT session_date, title, total_volume_kg, duration_minutes, sauna "
                "FROM sessions ORDER BY session_date DESC LIMIT :n"
            ),
            {"n": int(limit)},
        ).fetchall()
    return [
        {"date": r[0], "title": r[1], "volume_kg": float(r[2] or 0), "duration": int(r[3] or 0), "sauna": bool(r[4])}
        for r in rows
    ]


def log_readiness(session_date: str, sleep: int, energy: int, soreness: int) -> int:
    score = int(round((sleep + energy + (6 - soreness)) / 15.0 * 100))
    with get_engine().begin() as conn:
        conn.execute(
            text(
                """
                INSERT INTO readiness (session_date, sleep, energy, soreness, score, logged_at)
                VALUES (:d, :s, :e, :a, :score, :ts)
                ON CONFLICT (session_date) DO UPDATE SET
                    sleep = excluded.sleep, energy = excluded.energy, soreness = excluded.soreness,
                    score = excluded.score, logged_at = excluded.logged_at
                """
            ),
            {"d": session_date, "s": int(sleep), "e": int(energy), "a": int(soreness), "score": score, "ts": _now()},
        )
    return score


def get_readiness(session_date: str) -> Optional[int]:
    with get_engine().connect() as conn:
        row = conn.execute(text("SELECT score FROM readiness WHERE session_date = :d"), {"d": session_date}).fetchone()
    return int(row[0]) if row else None


def get_best_est_1rm_by_key() -> Dict[str, float]:
    with get_engine().connect() as conn:
        rows = conn.execute(
            text(
                "SELECT exercise_key, MAX(est_1rm) FROM set_logs "
                "WHERE exercise_key IS NOT NULL AND exercise_key <> '' GROUP BY exercise_key"
            )
        ).fetchall()
    return {r[0]: float(r[1] or 0) for r in rows}


def export_all_logs_dataframe() -> pd.DataFrame:
    query = text(
        "SELECT session_date, day_id, block_week, exercise_name, set_number, pct_1rm, weight, reps, rpe, est_1rm, logged_at "
        "FROM set_logs ORDER BY session_date DESC, exercise_name, set_number"
    )
    with get_engine().connect() as conn:
        return pd.read_sql_query(query, conn)
