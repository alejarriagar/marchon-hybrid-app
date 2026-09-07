import streamlit as st

def check_pin_auth(default_pin="1234") -> bool:
    """Pantalla de bloqueo por PIN con estética Marchon"""
    if st.session_state.get("authenticated", False):
        return True

    st.markdown("""
    <div style="max-width: 420px; margin: 3.5rem auto 1rem auto; text-align: center;">
        <div style="background: #FF5722; width: 50px; height: 50px; border-radius: 12px; display: inline-flex; align-items: center; justify-content: center; font-weight: 900; color: white; font-size: 1.6rem; margin-bottom: 1rem; box-shadow: 0 4px 20px rgba(255, 87, 34, 0.4);">M</div>
        <h2 style="color: white; font-weight: 800; margin-bottom: 0.2rem;">MARCHON Hybrid OS</h2>
        <p style="color: #9CA3AF; font-size: 0.85rem;">Introduce tu PIN de atleta para desbloquear tus métricas</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.8, 1])
    with c2:
        st.markdown('<div class="marchon-card">', unsafe_allow_html=True)
        with st.form("pin_login_form"):
            pin_input = st.text_input("PIN de Seguridad", type="password", placeholder="Introduce tu PIN (ej: 1234)", label_visibility="collapsed")
            submit = st.form_submit_button("🔓 DESBLOQUEAR SISTEMA", use_container_width=True)
            if submit:
                # Comprobar PIN (por defecto 1234 o el configurado en secrets)
                valid_pin = st.secrets.get("APP_PIN", default_pin) if hasattr(st, "secrets") and "APP_PIN" in st.secrets else default_pin
                if pin_input == valid_pin:
                    st.session_state["authenticated"] = True
                    st.toast("¡Acceso concedido! Cargando plan...")
                    st.rerun()
                else:
                    st.error("PIN incorrecto. Inténtalo de nuevo.")
        st.markdown('</div>', unsafe_allow_html=True)
    return False

def render_top_bar(program_name="PERFORM • Fase 1 (Septiembre)", streak_days=4):
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"""
<div style="display: flex; align-items: center; gap: 0.8rem;">
    <div style="background: #FF5722; width: 34px; height: 34px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: 900; color: white;">M</div>
    <div>
        <div style="font-size: 0.75rem; color: #9CA3AF; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px;">Programa Activo</div>
        <div style="font-size: 1.1rem; font-weight: 800; color: white;">{program_name}</div>
    </div>
</div>
""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
<div style="text-align: right; background: #161922; padding: 0.4rem 0.8rem; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08); display: inline-block; float: right;">
    <span style="color: #F59E0B; font-weight: 800; font-size: 1rem;">⚡ {streak_days}</span>
    <span style="color: #9CA3AF; font-size: 0.8rem; font-weight: 600; margin-left: 0.2rem;">días racha</span>
</div>
""", unsafe_allow_html=True)

def render_phase_snapshot(sessions=3, pbs=2, total_time="3h 33m"):
    st.markdown('<div style="font-size: 1.1rem; font-weight: 800; color: white; margin-bottom: 0.75rem;">Phase Snapshot</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="stat-box"><div class="stat-value">{sessions}</div><div class="stat-label">Sesiones</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat-box"><div class="stat-value" style="color: #FF5722;">{pbs}</div><div class="stat-label">Récords (PB)</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="stat-box"><div class="stat-value">{total_time}</div><div class="stat-label">Tiempo Total</div></div>', unsafe_allow_html=True)

def render_kpi_table(kpis):
    st.markdown('<div style="margin-top: 1.5rem; margin-bottom: 0.5rem;"><div style="font-size: 1.1rem; font-weight: 800; color: white;">KPI Progress</div><div style="font-size: 0.75rem; color: #9CA3AF;">Testados al inicio y final de la fase</div></div>', unsafe_allow_html=True)
    for kpi in kpis:
        st.markdown(
            f'<div style="display: flex; justify-content: space-between; align-items: center; background: #161922; border-bottom: 1px solid rgba(255,255,255,0.06); padding: 0.75rem 0.5rem;">'
            f'<div><span class="badge-kpi" style="margin-right: 0.4rem;">KPI</span>'
            f'<span style="font-weight: 700; color: white; font-size: 0.9rem;">{kpi["name"]}</span>'
            f'<div style="font-size: 0.75rem; color: #9CA3AF; margin-left: 2rem;">{kpi["metric"]}</div></div>'
            f'<div style="text-align: right;"><div style="color: #9CA3AF; font-size: 0.8rem; text-decoration: line-through;">{kpi["baseline"]}</div>'
            f'<div style="color: white; font-weight: 800; font-size: 0.95rem;">{kpi["retest"]} <span class="badge-green">{kpi["delta"]}</span></div></div>'
            f'</div>',
            unsafe_allow_html=True
        )

def render_exercise_item(name: str, target: str, notes: str = None):
    notes_html = f'<div style="font-size: 0.75rem; color: #9CA3AF; margin-top: 2px;">{notes}</div>' if notes else ''
    html = (
        f'<div class="exercise-row">'
        f'<div><div class="exercise-name">{name}</div>{notes_html}</div>'
        f'<span class="exercise-reps">{target}</span>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)
