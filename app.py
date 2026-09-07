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

# Cargar 1RMs actuales del usuario
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
# VISTA 1: PLAN SEMANAL CON % 1RM CALCULADO EN TIEMPO REAL
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

    col_workout, col_sidebar = st.columns([6.5, 3.5])

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
                expander_label = f"{block.code}  •  {block.title} ({block.subtitle})"
                with st.expander(expander_label, expanded=True):
                    for ex in block.exercises:
                        if block.code == "S" and (ex.intensity_pct or ex.default_weight):
                            # Calcular peso objetivo según 1RM
                            base_1rm = user_1rms.get(ex.exercise_key, 100.0) if ex.exercise_key else 100.0
                            calculated_target_w = calculate_target_weight(base_1rm, ex.intensity_pct) if ex.intensity_pct else ex.default_weight
                            pct_label = f" ({int(ex.intensity_pct*100)}% de tu 1RM: {base_1rm} kg)" if ex.intensity_pct else ""

                            st.markdown(f"<div style='color: white; font-weight: 700; font-size: 1rem; margin-top: 10px;'>{ex.name}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div style='color: #10B981; font-weight: 600; font-size: 0.8rem; margin-bottom: 10px;'>🎯 Peso Sugerido: {calculated_target_w} kg{pct_label}</div>", unsafe_allow_html=True)
                            
                            num_sets = ex.target_sets or 4
                            cols_head = st.columns([1, 2, 2, 2, 1.5])
                            cols_head[0].markdown("<span style='color:#9CA3AF; font-size:0.75rem; font-weight:700;'>SET</span>", unsafe_allow_html=True)
                            cols_head[1].markdown("<span style='color:#9CA3AF; font-size:0.75rem; font-weight:700;'>PESO (KG)</span>", unsafe_allow_html=True)
                            cols_head[2].markdown("<span style='color:#9CA3AF; font-size:0.75rem; font-weight:700;'>REPS</span>", unsafe_allow_html=True)
                            cols_head[3].markdown("<span style='color:#9CA3AF; font-size:0.75rem; font-weight:700;'>RPE</span>", unsafe_allow_html=True)
                            cols_head[4].markdown("<span style='color:#9CA3AF; font-size:0.75rem; font-weight:700;'>EST. 1RM</span>", unsafe_allow_html=True)

                            for s_num in range(1, num_sets + 1):
                                sc = st.columns([1, 2, 2, 2, 1.5])
                                sc[0].markdown(f"<div style='color: white; font-weight: 800; margin-top: 8px;'>#{s_num}</div>", unsafe_allow_html=True)
                                s_w = sc[1].number_input(f"W_{s_num}", min_value=0.0, value=calculated_target_w, step=2.5, key=f"w_{ex.name}_{s_num}", label_visibility="collapsed")
                                s_r = sc[2].number_input(f"R_{s_num}", min_value=1, max_value=30, value=ex.target_reps or 5, step=1, key=f"r_{ex.name}_{s_num}", label_visibility="collapsed")
                                s_rpe = sc[3].selectbox(f"RPE_{s_num}", [7.0, 7.5, 8.0, 8.5, 9.0], index=2, key=f"rpe_{ex.name}_{s_num}", label_visibility="collapsed")
                                
                                est_1rm = calculate_estimated_1rm(s_w, s_r)
                                sc[4].markdown(f"<div style='color: #10B981; font-weight: 800; margin-top: 8px;'>{est_1rm} kg</div>", unsafe_allow_html=True)
                            
                            st.markdown("<hr style='border: 0.5px solid rgba(255,255,255,0.06); margin: 15px 0;'>", unsafe_allow_html=True)
                        else:
                            render_exercise_item(name=ex.name, target=ex.target, notes=ex.notes)

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            t_col1, t_col2 = st.columns([1, 3])
            with t_col1:
                if st.button("⏱️ DESCANSO 2:00", use_container_width=True):
                    with st.spinner("⏳ Descansando 2 minutos..."):
                        time.sleep(2)
                        st.toast("¡Tiempo de descanso cumplido! A por la siguiente serie 💪")

            if st.button("🔥 COMPLETAR Y GUARDAR ESTA SESIÓN", use_container_width=True):
                sauna_checked = st.session_state.get("sauna_check", False)
                log_session(day_id=current_day.day_id, date=f"2026-09-{current_day.date_num.zfill(2)}", duration=55, sauna=sauna_checked)
                st.success(f"¡Sesión de {current_day.day_name} registrada en la base de datos! 🔥")

    with col_sidebar:
        total_sessions = 3 + get_completed_sessions_count()
        render_phase_snapshot(sessions=total_sessions, pbs=2, total_time=f"{total_sessions * 55 // 60}h {total_sessions * 55 % 60}m")
        
        kpis_data = [
            {"name": "Bench Press", "metric": "5 RM Weight", "baseline": f"{user_1rms.get('bench_press', 120)*0.85:.1f} kg", "retest": f"{user_1rms.get('bench_press', 120)} kg (1RM)", "delta": "+4.3%"},
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
