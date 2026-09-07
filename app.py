import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import streamlit as st

st.set_page_config(
    page_title="MARCHON Hybrid OS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

import time
import pandas as pd
import plotly.express as px
from src.ui.styles import apply_custom_styles
from src.ui.components import (
    check_pin_auth, render_top_bar, render_phase_snapshot, 
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

# -------------------------------------------------------------
# BARRERA DE SEGURIDAD (PIN AUTH: 6367)
# -------------------------------------------------------------
if not check_pin_auth(default_pin="6367"):
    st.stop()

user_1rms = get_all_user_1rms()

if "device_mode" not in st.session_state:
    st.session_state["device_mode"] = "mobile"
if "active_program_id" not in st.session_state:
    st.session_state["active_program_id"] = "perform_sep"
if "selected_day_idx" not in st.session_state:
    st.session_state["selected_day_idx"] = 0
if "current_view" not in st.session_state:
    st.session_state["current_view"] = "plan"
if "current_block_week" not in st.session_state:
    st.session_state["current_block_week"] = 1
if "target_10k_time" not in st.session_state:
    st.session_state["target_10k_time"] = 45.0
if "readiness_score" not in st.session_state:
    st.session_state["readiness_score"] = 90

active_program_data = SEPTEMBER_PROGRAM if st.session_state["active_program_id"] == "perform_sep" else OCTOBER_BJJ_PROGRAM
active_program_title = "FASE 1 (Sept)" if st.session_state["active_program_id"] == "perform_sep" else "FASE 2 (Oct + BJJ)"
current_wave = get_week_periodization_wave(st.session_state["current_block_week"])

# Barra superior con selector de modo
top_c1, top_c2 = st.columns([3, 1.5])
with top_c1:
    render_top_bar(program_name=f"PERFORM • {active_program_title}", streak_days=4 + get_completed_sessions_count())
with top_c2:
    mode_text = "💻 Cambiar a Web" if st.session_state["device_mode"] == "mobile" else "📱 Cambiar a Móvil"
    if st.button(mode_text, key="toggle_device_btn", use_container_width=True):
        st.session_state["device_mode"] = "desktop" if st.session_state["device_mode"] == "mobile" else "mobile"
        st.rerun()

# Menú de Navegación
nav_c1, nav_c2, nav_c3, nav_c4, nav_c5 = st.columns(5)
with nav_c1:
    if st.button("📅 PLAN", use_container_width=True):
        st.session_state["current_view"] = "plan"
with nav_c2:
    if st.button("🧭 EXPLORAR", use_container_width=True):
        st.session_state["current_view"] = "explore"
with nav_c3:
    if st.button("📊 KPIS", use_container_width=True):
        st.session_state["current_view"] = "kpis"
with nav_c4:
    if st.button("📜 HISTORIAL", use_container_width=True):
        st.session_state["current_view"] = "history"
with nav_c5:
    if st.button("⚙️ 1RMs", use_container_width=True):
        st.session_state["current_view"] = "settings_1rm"

st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# VISTA 1: PLAN SEMANAL
# -------------------------------------------------------------
if st.session_state["current_view"] == "plan":
    # Selector de Semanas
    w_cols = st.columns(4)
    for w_i in range(1, 5):
        w_name = f"Sem {w_i}: {['Acum.', 'Sobrec.', 'Pico', 'Deload'][w_i-1]}"
        with w_cols[w_i-1]:
            if st.button(w_name, key=f"w_btn_{w_i}", use_container_width=True, type="primary" if st.session_state["current_block_week"]==w_i else "secondary"):
                st.session_state["current_block_week"] = w_i
                st.rerun()

    # Selector de Días Semanales
    cols_cal = st.columns(7)
    for idx, day in enumerate(active_program_data):
        with cols_cal[idx]:
            is_sel = (idx == st.session_state["selected_day_idx"])
            label = f"{day.day_name} {day.date_num}\n{day.type_badge.split(':')[0]}"
            if st.button(label, key=f"cal_btn_{idx}", use_container_width=True, type="primary" if is_sel else "secondary"):
                st.session_state["selected_day_idx"] = idx
                st.rerun()

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    current_day = active_program_data[st.session_state["selected_day_idx"]]

    def render_workout_content():
        tags_html = "".join([f'<span class="badge-tag">{t}</span>' for t in current_day.tags])
        kpi_html = ""
        if current_day.kpis:
            kpi_html = f'<div style="display: flex; align-items: center; gap: 0.4rem; margin-top: 0.3rem;"><span class="badge-kpi">KPI</span><span style="color: #E2E8F0; font-size: 0.8rem; font-weight: 600;">{", ".join(current_day.kpis)}</span></div>'

        st.markdown(
            f'<div class="marchon-card">'
            f'<div style="display: flex; justify-content: space-between; align-items: flex-start;">'
            f'<div>{tags_html}<h3 style="color: white; margin: 0.3rem 0; font-size: 1.3rem; font-weight: 800;">{current_day.title}</h3>{kpi_html}</div>'
            f'<div style="text-align: right;"><span class="badge-green">{current_day.day_name} {current_day.date_num}</span></div>'
            f'</div></div>',
            unsafe_allow_html=True
        )

        sets_to_save = []

        if current_day.is_rest_day:
            st.markdown(
                '<div class="marchon-card" style="text-align: center; padding: 2rem 1rem;">'
                '<div style="font-size: 2.2rem; margin-bottom: 0.5rem;">🧘‍♂️</div>'
                '<h3 style="color: white; font-weight: 800;">Día de Descanso Total & Regeneración</h3>'
                '<p style="color: #9CA3AF; font-size: 0.85rem;">Prioriza 8 horas de sueño, nutrición limpia y sauna.</p>'
                '</div>',
                unsafe_allow_html=True
            )
        else:
            for block in current_day.blocks:
                rest_info = f" • ⏱️ {block.rest_block_desc}" if block.rest_block_desc else ""
                expander_label = f"{block.code}  •  {block.title}{rest_info}"
                
                with st.expander(expander_label, expanded=True):
                    for ex in block.exercises:
                        if block.code == "R":
                            paces = calculate_running_10k_paces(st.session_state["target_10k_time"])
                            st.markdown(
                                f'<div style="background: #1D222E; border-left: 3px solid #10B981; padding: 0.6rem 0.8rem; border-radius: 6px; margin-bottom: 8px;">'
                                f'<div style="color: white; font-weight: 700; font-size: 0.9rem;">{ex.name}</div>'
                                f'<div style="color: #10B981; font-size: 0.8rem; font-weight: 700; margin-top: 2px;">🎯 Ritmo Objetivo: {paces["intervals_1000m"]}</div>'
                                f'<div style="color: #9CA3AF; font-size: 0.75rem; margin-top: 2px;">{ex.notes if ex.notes else ex.target} • ⏱️ {ex.rest_description}</div>'
                                f'</div>',
                                unsafe_allow_html=True
                            )
                        elif block.code == "S" and (ex.exercise_key or ex.intensity_pct or ex.default_weight):
                            base_1rm = user_1rms.get(ex.exercise_key, 100.0) if ex.exercise_key else 100.0
                            
                            st.markdown(
                                f'<div style="display: flex; justify-content: space-between; align-items: baseline; margin-top: 8px; margin-bottom: 2px;">'
                                f'<div><span style="color: white; font-weight: 800; font-size: 0.95rem;">{ex.name}</span>'
                                f'<span style="background: #242936; color: #10B981; font-size: 0.72rem; font-weight: 700; padding: 0.15rem 0.4rem; border-radius: 4px; margin-left: 0.4rem;">⏱️ {ex.rest_description}</span></div>'
                                f'<span style="color: #9CA3AF; font-size: 0.75rem;">1RM: <b style="color: #FF5722;">{base_1rm} kg</b></span>'
                                f'</div>',
                                unsafe_allow_html=True
                            )
                            if ex.notes:
                                st.markdown(f"<div style='color: #9CA3AF; font-size: 0.75rem; margin-bottom: 8px;'>💡 {ex.notes}</div>", unsafe_allow_html=True)
                            
                            num_sets = current_wave["sets"]
                            default_reps = current_wave["reps"]
                            pct_wave = current_wave["pct_wave"]

                            # Renderizado Adaptativo: Móvil (Tarjetas 3 Col) vs Desktop (Tabla 6 Col)
                            if st.session_state["device_mode"] == "mobile":
                                # 📱 MODO MÓVIL: Tarjetas individuales de Serie con 3 inputs amplios
                                for s_num in range(1, num_sets + 1):
                                    default_pct = pct_wave[s_num - 1] if s_num <= len(pct_wave) else pct_wave[-1]
                                    calc_weight = calculate_target_weight(base_1rm, default_pct / 100.0)

                                    st.markdown(f"""
                                    <div class="mobile-set-box">
                                        <div class="mobile-set-header">
                                            <div>
                                                <b style="color: white; font-size: 0.9rem;">SERIE #{s_num}</b>
                                                <span class="badge-tag" style="margin-left: 0.3rem;">{default_pct}% 1RM</span>
                                            </div>
                                            <div>
                                                <span style="color: #10B981; font-weight: 800; font-size: 0.85rem;">🎯 Sugerido: {calc_weight} kg</span>
                                            </div>
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)

                                    c_w, c_r, c_rpe = st.columns([1.5, 1.2, 1.3])
                                    with c_w:
                                        s_w = st.number_input("Peso (kg)", min_value=0.0, value=calc_weight, step=2.5, key=f"mw_{ex.name}_{s_num}_{st.session_state['current_block_week']}")
                                    with c_r:
                                        s_r = st.number_input("Reps", min_value=1, max_value=30, value=default_reps, step=1, key=f"mr_{ex.name}_{s_num}_{st.session_state['current_block_week']}")
                                    with c_rpe:
                                        s_rpe = st.selectbox("RPE", [6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0], index=4, key=f"mrpe_{ex.name}_{s_num}_{st.session_state['current_block_week']}")
                                    
                                    est_1rm = calculate_estimated_1rm(s_w, s_r)
                                    st.markdown(f"<div style='text-align: right; color: #9CA3AF; font-size: 0.72rem; margin-top: -8px; margin-bottom: 8px;'>1RM Estimado: <b style='color: #10B981;'>{est_1rm} kg</b></div>", unsafe_allow_html=True)

                                    sets_to_save.append({
                                        "exercise_name": ex.name,
                                        "set_num": s_num,
                                        "pct_1rm": default_pct,
                                        "weight": s_w,
                                        "reps": s_r,
                                        "rpe": s_rpe,
                                        "est_1rm": est_1rm
                                    })
                            else:
                                # 💻 MODO DESKTOP: Tabla panorámica de 6 columnas
                                cols_head = st.columns([0.8, 1.8, 2.0, 1.4, 1.4, 1.4])
                                cols_head[0].markdown("<span style='color:#9CA3AF; font-size:0.7rem; font-weight:700;'>SET</span>", unsafe_allow_html=True)
                                cols_head[1].markdown("<span style='color:#9CA3AF; font-size:0.7rem; font-weight:700;'>% 1RM</span>", unsafe_allow_html=True)
                                cols_head[2].markdown("<span style='color:#9CA3AF; font-size:0.7rem; font-weight:700;'>PESO</span>", unsafe_allow_html=True)
                                cols_head[3].markdown("<span style='color:#9CA3AF; font-size:0.7rem; font-weight:700;'>REPS</span>", unsafe_allow_html=True)
                                cols_head[4].markdown("<span style='color:#9CA3AF; font-size:0.7rem; font-weight:700;'>RPE</span>", unsafe_allow_html=True)
                                cols_head[5].markdown("<span style='color:#9CA3AF; font-size:0.7rem; font-weight:700;'>1RM</span>", unsafe_allow_html=True)

                                for s_num in range(1, num_sets + 1):
                                    sc = st.columns([0.8, 1.8, 2.0, 1.4, 1.4, 1.4])
                                    sc[0].markdown(f"<div style='color: white; font-weight: 800; margin-top: 8px;'>#{s_num}</div>", unsafe_allow_html=True)
                                    default_pct = pct_wave[s_num - 1] if s_num <= len(pct_wave) else pct_wave[-1]
                                    pct_options = [60.0, 65.0, 70.0, 72.5, 75.0, 77.5, 80.0, 82.5, 85.0, 87.5, 90.0]
                                    idx_pct = pct_options.index(default_pct) if default_pct in pct_options else 5
                                    
                                    s_pct = sc[1].selectbox(f"Pct_{s_num}", pct_options, index=idx_pct, key=f"pct_{ex.name}_{s_num}_{st.session_state['current_block_week']}", label_visibility="collapsed", format_func=lambda x: f"{x}%")
                                    calc_weight = calculate_target_weight(base_1rm, s_pct / 100.0)
                                    
                                    s_w = sc[2].number_input(f"W_{s_num}", min_value=0.0, value=calc_weight, step=2.5, key=f"w_{ex.name}_{s_num}_{st.session_state['current_block_week']}", label_visibility="collapsed")
                                    s_r = sc[3].number_input(f"R_{s_num}", min_value=1, max_value=30, value=default_reps, step=1, key=f"r_{ex.name}_{s_num}_{st.session_state['current_block_week']}", label_visibility="collapsed")
                                    s_rpe = sc[4].selectbox(f"RPE_{s_num}", [6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0], index=4, key=f"rpe_{ex.name}_{s_num}_{st.session_state['current_block_week']}", label_visibility="collapsed")
                                    
                                    est_1rm = calculate_estimated_1rm(s_w, s_r)
                                    sc[5].markdown(f"<div style='color: #10B981; font-weight: 800; margin-top: 8px;'>{est_1rm}</div>", unsafe_allow_html=True)

                                    sets_to_save.append({
                                        "exercise_name": ex.name,
                                        "set_num": s_num,
                                        "pct_1rm": s_pct,
                                        "weight": s_w,
                                        "reps": s_r,
                                        "rpe": s_rpe,
                                        "est_1rm": est_1rm
                                    })

                            # Temporizador de descanso
                            rest_mins = (ex.rest_seconds or 120) // 60
                            rest_secs = (ex.rest_seconds or 120) % 60
                            if st.button(f"⏱️ Iniciar Descanso ({rest_mins}:{rest_secs:02d})", key=f"btn_t_{ex.name}", use_container_width=True):
                                with st.spinner(f"⏳ Descansando {ex.rest_description}..."):
                                    time.sleep(2)
                                    st.toast(f"🔔 ¡Tiempo cumplido ({ex.rest_description})! A por la siguiente serie 💪")

                            st.markdown("<hr style='border: 0.5px solid rgba(255,255,255,0.06); margin: 10px 0;'>", unsafe_allow_html=True)
                        else:
                            notes_with_rest = f"{ex.notes} • ⏱️ {ex.rest_description}" if ex.notes else f"⏱️ {ex.rest_description}"
                            render_exercise_item(name=ex.name, target=ex.target, notes=notes_with_rest)

            # Checkbox de sauna antes de guardar
            sauna_done = st.checkbox("🧖 20-30 min Sauna Realizada Hoy", key="sauna_check")

            if st.button("🔥 COMPLETAR Y GUARDAR SESIÓN", use_container_width=True, type="primary"):
                save_full_session_log(
                    day_id=current_day.day_id,
                    date=f"2026-09-{current_day.date_num.zfill(2)}",
                    title=current_day.title,
                    sets_records=sets_to_save,
                    sauna=sauna_done,
                    duration=55
                )
                st.success(f"¡Sesión de {current_day.day_name} guardada en marchon.db! 🔥")
                time.sleep(1)
                st.rerun()

    # Layout Móvil vs Desktop
    if st.session_state["device_mode"] == "mobile":
        render_workout_content()
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        with st.expander("⚡ Daily Readiness & Recuperación", expanded=False):
            s_val = st.slider("Calidad de Sueño (1-5)", 1, 5, 4, key="m_s")
            e_val = st.slider("Nivel de Energía (1-5)", 1, 5, 4, key="m_e")
            a_val = st.slider("Molestia en Brazo (1-5)", 1, 5, 2, key="m_a")
            if st.button("Calcular Readiness", key="m_btn_readiness", use_container_width=True):
                score = log_readiness(f"2026-09-{current_day.date_num.zfill(2)}", s_val, e_val, a_val)
                st.session_state["readiness_score"] = score
                st.rerun()
    else:
        col_workout, col_sidebar = st.columns([6.8, 3.2])
        with col_workout:
            render_workout_content()
        with col_sidebar:
            st.markdown("""
            <div class="marchon-card">
                <div style="font-size: 0.95rem; font-weight: 800; color: white; margin-bottom: 0.3rem;">⚡ Daily Readiness</div>
                <div style="font-size: 0.75rem; color: #9CA3AF; margin-bottom: 0.6rem;">Check-in de fatiga y autorregulación</div>
            </div>
            """, unsafe_allow_html=True)
            with st.expander("📝 Evaluar Estado de Hoy", expanded=False):
                s_val = st.slider("Calidad de Sueño (1-5)", 1, 5, 4)
                e_val = st.slider("Nivel de Energía (1-5)", 1, 5, 4)
                a_val = st.slider("Molestia en Brazo (1-5)", 1, 5, 2)
                if st.button("Calcular Readiness", use_container_width=True):
                    score = log_readiness(f"2026-09-{current_day.date_num.zfill(2)}", s_val, e_val, a_val)
                    st.session_state["readiness_score"] = score
                    st.rerun()

            total_sessions = 3 + get_completed_sessions_count()
            render_phase_snapshot(sessions=total_sessions, pbs=2, total_time=f"{total_sessions * 55 // 60}h {total_sessions * 55 % 60}m")
            
            kpis_data = [
                {"name": "Bench Press", "metric": "1RM", "baseline": f"{user_1rms.get('bench_press', 120)*0.95:.1f} kg", "retest": f"{user_1rms.get('bench_press', 120)} kg", "delta": "+5.2%"},
                {"name": "Back Squat", "metric": "1RM", "baseline": "135 kg", "retest": f"{user_1rms.get('back_squat', 140)} kg", "delta": "+3.7%"},
                {"name": "Deadlift", "metric": "1RM", "baseline": "155 kg", "retest": f"{user_1rms.get('deadlift', 165)} kg", "delta": "+6.4%"},
                {"name": "San Silvestre 10k", "metric": "1000m", "baseline": "4:45/km", "retest": f"{calculate_running_10k_paces(st.session_state['target_10k_time'])['intervals_1000m']}", "delta": "+6.0%"},
            ]
            render_kpi_table(kpis_data)

# -------------------------------------------------------------
# VISTA 2: EXPLORAR PROGRAMAS
# -------------------------------------------------------------
elif st.session_state["current_view"] == "explore":
    st.markdown("<h2 style='color: white; font-weight: 800;'>Explorar Programas</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #9CA3AF;'>Activa el programa correspondiente según el mes de tu planificación</p>", unsafe_allow_html=True)
    for prog in PROGRAMS_CATALOG:
        is_current_active = (prog.id == st.session_state["active_program_id"])
        tags_str = "".join([f'<span class="badge-tag">{t}</span>' for t in prog.tags])
        
        c_left, c_right = st.columns([4, 1])
        with c_left:
            st.markdown(
                f'<div class="marchon-card">'
                f'<span class="badge-kpi" style="margin-bottom: 0.3rem;">{prog.category}</span>'
                f'<h3 style="color: white; margin: 0.3rem 0; font-weight: 800;">{prog.title}</h3>'
                f'<p style="color: #9CA3AF; font-size: 0.85rem; margin-bottom: 0.5rem;">{prog.description}</p>{tags_str}'
                f'</div>',
                unsafe_allow_html=True
            )
        with c_right:
            st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
            if is_current_active:
                st.markdown('<span class="badge-green" style="font-size: 0.9rem; padding: 0.4rem 0.8rem;">✓ ACTIVO</span>', unsafe_allow_html=True)
            else:
                if st.button("ACTIVAR", key=f"act_{prog.id}", use_container_width=True):
                    st.session_state["active_program_id"] = prog.id
                    st.session_state["selected_day_idx"] = 0
                    st.toast(f"¡Programa {prog.title} activado!")
                    st.rerun()

# -------------------------------------------------------------
# VISTA 3: PROGRESO Y KPIS
# -------------------------------------------------------------
elif st.session_state["current_view"] == "kpis":
    st.markdown("<h2 style='color: white; font-weight: 800;'>Progreso & Test de Rendimiento (KPIs)</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #9CA3AF;'>Métricas clave y distribución de volumen del Atleta Híbrido</p>", unsafe_allow_html=True)
    render_phase_snapshot(sessions=3 + get_completed_sessions_count(), pbs=2, total_time="3h 33m")
    
    col_chart1, col_chart2 = st.columns([1, 1])
    with col_chart1:
        st.markdown("<div style='font-weight: 700; color: white; margin-top: 15px; margin-bottom: 5px;'>📈 Evolución 1RM Estimado (Fuerza)</div>", unsafe_allow_html=True)
        df_strength = pd.DataFrame({
            "Semana": ["Base", "Sem 1", "Sem 2", "Sem 3 (Test)"],
            "Bench Press (kg)": [user_1rms.get("bench_press", 120)-5, user_1rms.get("bench_press", 120)-2.5, user_1rms.get("bench_press", 120), user_1rms.get("bench_press", 120)+2.5],
            "Deadlift (kg)": [user_1rms.get("deadlift", 165)-10, user_1rms.get("deadlift", 165)-5, user_1rms.get("deadlift", 165), user_1rms.get("deadlift", 165)+5],
            "Back Squat (kg)": [user_1rms.get("back_squat", 140)-7.5, user_1rms.get("back_squat", 140)-2.5, user_1rms.get("back_squat", 140), user_1rms.get("back_squat", 140)+5]
        })
        fig_str = px.line(df_strength, x="Semana", y=["Bench Press (kg)", "Deadlift (kg)", "Back Squat (kg)"],
                          color_discrete_sequence=["#FF5722", "#10B981", "#3B82F6"], markers=True)
        fig_str.update_layout(
            paper_bgcolor="#161922", plot_bgcolor="#161922", font_color="#9CA3AF",
            margin=dict(l=20, r=20, t=20, b=20), height=280,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_str, use_container_width=True)

    with col_chart2:
        st.markdown("<div style='font-weight: 700; color: white; margin-top: 15px; margin-bottom: 5px;'>⚡ Balance de Disciplinas (Horas/Semana)</div>", unsafe_allow_html=True)
        disciplinas = ["Gym (Fuerza)", "Running 10k", "Jiu-Jitsu", "Ciclismo Z2"]
        horas = [3.5, 2.0, 3.0, 1.5] if st.session_state["active_program_id"] == "perform_oct_bjj" else [4.5, 2.0, 0.0, 1.5]
        fig_pie = px.pie(names=disciplinas, values=horas,
                         color_discrete_sequence=["#FF5722", "#10B981", "#8B5CF6", "#3B82F6"], hole=0.55)
        fig_pie.update_layout(
            paper_bgcolor="#161922", font_color="#FFFFFF",
            margin=dict(l=10, r=10, t=10, b=10), height=280,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2)
        )
        st.plotly_chart(fig_pie, use_container_width=True)

# -------------------------------------------------------------
# VISTA 4: HISTORIAL DE ENTRENAMIENTOS & EXPORTADOR CSV
# -------------------------------------------------------------
elif st.session_state["current_view"] == "history":
    st.markdown("<h2 style='color: white; font-weight: 800;'>📜 Historial de Sesiones & Base de Datos</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #9CA3AF;'>Registro inmutable de todas las series guardadas en tu base de datos local SQLite.</p>", unsafe_allow_html=True)

    st.markdown("""
    <div class="marchon-card" style="border: 1px solid #10B981; background: rgba(16, 185, 129, 0.05); margin-bottom: 1.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span class="badge-green">ASISTENTE DE PROGRESIÓN</span>
                <h3 style="color: white; margin: 0.3rem 0; font-weight: 800;">¿Has completado el Bloque de Septiembre?</h3>
                <p style="color: #9CA3AF; font-size: 0.85rem; margin: 0;">Aplica automáticamente las ganancias de fuerza de Septiembre y transiciona al programa de Octubre con Jiu-Jitsu.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c_trans1, c_trans2 = st.columns([3, 1])
    with c_trans1:
        st.markdown(f"""
        <div style="background: #161922; padding: 1rem; border-radius: 8px; border: 1px solid rgba(255,255,255,0.06);">
            <div style="color: white; font-weight: 700; margin-bottom: 6px;">Nuevas Marcas Proyectadas para Octubre (+2.5 a +5 kg de sobrecarga):</div>
            <div style="font-size: 0.85rem; color: #9CA3AF;">• Bench Press: <b>{user_1rms.get('bench_press', 120)+2.5} kg</b> (Anterior: {user_1rms.get('bench_press', 120)} kg)</div>
            <div style="font-size: 0.85rem; color: #9CA3AF;">• Back Squat: <b>{user_1rms.get('back_squat', 140)+5.0} kg</b> (Anterior: {user_1rms.get('back_squat', 140)} kg)</div>
            <div style="font-size: 0.85rem; color: #9CA3AF;">• Deadlift: <b>{user_1rms.get('deadlift', 165)+7.5} kg</b> (Anterior: {user_1rms.get('deadlift', 165)} kg)</div>
            <div style="font-size: 0.85rem; color: #9CA3AF;">• Overhead Press: <b>{user_1rms.get('ohp', 70)+2.5} kg</b> (Anterior: {user_1rms.get('ohp', 70)} kg)</div>
        </div>
        """, unsafe_allow_html=True)
    with c_trans2:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        if st.button("🚀 APLICAR Y ACTIVAR OCTUBRE", use_container_width=True, type="primary"):
            update_user_1rm("bench_press", user_1rms.get('bench_press', 120)+2.5)
            update_user_1rm("back_squat", user_1rms.get('back_squat', 140)+5.0)
            update_user_1rm("deadlift", user_1rms.get('deadlift', 165)+7.5)
            update_user_1rm("ohp", user_1rms.get('ohp', 70)+2.5)
            st.session_state["active_program_id"] = "perform_oct_bjj"
            st.session_state["selected_day_idx"] = 0
            st.toast("¡Octubre activado con las nuevas marcas de 1RM! 🔥")
            st.rerun()

    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
    
    df_export = export_all_logs_dataframe()
    if not df_export.empty:
        csv_data = df_export.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 EXPORTAR TODAS LAS SERIES A CSV (EXCEL)",
            data=csv_data,
            file_name="marchon_training_logs.csv",
            mime="text/csv"
        )
    
    st.markdown("<h4 style='color: white; font-weight: 800; margin-top: 15px;'>Últimas Sesiones Guardadas</h4>", unsafe_allow_html=True)
    
    history_logs = get_recent_workout_history(limit=15)
    if not history_logs:
        st.info("Aún no has guardado sesiones. Cuando completes un entrenamiento en el Plan Semanal, aparecerá aquí con sus series y volumen.")
    else:
        for log in history_logs:
            sauna_icon = "🧖 Sauna Realizada" if log["sauna"] else "Sin Sauna"
            st.markdown(f"""
            <div class="marchon-card" style="margin-bottom: 0.6rem; padding: 0.8rem 1.2rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="color: #9CA3AF; font-size: 0.75rem; font-weight: 700;">{log['date']}</div>
                        <div style="color: white; font-weight: 800; font-size: 1.05rem;">{log['title']}</div>
                    </div>
                    <div style="text-align: right;">
                        <span style="color: #10B981; font-weight: 800; font-size: 0.95rem;">{log['volume_kg']} kg levantados</span>
                        <div style="color: #9CA3AF; font-size: 0.75rem;">⏱️ {log['duration']} min • {sauna_icon}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# -------------------------------------------------------------
# VISTA 5: PANEL DE GESTIÓN DE 1RMs Y SEGURIDAD
# -------------------------------------------------------------
elif st.session_state["current_view"] == "settings_1rm":
    st.markdown("<h2 style='color: white; font-weight: 800;'>⚙️ Gestión de Marcas 1RM & Seguridad</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #9CA3AF;'>Personaliza tu perfil de atleta. Las cargas del gimnasio y los ritmos de carrera se sincronizan en tiempo real.</p>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="marchon-card"><h4 style="color: white;">🏋️‍♂️ 1RMs de Fuerza (kg)</h4>', unsafe_allow_html=True)
        new_bench = st.number_input("Barbell Bench Press (1RM en kg)", min_value=20.0, max_value=300.0, value=float(user_1rms.get("bench_press", 120.0)), step=2.5)
        new_ohp = st.number_input("Standing Overhead Press (1RM en kg)", min_value=15.0, max_value=200.0, value=float(user_1rms.get("ohp", 70.0)), step=2.5)
        new_squat = st.number_input("Barbell Back Squat (1RM en kg)", min_value=20.0, max_value=400.0, value=float(user_1rms.get("back_squat", 140.0)), step=2.5)
        new_deadlift = st.number_input("Trap Bar Deadlift (1RM en kg)", min_value=30.0, max_value=450.0, value=float(user_1rms.get("deadlift", 165.0)), step=2.5)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="marchon-card"><h4 style="color: white;">🏃‍♂️ San Silvestre Vallecana 10k</h4>', unsafe_allow_html=True)
        target_10k = st.number_input("Objetivo 10k (Tiempo en minutos)", min_value=30.0, max_value=75.0, value=float(st.session_state["target_10k_time"]), step=0.5)
        st.session_state["target_10k_time"] = target_10k
        
        paces = calculate_running_10k_paces(target_10k)
        st.markdown(f"""
        <div style="background: #1D222E; padding: 0.75rem; border-radius: 8px; margin-top: 10px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                <span style="color: #9CA3AF; font-size: 0.85rem;">Ritmo Carrera 10k:</span>
                <span style="color: white; font-weight: 800;">{paces['race_pace']}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                <span style="color: #9CA3AF; font-size: 0.85rem;">Series 1000m (Martes):</span>
                <span style="color: #10B981; font-weight: 800;">{paces['intervals_1000m']}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                <span style="color: #9CA3AF; font-size: 0.85rem;">Tirada Z2 (Sábado/Bici):</span>
                <span style="color: #3B82F6; font-weight: 800;">{paces['z2_easy']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    c_b1, c_b2 = st.columns([3, 1])
    with c_b1:
        if st.button("💾 GUARDAR TODOS LOS PARÁMETROS", use_container_width=True):
            update_user_1rm("bench_press", new_bench)
            update_user_1rm("ohp", new_ohp)
            update_user_1rm("back_squat", new_squat)
            update_user_1rm("deadlift", new_deadlift)
            st.success("¡Perfil y marcas actualizadas! Plan totalmente sincronizado.")
            time.sleep(1)
            st.rerun()
    with c_b2:
        if st.button("🔒 CERRAR SESIÓN", use_container_width=True):
            st.session_state["authenticated"] = False
            st.rerun()
