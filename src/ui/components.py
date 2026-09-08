import streamlit as st

def check_pin_auth(default_pin="6367") -> bool:
    if st.session_state.get("authenticated", False):
        return True

    _, col_center, _ = st.columns([1, 1.6, 1])
    with col_center:
        st.markdown("""
        <div style="text-align: center; margin-top: 4rem; margin-bottom: 1.5rem;">
            <div style="background: #FF5722; width: 44px; height: 44px; border-radius: 8px; display: inline-flex; align-items: center; justify-content: center; font-weight: 900; color: white; font-size: 1.5rem; margin-bottom: 1rem;">M</div>
            <h3 style="color: white; font-weight: 900; margin-bottom: 0.2rem; text-transform: uppercase; letter-spacing: 0.5px;">MARCHON HYBRID OS</h3>
            <p style="color: #9CA3AF; font-size: 0.8rem;">Introduce tu clave de acceso</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("pin_login_form"):
            pin_input = st.text_input("PIN", type="password", placeholder="PIN", label_visibility="collapsed")
            submit = st.form_submit_button("DESBLOQUEAR", use_container_width=True)
            if submit:
                # Lectura blindada: si no hay secrets.toml, usa 'default_pin' directamente
                valid_pin = default_pin
                try:
                    valid_pin = str(st.secrets["APP_PIN"])
                except Exception:
                    valid_pin = default_pin

                if pin_input == valid_pin:
                    st.session_state["authenticated"] = True
                    st.rerun()
                else:
                    st.error("PIN incorrecto")
    return False

def render_top_bar(program_name="PERFORM", streak_days=4):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"""
        <div style="margin-bottom: 0.3rem;">
            <div style="font-size: 0.7rem; color: #9CA3AF; text-transform: uppercase; font-weight: 800; letter-spacing: 0.5px;">SEPTIEMBRE 2026</div>
            <div style="font-size: 1.35rem; font-weight: 900; color: white; letter-spacing: -0.5px;">{program_name}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="text-align: right; margin-top: 5px;">
            <span style="background: #161922; border: 1px solid rgba(255,255,255,0.08); padding: 0.35rem 0.6rem; border-radius: 6px; color: #F59E0B; font-weight: 800; font-size: 0.78rem;">RACHA: {streak_days} DÍAS</span>
        </div>
        """, unsafe_allow_html=True)

def render_phase_snapshot(sessions=3, pbs=2, total_time="3h 33m"):
    st.markdown('<div style="font-size: 0.95rem; font-weight: 800; color: white; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.5px;">Resumen de Fase</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="stat-box"><div class="stat-value">{sessions}</div><div class="stat-label">Sesiones</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat-box"><div class="stat-value" style="color: #FF5722;">{pbs}</div><div class="stat-label">Récords (PB)</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="stat-box"><div class="stat-value">{total_time}</div><div class="stat-label">Tiempo Total</div></div>', unsafe_allow_html=True)

def render_kpi_table(kpis):
    st.markdown('<div style="margin-top: 1.2rem; margin-bottom: 0.4rem;"><div style="font-size: 0.95rem; font-weight: 800; color: white; text-transform: uppercase; letter-spacing: 0.5px;">Progreso de KPIs</div></div>', unsafe_allow_html=True)
    for kpi in kpis:
        st.markdown(
            f'<div style="display: flex; justify-content: space-between; align-items: center; background: #161922; border-bottom: 1px solid rgba(255,255,255,0.06); padding: 0.65rem 0.4rem;">'
            f'<div><span class="badge-kpi" style="margin-right: 0.4rem;">KPI</span>'
            f'<span style="font-weight: 700; color: white; font-size: 0.88rem;">{kpi["name"]}</span>'
            f'<div style="font-size: 0.72rem; color: #9CA3AF; margin-left: 2rem;">{kpi["metric"]}</div></div>'
            f'<div style="text-align: right;"><div style="color: #9CA3AF; font-size: 0.75rem; text-decoration: line-through;">{kpi["baseline"]}</div>'
            f'<div style="color: white; font-weight: 800; font-size: 0.9rem;">{kpi["retest"]} <span class="badge-green">{kpi["delta"]}</span></div></div>'
            f'</div>',
            unsafe_allow_html=True
        )

def render_exercise_item(name: str, target: str, notes: str = None):
    notes_html = f'<div style="font-size: 0.72rem; color: #9CA3AF; margin-top: 2px;">{notes}</div>' if notes else ''
    html = (
        f'<div class="exercise-row">'
        f'<div><div class="exercise-name">{name}</div>{notes_html}</div>'
        f'<span class="exercise-reps">{target}</span>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)
