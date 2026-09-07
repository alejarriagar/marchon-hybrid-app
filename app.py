import streamlit as st
import time
import pandas as pd
import plotly.express as px
from src.ui.styles import apply_custom_styles
from src.ui.components import render_top_bar, render_phase_snapshot, render_kpi_table, render_exercise_item
from src.database.repository import init_db, log_session, get_completed_sessions_count, get_all_user_1rms, update_user_1rm
from src.services.progression import calculate_estimated_1rm, calculate_target_weight
from src.seed_data import SEPTEMBER_PROGRAM, OCTOBER_BJJ_PROGRAM, PROGRAMS_CATALOG

init_db()

st.set_page_config(
    page_title="MARCHON Hybrid OS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

apply_custom_styles()

user_1rms = get_all_user_1rms()

if "active_program_id" not in st.session_state:
    st.session_state["active_program_id"] = "perform_sep"
if "selected_day_idx" not in st.session_state:
    st.session_state["selected_day_idx"] = 0
if "current_view" not in st.session_state:
    st.session_state["current_view"] = "plan"

active_program_data = SEPTEMBER_PROGRAM if st.session_state["active_program_id"] == "perform_sep" else OCTOBER_BJJ_PROGRAM
active_program_title = "FASE 1 (Septiembre Cimentación)" if st.session_state["active_program_id"] == "perform_sep" else "FASE 2 (Octubre + BJJ)"

render_top_bar(program_name=f"PERFORM • {active_program_title}", streak_days=4 + get_completed_sessions_count())

# Selector de Vistas
nav_c1, nav_c2, nav_c3, nav_c4 = st.columns([1, 1, 1, 1])
with nav_c1:
    if st.button("📅 PLAN SEMANAL", use_container_width=True):
        st.session_state["current_view"] = "plan"
with nav_c2:
    if st.button("🧭 EXPLORAR PROGRAMAS", use_container_width=True):
        st.session_state["current_view"] = "explore"
with nav_c3:
    if st.button("📊 PROGRESO & KPIS", use_container_width=True):
        st.session_state["current_view"] = "kpis"
with nav_c4:
    if st.button("⚙️ MIS 1RMs", use_container_width=True):
        st.session_state["current_view"] = "settings_1rm"

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# VISTA 1: PLAN SEMANAL CON TIEMPOS DE DESCANSO VISIBLES
# -------------------------------------------------------------
if st.session_state["current_view"] == "plan":
    st.markdown(f"<div style='font-size: 0.8rem; font-weight: 700; color: #9CA3AF; text-transform: uppercase; margin-bottom: 0.4rem;'>MICROCIELO SEMANAL • {active_program_title}</div>", unsafe_allow_html=True)
    cols_cal = st.columns(7)
    
    for idx, day in enumerate(active_program_data):
        with cols_cal[idx]:
            label = f"{day.day_name} {day.date_num}\n{day.type_badge}"
            if st.button(label, key=f"cal_btn_{idx}", use_container_width=True):
                st.session_state["selected_day_idx"] = idx
                st.rerun()

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    current_day = active_program_data[st.session_state["selected_day_idx"]]

    col_workout, col_sidebar = st.columns([6.8, 3.2])

    with col_workout:
        tags_html = "".join([f'<span class="badge-tag">{t}</span>' for t in current_day.tags])
        kpi_html = ""
        if current_day.kpis:
            kpi_html = f'<div style="display: flex; align-items: center; gap: 0.5rem; margin-top: 0.3rem;"><span class="badge-kpi">KPI</span><span style="color: #E2E8F0; font-size: 0.85rem; font-weight: 600;">{", ".join(current_day.kpis)}</span></div>'

        st.markdown(
            f'<div class="marchon-card">'
            f'<div style="display: flex; justify-content: space-between; align-items: flex-start;">'
            f'<div>{tags_html}<h2 style="color: white; margin: 0.4rem 0; font-size: 1.5rem; font-weight: 800;">{current_day.title}</h2>{kpi_html}</div>'
            f'<div style="text-align: right;"><span class="badge-green">{current_day.day_name} {current_day.date_num}</span></div>'
            f'</div></div>',
            unsafe_allow_html=True
        )

        if current_day.is_rest_day:
            st.markdown(
                '<div class="marchon-card" style="text-align: center; padding: 2.5rem 1rem;">'
                '<div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🧘‍♂️</div>'
                '<h3 style="color: white; font-weight: 800;">Día de Descanso Total & Regeneración</h3>'
                '<p style="color: #9CA3AF; max-width: 500px; margin: 0 auto;">El descanso es donde ocurre la adaptación biológica. Prioriza 8 horas de sueño, buena nutrición y tu sesión de sauna.</p>'
                '</div>',
                unsafe_allow_html=True
            )
        else:
            for block in current_day.blocks:
                rest_info = f" • ⏱️ {block.rest_block_desc}" if block.rest_block_desc else ""
                expander_label = f"{block.code}  •  {block.title} ({block.subtitle}){rest_info}"
                
                with st.expander(expander_label, expanded=True):
                    if block.rest_block_desc:
                        st.markdown(
                            f'<div style="background: rgba(255, 87, 34, 0.08); border-left: 3px solid #FF5722; padding: 0.4rem 0.8rem; border-radius: 4px; font-size: 0.8rem; color: #E2E8F0; margin-bottom: 12px;">'
                            f'⏱️ <b>Pauta de Descanso:</b> {block.rest_block_desc}'
                            f'</div>',
                            unsafe_allow_html=True
                        )

                    for ex in block.exercises:
                        if block.code == "S" and (ex.exercise_key or ex.intensity_pct or ex.default_weight):
                            base_1rm = user_1rms.get(ex.exercise_key, 100.0) if ex.exercise_key else 100.0
                            
                            st.markdown(
                                f'<div style="display: flex; justify-content: space-between; align-items: baseline; margin-top: 10px; margin-bottom: 4px;">'
                                f'<div><span style="color: white; font-weight: 800; font-size: 1.05rem;">{ex.name}</span>'
                                f'<span style="background: #242936; color: #10B981; font-size: 0.75rem; font-weight: 700; padding: 0.2rem 0.5rem; border-radius: 4px; margin-left: 0.6rem;">⏱️ {ex.rest_description}</span></div>'
                                f'<span style="color: #9CA3AF; font-size: 0.8rem;">1RM Base: <b style="color: #FF5722;">{base_1rm} kg</b></span>'
                                f'</div>',
                                unsafe_allow_html=True
                            )
                            if ex.notes:
                                st.markdown(f"<div style='color: #9CA3AF; font-size: 0.78rem; margin-bottom: 10px;'>💡 {ex.notes}</div>", unsafe_allow_html=True)
                            
                            num_sets = ex.target_sets or 4
                            default_reps = ex.target_reps or 5
                            
                            cols_head = st.columns([0.8, 1.8, 2.0, 1.4, 1.4, 1.4])
                            cols_head[0].markdown("<span style='color:#9CA3AF; font-size:0.75rem; font-weight:700;'>SET</span>", unsafe_allow_html=True)
                            cols_head[1].markdown("<span style='color:#9CA3AF; font-size:0.75rem; font-weight:700;'>% 1RM</span>", unsafe_allow_html=True)
                            cols_head[2].markdown("<span style='color:#9CA3AF; font-size:0.75rem; font-weight:700;'>PESO (KG)</span>", unsafe_allow_html=True)
                            cols_head[3].markdown("<span style='color:#9CA3AF; font-size:0.75rem; font-weight:700;'>REPS</span>", unsafe_allow_html=True)
                            cols_head[4].markdown("<span style='color:#9CA3AF; font-size:0.75rem; font-weight:700;'>RPE</span>", unsafe_allow_html=True)
                            cols_head[5].markdown("<span style='color:#9CA3AF; font-size:0.75rem; font-weight:700;'>EST. 1RM</span>", unsafe_allow_html=True)

                            pct_wave_defaults = [72.5, 75.0, 77.5, 80.0] if num_sets >= 4 else [75.0, 77.5, 80.0]

                            for s_num in range(1, num_sets + 1):
                                sc = st.columns([0.8, 1.8, 2.0, 1.4, 1.4, 1.4])
                                sc[0].markdown(f"<div style='color: white; font-weight: 800; margin-top: 8px;'>#{s_num}</div>", unsafe_allow_html=True)
                                
                                default_pct = pct_wave_defaults[s_num - 1] if s_num <= len(pct_wave_defaults) else 77.5
                                pct_options = [60.0, 65.0, 70.0, 72.5, 75.0, 77.5, 80.0, 82.5, 85.0, 87.5, 90.0]
                                idx_pct = pct_options.index(default_pct) if default_pct in pct_options else 5
                                
                                s_pct = sc[1].selectbox(f"Pct_{s_num}", pct_options, index=idx_pct, key=f"pct_{ex.name}_{s_num}", label_visibility="collapsed", format_func=lambda x: f"{x}%")
                                calc_weight = calculate_target_weight(base_1rm, s_pct / 100.0)
                                
                                s_w = sc[2].number_input(f"W_{s_num}", min_value=0.0, value=calc_weight, step=2.5, key=f"w_{ex.name}_{s_num}", label_visibility="collapsed")
                                s_r = sc[3].number_input(f"R_{s_num}", min_value=1, max_value=30, value=default_reps, step=1, key=f"r_{ex.name}_{s_num}", label_visibility="collapsed")
                                s_rpe = sc[4].selectbox(f"RPE_{s_num}", [7.0, 7.5, 8.0, 8.5, 9.0], index=2, key=f"rpe_{ex.name}_{s_num}", label_visibility="collapsed")
                                
                                est_1rm = calculate_estimated_1rm(s_w, s_r)
                                sc[5].markdown(f"<div style='color: #10B981; font-weight: 800; margin-top: 8px;'>{est_1rm} kg</div>", unsafe_allow_html=True)

                            # Temporizador dedicado para este ejercicio pesado
                            rest_mins = (ex.rest_seconds or 120) // 60
                            rest_secs = (ex.rest_seconds or 120) % 60
                            rest_btn_label = f"⏱️ Iniciar Descanso ({rest_mins}:{rest_secs:02d})"
                            
                            c_t1, c_t2 = st.columns([2.5, 4.5])
                            with c_t1:
                                if st.button(rest_btn_label, key=f"btn_t_{ex.name}", use_container_width=True):
                                    with st.spinner(f"⏳ Descansando {ex.rest_description}..."):
                                        time.sleep(2)
                                        st.toast(f"¡Tiempo cumplido ({ex.rest_description})! A por la siguiente serie 💪")

                            st.markdown("<hr style='border: 0.5px solid rgba(255,255,255,0.06); margin: 15px 0;'>", unsafe_allow_html=True)
                        else:
                            notes_with_rest = f"{ex.notes} • ⏱️ {ex.rest_description}" if ex.notes else f"⏱️ {ex.rest_description}"
                            render_exercise_item(name=ex.name, target=ex.target, notes=notes_with_rest)

            if st.button("🔥 COMPLETAR Y GUARDAR ESTA SESIÓN", use_container_width=True):
                sauna_checked = st.session_state.get("sauna_check", False)
                log_session(day_id=current_day.day_id, date=f"2026-09-{current_day.date_num.zfill(2)}", duration=55, sauna=sauna_checked)
                st.success(f"¡Sesión de {current_day.day_name} registrada en la base de datos! 🔥")

    with col_sidebar:
        total_sessions = 3 + get_completed_sessions_count()
        render_phase_snapshot(sessions=total_sessions, pbs=2, total_time=f"{total_sessions * 55 // 60}h {total_sessions * 55 % 60}m")
        
        kpis_data = [
            {"name": "Bench Press", "metric": "1RM Actual", "baseline": f"{user_1rms.get('bench_press', 120)*0.95:.1f} kg", "retest": f"{user_1rms.get('bench_press', 120)} kg", "delta": "+5.2%"},
            {"name": "Back Squat", "metric": "1RM Actual", "baseline": "135 kg", "retest": f"{user_1rms.get('back_squat', 140)} kg", "delta": "+3.7%"},
            {"name": "Trap Bar Deadlift", "metric": "1RM Actual", "baseline": "155 kg", "retest": f"{user_1rms.get('deadlift', 165)} kg", "delta": "+6.4%"},
            {"name": "San Silvestre 10k", "metric": "Ritmo Umbral", "baseline": "4:45/km", "retest": "4:28/km", "delta": "+6.0%"},
        ]
        render_kpi_table(kpis_data)
        
        st.markdown(
            '<div class="marchon-card" style="margin-top: 1.5rem;">'
            '<div style="font-size: 1rem; font-weight: 700; color: white; margin-bottom: 0.3rem;">🧖 Protocolo Sauna & Recuperación</div>'
            '<div style="font-size: 0.75rem; color: #9CA3AF; margin-bottom: 0.5rem;">Aclimatación térmica (expande volumen plasmático)</div>'
            '</div>',
            unsafe_allow_html=True
        )
        st.checkbox("20-30 min Sauna Seca Post-Entreno", key="sauna_check")

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
# VISTA 4: PANEL DE GESTIÓN Y ACTUALIZACIÓN DE 1RMs
# -------------------------------------------------------------
elif st.session_state["current_view"] == "settings_1rm":
    st.markdown("<h2 style='color: white; font-weight: 800;'>⚙️ Gestión de Marcas 1RM del Usuario</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #9CA3AF;'>Introduce tus marcas máximas reales. Todos los entrenamientos calcularán automáticamente los pesos exactos de cada serie según el % programado.</p>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="marchon-card"><h4 style="color: white;">Tren Superior</h4>', unsafe_allow_html=True)
        new_bench = st.number_input("Barbell Bench Press (1RM en kg)", min_value=20.0, max_value=300.0, value=float(user_1rms.get("bench_press", 120.0)), step=2.5)
        new_ohp = st.number_input("Standing Overhead Press (1RM en kg)", min_value=15.0, max_value=200.0, value=float(user_1rms.get("ohp", 70.0)), step=2.5)
        new_pull = st.number_input("Weighted Pull-up (Peso corporal + Lastre en kg)", min_value=40.0, max_value=250.0, value=float(user_1rms.get("pull_up", 100.0)), step=2.5)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="marchon-card"><h4 style="color: white;">Tren Inferior</h4>', unsafe_allow_html=True)
        new_squat = st.number_input("Barbell Back Squat (1RM en kg)", min_value=20.0, max_value=400.0, value=float(user_1rms.get("back_squat", 140.0)), step=2.5)
        new_deadlift = st.number_input("Trap Bar Deadlift (1RM en kg)", min_value=30.0, max_value=450.0, value=float(user_1rms.get("deadlift", 165.0)), step=2.5)
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("💾 GUARDAR NUEVOS 1RMs Y RECALCULAR PLAN", use_container_width=True):
        update_user_1rm("bench_press", new_bench)
        update_user_1rm("ohp", new_ohp)
        update_user_1rm("pull_up", new_pull)
        update_user_1rm("back_squat", new_squat)
        update_user_1rm("deadlift", new_deadlift)
        st.success("¡1RMs actualizados en la base de datos con éxito! Todos los pesos del plan han sido recalculados.")
        time.sleep(1)
        st.rerun()
