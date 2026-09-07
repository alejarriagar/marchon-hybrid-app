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
    init_db, save_full_session_log, get_completed_sessions_count, 
    get_all_user_1rms, update_user_1rm, get_recent_workout_history,
    log_readiness, export_all_logs_dataframe
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
# 1. TIRA HORIZONTAL DE CALENDARIO (SCROLL FORZADO EN MÓVIL)
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

# -------------------------------------------------------------
# 2. CABECERA MARCHON (TODAY + PROGRAMAS + SUBTABS)
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
# VISTA: WORKOUT CON 3 NIVELES COLAPSABLES (BLOQUE -> EJERCICIO -> SERIES)
# -------------------------------------------------------------
if st.session_state["current_view"] == "workout":
    sets_to_save = []

    if current_day.is_rest_day:
        st.markdown(
            '<div style="background: #161922; border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; text-align: center; padding: 2.5rem 1rem;">'
            '<h4 style="color: white; font-weight: 900; text-transform: uppercase;">DESCANSO TOTAL & REGENERACIÓN</h4>'
            '<p style="color: #9CA3AF; font-size: 0.85rem; margin-top: 0.4rem;">Prioriza 8 horas de sueño, nutrición limpia y sesión de sauna.</p>'
            '</div>',
            unsafe_allow_html=True
        )
    else:
        # NIVEL 1: BLOQUES COLAPSABLES CON CÓDIGO DE COLOR
        for b_idx, block in enumerate(current_day.blocks):
            block_code_lower = block.code.lower()
            block_label = f"[{block.code}]  {block.title.upper()} ({block.subtitle})"
            
            with st.expander(block_label, expanded=(b_idx == 0 or b_idx == 1)):
                if block.rest_block_desc:
                    st.markdown(f"<div style='color: #9CA3AF; font-size: 0.72rem; margin-bottom: 8px; text-transform: uppercase;'>PAUTA DE DESCANSO: {block.rest_block_desc}</div>", unsafe_allow_html=True)

                # NIVEL 2: EJERCICIOS INDIVIDUALES COLAPSABLES
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

                            # NIVEL 3: CADA SERIE INDIVIDUALMENTE COLAPSABLE
                            for s_num in range(1, num_sets + 1):
                                default_pct = pct_wave[s_num - 1] if (block.code=="S" and s_num <= len(pct_wave)) else (ex.intensity_pct*100 if ex.intensity_pct else 75.0)
                                calc_weight = calculate_target_weight(base_1rm, default_pct / 100.0) if ex.exercise_key else (ex.default_weight or 20.0)

                                set_label = f"SERIE #{s_num}  •  {default_pct}% 1RM  •  {calc_weight} KG"
                                
                                with st.expander(set_label, expanded=(s_num == 1)):
                                    c_w, c_r, c_rpe = st.columns([1.4, 1.2, 1.4])
                                    with c_w:
                                        s_w = st.number_input("Peso (kg)", min_value=0.0, value=calc_weight, step=2.5, key=f"mw_{ex.name}_{s_num}_{st.session_state['current_block_week']}")
                                    with c_r:
                                        s_r = st.number_input("Reps", min_value=1, max_value=30, value=default_reps, step=1, key=f"mr_{ex.name}_{s_num}_{st.session_state['current_block_week']}")
                                    with c_rpe:
                                        s_rpe = st.selectbox("RPE", [6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0], index=4, key=f"mrpe_{ex.name}_{s_num}_{st.session_state['current_block_week']}")
                                    
                                    est_1rm = calculate_estimated_1rm(s_w, s_r)
                                    st.markdown(f"<div style='text-align: right; color: #9CA3AF; font-size: 0.72rem; margin-top: 4px;'>1RM ESTIMADO: <b style='color: #10B981;'>{est_1rm} KG</b></div>", unsafe_allow_html=True)

                                    sets_to_save.append({
                                        "exercise_name": ex.name, "set_num": s_num, "pct_1rm": default_pct,
                                        "weight": s_w, "reps": s_r, "rpe": s_rpe, "est_1rm": est_1rm
                                    })

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

        if st.button("GUARDAR SESIÓN", use_container_width=True, type="primary"):
            save_full_session_log(
                day_id=current_day.day_id, date=f"2026-09-{current_day.date_num.zfill(2)}",
                title=current_day.title, sets_records=sets_to_save, sauna=sauna_done, duration=55
            )
            st.success(f"Sesión de {current_day.day_name} registrada con éxito.")
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
        {"name": "Bench Press", "metric": "1RM Actual", "baseline": f"{user_1rms.get('bench_press', 120)*0.95:.1f} kg", "retest": f"{user_1rms.get('bench_press', 120)} kg", "delta": "+5.2%"},
        {"name": "Back Squat", "metric": "1RM Actual", "baseline": "135 kg", "retest": f"{user_1rms.get('back_squat', 140)} kg", "delta": "+3.7%"},
        {"name": "Deadlift", "metric": "1RM Actual", "baseline": "155 kg", "retest": f"{user_1rms.get('deadlift', 165)} kg", "delta": "+6.4%"},
        {"name": "San Silvestre 10k", "metric": "Ritmo Umbral", "baseline": "4:45/km", "retest": f"{calculate_running_10k_paces(st.session_state['target_10k_time'])['intervals_1000m']}", "delta": "+6.0%"},
    ]
    render_kpi_table(kpis_data)

# -------------------------------------------------------------
# VISTA: ACCOUNT
# -------------------------------------------------------------
elif st.session_state["current_view"] == "account":
    st.markdown("<h3 style='color: white; font-weight: 900; text-transform: uppercase;'>Perfil de Marcas 1RM</h3>", unsafe_allow_html=True)
    new_bench = st.number_input("Bench Press (1RM kg)", min_value=20.0, value=float(user_1rms.get("bench_press", 120.0)), step=2.5)
    new_ohp = st.number_input("Overhead Press (1RM kg)", min_value=15.0, value=float(user_1rms.get("ohp", 70.0)), step=2.5)
    new_squat = st.number_input("Back Squat (1RM kg)", min_value=20.0, value=float(user_1rms.get("back_squat", 140.0)), step=2.5)
    new_deadlift = st.number_input("Deadlift (1RM kg)", min_value=30.0, value=float(user_1rms.get("deadlift", 165.0)), step=2.5)
    target_10k = st.number_input("Objetivo San Silvestre 10k (min)", min_value=30.0, value=float(st.session_state["target_10k_time"]), step=0.5)

    if st.button("GUARDAR 1RMs", use_container_width=True, type="primary"):
        update_user_1rm("bench_press", new_bench)
        update_user_1rm("ohp", new_ohp)
        update_user_1rm("back_squat", new_squat)
        update_user_1rm("deadlift", new_deadlift)
        st.session_state["target_10k_time"] = target_10k
        st.success("Marcas actualizadas correctamente.")
        time.sleep(1)
        st.rerun()

    if st.button("CERRAR SESIÓN", use_container_width=True):
        st.session_state["authenticated"] = False
        st.rerun()

# -------------------------------------------------------------
# BARRA INFERIOR DE NAVEGACIÓN
# -------------------------------------------------------------
st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
bot_c1, bot_c2, bot_c3, bot_c4, bot_c5 = st.columns(5)
with bot_c1:
    if st.button("HOME", key="bot_home", use_container_width=True, type="primary" if st.session_state["current_view"]=="home" else "secondary"):
        st.session_state["current_view"] = "home"
        st.rerun()
with bot_c2:
    if st.button("WORKOUT", key="bot_workout", use_container_width=True, type="primary" if st.session_state["current_view"]=="workout" else "secondary"):
        st.session_state["current_view"] = "workout"
        st.rerun()
with bot_c3:
    if st.button("PROGRAMS", key="bot_progs", use_container_width=True, type="primary" if st.session_state["current_view"]=="programs" else "secondary"):
        st.session_state["current_view"] = "programs"
        st.rerun()
with bot_c4:
    if st.button("KPIS", key="bot_kpis", use_container_width=True, type="primary" if st.session_state["current_view"]=="kpis" else "secondary"):
        st.session_state["current_view"] = "kpis"
        st.rerun()
with bot_c5:
    if st.button("ACCOUNT", key="bot_account", use_container_width=True, type="primary" if st.session_state["current_view"]=="account" else "secondary"):
        st.session_state["current_view"] = "account"
        st.rerun()
