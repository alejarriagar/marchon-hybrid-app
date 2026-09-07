import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import streamlit as st

st.set_page_config(
    page_title="MARCHON Hybrid OS",
    layout="wide",
    initial_sidebar_state="collapsed"
)

import time
import pandas as pd
import plotly.express as px
from src.ui.styles import apply_custom_styles
from src.ui.components import (
    check_pin_auth, render_phase_snapshot, 
    render_kpi_table, render_exercise_item
)
from src.database.repository import (
    init_db, save_single_set, get_day_logged_sets, finalize_session_summary,
    get_completed_sessions_count, get_all_user_1rms, update_user_1rm, 
    get_recent_workout_history, log_readiness, export_all_logs_dataframe
)
from src.services.progression import calculate_estimated_1rm, calculate_target_weight, get_week_periodization_wave, calculate_running_10k_paces
from src.seed_data import SEPTEMBER_PROGRAM, OCTOBER_BJJ_PROGRAM, PROGRAMS_CATALOG

init_db()
apply_custom_styles()

if not check_pin_auth(default_pin="6367"):
    st.stop()

user_1rms = get_all_user_1rms()

if "active_program_id" not in st.session_state:
    st.session_state["active_program_id"] = "perform_sep"
if "selected_day_idx" not in st.session_state:
    st.session_state["selected_day_idx"] = 0
if "current_view" not in st.session_state:
    st.session_state["current_view"] = "workout"
if "current_block_week" not in st.session_state:
    st.session_state["current_block_week"] = 1
if "target_10k_time" not in st.session_state:
    st.session_state["target_10k_time"] = 45.0
if "readiness_score" not in st.session_state:
    st.session_state["readiness_score"] = 90

active_program_data = SEPTEMBER_PROGRAM if st.session_state["active_program_id"] == "perform_sep" else OCTOBER_BJJ_PROGRAM
current_wave = get_week_periodization_wave(st.session_state["current_block_week"])

# -------------------------------------------------------------
# 1. TIRA HORIZONTAL DE CALENDARIO
# -------------------------------------------------------------
cal_cols = st.columns(7)
for idx, day in enumerate(active_program_data):
    with cal_cols[idx]:
        is_selected = (idx == st.session_state["selected_day_idx"])
        if idx < get_completed_sessions_count():
            icon_str = "✓"
        elif day.is_rest_day:
            icon_str = "○"
        else:
            icon_str = "•"
            
        btn_label = f"{icon_str}\n{day.day_name}\n{day.date_num}"
        btn_type = "primary" if is_selected else "secondary"
        
        if st.button(btn_label, key=f"cal_strip_{idx}", use_container_width=True, type=btn_type):
            st.session_state["selected_day_idx"] = idx
            st.rerun()

current_day = active_program_data[st.session_state["selected_day_idx"]]
today_date_str = f"2026-09-{current_day.date_num.zfill(2)}"

# Obtener series ya guardadas en la base de datos para hoy
saved_sets_map = get_day_logged_sets(today_date_str, current_day.day_id)

# -------------------------------------------------------------
# 2. CABECERA MARCHON
# -------------------------------------------------------------
st.markdown(f"""
<div style="margin-top: 0.2rem; margin-bottom: 0.5rem;">
    <div style="font-size: 0.8rem; color: #9CA3AF; font-weight: 700; text-transform: uppercase;">Today {current_day.date_num} Sep 2026</div>
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.1rem; margin-bottom: 0.6rem;">
        <div style="display: flex; gap: 0.8rem; align-items: baseline;">
            <span style="color: #FFFFFF; font-size: 1.4rem; font-weight: 900; letter-spacing: -0.5px;">PERFORM</span>
            <span style="color: #4B5563; font-size: 1.2rem; font-weight: 800; letter-spacing: -0.5px;">HYROX</span>
        </div>
        <div style="color: #6B7280; font-size: 1.3rem; font-weight: 300;">+</div>
    </div>
    <div style="display: flex; gap: 1.2rem; border-bottom: 1px solid rgba(255, 255, 255, 0.08); padding-bottom: 0.4rem; margin-bottom: 0.8rem;">
        <span style="color: #FFFFFF; font-weight: 800; font-size: 0.9rem; border-bottom: 2px solid white; padding-bottom: 4px;">Workout</span>
        <span style="color: #6B7280; font-weight: 600; font-size: 0.9rem;">Coach Notes</span>
        <span style="color: #6B7280; font-weight: 600; font-size: 0.9rem;">Readiness</span>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# VISTA: WORKOUT CON GUARDADO INMEDIATO POR SERIE
# -------------------------------------------------------------
if st.session_state["current_view"] == "workout":
    if current_day.is_rest_day:
        st.markdown(
            '<div style="background: #161922; border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; text-align: center; padding: 2.5rem 1rem;">'
            '<h4 style="color: white; font-weight: 900; text-transform: uppercase;">DESCANSO TOTAL & REGENERACIÓN</h4>'
            '<p style="color: #9CA3AF; font-size: 0.85rem; margin-top: 0.4rem;">Prioriza 8 horas de sueño, nutrición limpia y sesión de sauna.</p>'
            '</div>',
            unsafe_allow_html=True
        )
    else:
        for b_idx, block in enumerate(current_day.blocks):
            block_label = f"[{block.code}]  {block.title.upper()} ({block.subtitle})"
            
            with st.expander(block_label, expanded=(b_idx == 0 or b_idx == 1)):
                if block.rest_block_desc:
                    st.markdown(f"<div style='color: #9CA3AF; font-size: 0.72rem; margin-bottom: 8px; text-transform: uppercase;'>PAUTA DE DESCANSO: {block.rest_block_desc}</div>", unsafe_allow_html=True)

                for e_idx, ex in enumerate(block.exercises):
                    if block.code == "R":
                        paces = calculate_running_10k_paces(st.session_state["target_10k_time"])
                        with st.expander(f"{ex.name}  •  {ex.target}", expanded=True):
                            st.markdown(
                                f'<div style="color: #10B981; font-weight: 800; font-size: 0.88rem; margin-bottom: 4px;">RITMO SAN SILVESTRE: {paces["intervals_1000m"]}</div>'
                                f'<div style="color: #9CA3AF; font-size: 0.78rem;">{ex.notes if ex.notes else ex.target} • {ex.rest_description}</div>',
                                unsafe_allow_html=True
                            )
                    elif block.code in ["S", "H"] and (ex.exercise_key or ex.intensity_pct or ex.default_weight):
                        base_1rm = user_1rms.get(ex.exercise_key, 100.0) if ex.exercise_key else 100.0
                        num_sets = current_wave["sets"] if block.code == "S" else (ex.target_sets or 3)
                        default_reps = current_wave["reps"] if block.code == "S" else (ex.target_reps or 10)
                        pct_wave = current_wave["pct_wave"]

                        ex_label = f"{ex.name}  •  {ex.target}"
                        
                        with st.expander(ex_label, expanded=(e_idx == 0)):
                            st.markdown(
                                f'<div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 8px;">'
                                f'<span style="color: #9CA3AF; font-size: 0.78rem;">1RM Base: <b style="color: #FF5722;">{base_1rm} kg</b> | {ex.rest_description}</span>'
                                f'</div>',
                                unsafe_allow_html=True
                            )
                            if ex.notes:
                                st.markdown(f"<div style='color: #9CA3AF; font-size: 0.75rem; margin-bottom: 10px;'>• {ex.notes}</div>", unsafe_allow_html=True)

                            # RECORRIDO DE SERIES CON GUARDADO ATÓMICO
                            for s_num in range(1, num_sets + 1):
                                is_saved = (ex.name, s_num) in saved_sets_map
                                saved_data = saved_sets_map.get((ex.name, s_num), {})

                                default_pct = pct_wave[s_num - 1] if (block.code=="S" and s_num <= len(pct_wave)) else (ex.intensity_pct*100 if ex.intensity_pct else 75.0)
                                calc_weight = calculate_target_weight(base_1rm, default_pct / 100.0) if ex.exercise_key else (ex.default_weight or 20.0)

                                # Si ya estaba guardada en BD, usamos sus datos reales
                                current_w = saved_data.get("weight", calc_weight)
                                current_r = saved_data.get("reps", default_reps)
                                current_rpe = saved_data.get("rpe", 8.0)

                                # Cabecera de la serie: muestra [✓ GUARDADA] si ya está en SQLite
                                status_tag = f"✓ GUARDADA: {current_w} KG x {current_r}" if is_saved else f"{default_pct}% 1RM • {calc_weight} KG"
                                set_label = f"SERIE #{s_num}  •  {status_tag}"
                                
                                # Si no está guardada y es la primera pendiente, la abrimos por defecto
                                with st.expander(set_label, expanded=(not is_saved and s_num == 1) or is_saved):
                                    c_w, c_r, c_rpe = st.columns([1.4, 1.2, 1.4])
                                    with c_w:
                                        s_w = st.number_input("Peso (kg)", min_value=0.0, value=float(current_w), step=2.5, key=f"mw_{ex.name}_{s_num}_{st.session_state['current_block_week']}")
                                    with c_r:
                                        s_r = st.number_input("Reps", min_value=1, max_value=30, value=int(current_r), step=1, key=f"mr_{ex.name}_{s_num}_{st.session_state['current_block_week']}")
                                    with c_rpe:
                                        rpe_opts = [6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0]
                                        idx_rpe = rpe_opts.index(float(current_rpe)) if float(current_rpe) in rpe_opts else 4
                                        s_rpe = st.selectbox("RPE", rpe_opts, index=idx_rpe, key=f"mrpe_{ex.name}_{s_num}_{st.session_state['current_block_week']}")
                                    
                                    est_1rm = calculate_estimated_1rm(s_w, s_r)
                                    st.markdown(f"<div style='text-align: right; color: #9CA3AF; font-size: 0.72rem; margin-top: 4px; margin-bottom: 6px;'>1RM ESTIMADO: <b style='color: #10B981;'>{est_1rm} KG</b></div>", unsafe_allow_html=True)

                                    # BOTÓN DE GUARDADO INMEDIATO DE ESTA SERIE EN SQLITE
                                    btn_set_label = "ACTUALIZAR SERIE" if is_saved else f"✓ GUARDAR SERIE #{s_num}"
                                    if st.button(btn_set_label, key=f"btn_save_set_{ex.name}_{s_num}", use_container_width=True, type="primary" if not is_saved else "secondary"):
                                        save_single_set(
                                            date=today_date_str,
                                            day_id=current_day.day_id,
                                            exercise_name=ex.name,
                                            set_num=s_num,
                                            pct_1rm=default_pct,
                                            weight=s_w,
                                            reps=s_r,
                                            rpe=s_rpe,
                                            est_1rm=est_1rm
                                        )
                                        st.toast(f"Serie #{s_num} guardada en marchon.db ✓")
                                        time.sleep(0.5)
                                        st.rerun()

                            rest_mins = (ex.rest_seconds or 120) // 60
                            rest_secs = (ex.rest_seconds or 120) % 60
                            st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
                            if st.button(f"INICIAR DESCANSO ({rest_mins}:{rest_secs:02d})", key=f"btn_t_{ex.name}", use_container_width=True):
                                with st.spinner(f"Descansando {ex.rest_description}..."):
                                    time.sleep(2)
                                    st.toast(f"Tiempo cumplido: {ex.rest_description}")
                    else:
                        with st.expander(f"{ex.name}  •  {ex.target}", expanded=False):
                            notes_with_rest = f"{ex.notes} • {ex.rest_description}" if ex.notes else ex.rest_description
                            st.markdown(f"<div style='color: #9CA3AF; font-size: 0.8rem;'>{notes_with_rest}</div>", unsafe_allow_html=True)

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        sauna_done = st.checkbox("Sauna seca realizada hoy (20-30 min)", key="sauna_check")

        # El botón final solo sella el resumen del día (las series ya están 100% a salvo en SQLite)
        if st.button("FINALIZAR ENTRENAMIENTO COMPLETO", use_container_width=True, type="primary"):
            finalize_session_summary(
                day_id=current_day.day_id,
                date=today_date_str,
                title=current_day.title,
                sauna=sauna_done,
                duration=55
            )
            st.success(f"¡Entrenamiento de {current_day.day_name} finalizado con éxito!")
            time.sleep(1)
            st.rerun()

# -------------------------------------------------------------
# VISTA: HOME
# -------------------------------------------------------------
elif st.session_state["current_view"] == "home":
    st.markdown("<h3 style='color: white; font-weight: 900; text-transform: uppercase;'>Panel de Control</h3>", unsafe_allow_html=True)
    total_sessions = 3 + get_completed_sessions_count()
    render_phase_snapshot(sessions=total_sessions, pbs=2, total_time=f"{total_sessions * 55 // 60}h {total_sessions * 55 % 60}m")
    
    st.markdown("""
    <div style="background: #161922; border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 1rem; margin-top: 1rem;">
        <div style="font-size: 0.9rem; font-weight: 800; color: white; margin-bottom: 0.2rem; text-transform: uppercase;">Estado de Recuperación (Readiness)</div>
        <div style="font-size: 0.72rem; color: #9CA3AF; margin-bottom: 0.5rem;">Autorregulación biológica</div>
    </div>
    """, unsafe_allow_html=True)
    s_val = st.slider("Calidad de Sueño (1-5)", 1, 5, 4, key="h_s")
    e_val = st.slider("Nivel de Energía (1-5)", 1, 5, 4, key="h_e")
    a_val = st.slider("Molestia en Brazo (1=Sin dolor, 5=Alto)", 1, 5, 2, key="h_a")
    if st.button("CALCULAR READINESS", use_container_width=True):
        score = log_readiness("2026-09-07", s_val, e_val, a_val)
        st.session_state["readiness_score"] = score
        st.toast(f"Readiness actualizado a {score}%")

# -------------------------------------------------------------
# VISTA: PROGRAMAS
# -------------------------------------------------------------
elif st.session_state["current_view"] == "programs":
    st.markdown("<h3 style='color: white; font-weight: 900; text-transform: uppercase;'>Programas de Entrenamiento</h3>", unsafe_allow_html=True)
    for prog in PROGRAMS_CATALOG:
        is_current = (prog.id == st.session_state["active_program_id"])
        tags_str = "".join([f'<span class="badge-tag">{t}</span>' for t in prog.tags])
        st.markdown(f"""
        <div style="background: #161922; border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 1rem; margin-bottom: 0.8rem;">
            <span class="badge-tag">{prog.category}</span>
            <h4 style="color: white; margin: 0.3rem 0; font-weight: 800;">{prog.title}</h4>
            <p style="color: #9CA3AF; font-size: 0.82rem; margin-bottom: 0.5rem;">{prog.description}</p>
            {tags_str}
        </div>
        """, unsafe_allow_html=True)
        if not is_current:
            if st.button(f"ACTIVAR {prog.title.split(':')[0]}", key=f"btn_p_{prog.id}", use_container_width=True):
                st.session_state["active_program_id"] = prog.id
                st.session_state["selected_day_idx"] = 0
                st.rerun()

# -------------------------------------------------------------
# VISTA: KPIS
# -------------------------------------------------------------
elif st.session_state["current_view"] == "kpis":
    st.markdown("<h3 style='color: white; font-weight: 900; text-transform: uppercase;'>Progreso & Rendimiento</h3>", unsafe_allow_html=True)
    kpis_data = [
        {"name": "Bench Press", "metric": "1RM Actual", "baseline": f"{user_1rms.get('bench_press', 120)*0.95:.1f} kg", "retest": f"{
@'
import sqlite3
import pandas as pd
from typing import Dict, Any, List, Tuple

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
    
    # 2. Tabla de Series con Clave Única (Para que nunca se pierda ni duplique una serie)
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
        logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(date, day_id, exercise_name, set_number)
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

    # 4. Tabla de Readiness Diario
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

def save_single_set(date: str, day_id: str, exercise_name: str, set_num: int, pct_1rm: float, weight: float, reps: int, rpe: float, est_1rm: float):
    """Guarda una serie individual inmediatamente en SQLite"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO exercise_set_logs (date, day_id, exercise_name, set_number, pct_1rm, weight, reps, rpe, est_1rm, logged_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """, (date, day_id, exercise_name, set_num, pct_1rm, weight, reps, rpe, est_1rm))
    conn.commit()
    conn.close()

def get_day_logged_sets(date: str, day_id: str) -> Dict[Tuple[str, int], Dict[str, Any]]:
    """Obtiene todas las series ya guardadas de ese día para no perderlas al recargar"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT exercise_name, set_number, pct_1rm, weight, reps, rpe, est_1rm
    FROM exercise_set_logs
    WHERE date = ? AND day_id = ?
    """, (date, day_id))
    rows = cursor.fetchall()
    conn.close()
    
    logged_map = {}
    for r in rows:
        logged_map[(r[0], r[1])] = {
            "pct_1rm": r[2], "weight": r[3], "reps": r[4], "rpe": r[5], "est_1rm": r[6]
        }
    return logged_map

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

def finalize_session_summary(day_id: str, date: str, title: str, sauna: bool = False, duration: int = 55):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Calcular volumen total del día directamente de las series guardadas
    cursor.execute("SELECT SUM(weight * reps) FROM exercise_set_logs WHERE date = ? AND day_id = ?", (date, day_id))
    res = cursor.fetchone()[0]
    total_volume = res if res else 0.0
    
    cursor.execute("""
    INSERT INTO completed_sessions (day_id, date, session_title, total_volume_kg, duration_minutes, sauna_completed)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (day_id, date, title, total_volume, duration, sauna))
    
    conn.commit()
    conn.close()

def log_readiness(date: str, sleep: int, energy: int, arm_soreness: int) -> int:
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
