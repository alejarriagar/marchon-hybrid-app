import streamlit as st
from src.ui.styles import apply_custom_styles
from src.ui.components import render_top_bar, render_phase_snapshot, render_kpi_table, render_exercise_item
from src.database.repository import init_db, log_session, get_completed_sessions_count
from src.seed_data import SEPTEMBER_PROGRAM, PROGRAMS_CATALOG

init_db()

st.set_page_config(
    page_title="MARCHON Hybrid OS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

apply_custom_styles()

if "selected_day_idx" not in st.session_state:
    st.session_state["selected_day_idx"] = 0
if "current_view" not in st.session_state:
    st.session_state["current_view"] = "plan"

# 1. Barra Superior con navegación
render_top_bar(program_name="PERFORM • Fase 1 (Septiembre Cimentación)", streak_days=4 + get_completed_sessions_count())

nav_c1, nav_c2, nav_c3 = st.columns([1, 1, 1])
with nav_c1:
    if st.button("📅 PLAN SEMANAL", use_container_width=True):
        st.session_state["current_view"] = "plan"
with nav_c2:
    if st.button("🧭 EXPLORAR PROGRAMAS", use_container_width=True):
        st.session_state["current_view"] = "explore"
with nav_c3:
    if st.button("📊 PROGRESO & KPIS", use_container_width=True):
        st.session_state["current_view"] = "kpis"

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# VISTA 1: PLAN SEMANAL
# -------------------------------------------------------------
if st.session_state["current_view"] == "plan":
    st.markdown("<div style='font-size: 0.8rem; font-weight: 700; color: #9CA3AF; text-transform: uppercase; margin-bottom: 0.4rem;'>SEMANA 1 (7 - 13 SEPTIEMBRE)</div>", unsafe_allow_html=True)
    cols_cal = st.columns(7)
    
    for idx, day in enumerate(SEPTEMBER_PROGRAM):
        with cols_cal[idx]:
            label = f"{day.day_name} {day.date_num}\n{day.type_badge}"
            if st.button(label, key=f"cal_btn_{idx}", use_container_width=True):
                st.session_state["selected_day_idx"] = idx
                st.rerun()

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    current_day = SEPTEMBER_PROGRAM[st.session_state["selected_day_idx"]]

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
            f'<div style="text-align: right;"><span class="badge-green">{current_day.day_name} {current_day.date_num} Sept</span></div>'
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
                        if block.code == "S" and ex.default_weight:
                            c1, c2, c3 = st.columns([3, 2, 2])
                            with c1:
                                st.markdown(f"<div style='color: white; font-weight: 700; margin-top: 5px;'>{ex.name}</div><div style='color: #9CA3AF; font-size: 0.75rem;'>{ex.target}</div>", unsafe_allow_html=True)
                            with c2:
                                st.number_input(f"Peso (kg)", min_value=0.0, value=ex.default_weight, step=2.5, key=f"w_{ex.name}")
                            with c3:
                                st.selectbox(f"RPE", [7.0, 7.5, 8.0, 8.5, 9.0], index=2, key=f"rpe_{ex.name}")
                        else:
                            render_exercise_item(name=ex.name, target=ex.target, notes=ex.notes)

            if st.button("🔥 COMPLETAR Y GUARDAR ESTA SESIÓN", use_container_width=True):
                sauna_checked = st.session_state.get("sauna_check", False)
                log_session(day_id=current_day.day_id, date=f"2026-09-{current_day.date_num.zfill(2)}", duration=55, sauna=sauna_checked)
                st.success(f"¡Sesión de {current_day.day_name} registrada en la base de datos! 🔥")

    with col_sidebar:
        total_sessions = 3 + get_completed_sessions_count()
        render_phase_snapshot(sessions=total_sessions, pbs=2, total_time=f"{total_sessions * 55 // 60}h {total_sessions * 55 % 60}m")
        
        kpis_data = [
            {"name": "Bench Press", "metric": "5 RM Weight", "baseline": "115 kg", "retest": "120 kg", "delta": "+4.3%"},
            {"name": "Weighted Chin-up", "metric": "5 RM Lastre", "baseline": "+15 kg", "retest": "+20 kg", "delta": "+33%"},
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
    st.markdown("<p style='color: #9CA3AF;'>Elige un programa especializado según tu objetivo del mes</p>", unsafe_allow_html=True)
    for prog in PROGRAMS_CATALOG:
        active_badge = '<span class="badge-green">✓ ACTIVO</span>' if prog.is_active else '<span class="badge-tag">DISPONIBLE</span>'
        tags_str = "".join([f'<span class="badge-tag">{t}</span>' for t in prog.tags])
        st.markdown(
            f'<div class="marchon-card">'
            f'<div style="display: flex; justify-content: space-between; align-items: flex-start;">'
            f'<div><span class="badge-kpi" style="margin-bottom: 0.3rem;">{prog.category}</span>'
            f'<h3 style="color: white; margin: 0.3rem 0; font-weight: 800;">{prog.title}</h3>'
            f'<p style="color: #9CA3AF; font-size: 0.85rem; margin-bottom: 0.5rem;">{prog.description}</p>{tags_str}</div>'
            f'<div>{active_badge}</div>'
            f'</div></div>',
            unsafe_allow_html=True
        )

# -------------------------------------------------------------
# VISTA 3: PROGRESO Y KPIS
# -------------------------------------------------------------
elif st.session_state["current_view"] == "kpis":
    st.markdown("<h2 style='color: white; font-weight: 800;'>Progreso & Test de Rendimiento (KPIs)</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #9CA3AF;'>Métricas clave testadas al inicio y al final de la Fase 1</p>", unsafe_allow_html=True)
    render_phase_snapshot(sessions=3 + get_completed_sessions_count(), pbs=2, total_time="3h 33m")
    kpis_data = [
        {"name": "Barbell Bench Press", "metric": "5 RM Weight", "baseline": "115 kg", "retest": "120 kg", "delta": "+4.3%"},
        {"name": "Weighted Chin-up", "metric": "5 RM Lastre", "baseline": "+15 kg", "retest": "+20 kg", "delta": "+33.3%"},
        {"name": "Trap Bar Deadlift", "metric": "3 RM Weight", "baseline": "140 kg", "retest": "152.5 kg", "delta": "+8.9%"},
        {"name": "San Silvestre 10k (Series 1000m)", "metric": "Ritmo Umbral", "baseline": "4:45 min/km", "retest": "4:28 min/km", "delta": "+6.0%"},
        {"name": "Fondo en Bici (1h Z2)", "metric": "Potencia / FC Media", "baseline": "142 bpm", "retest": "134 bpm", "delta": "+5.6% eficiencia"}
    ]
    render_kpi_table(kpis_data)
