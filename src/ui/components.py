import hmac
from typing import Dict, List, Optional

import streamlit as st


def _configured_pin() -> Optional[str]:
    try:
        return str(st.secrets["APP_PIN"]).strip()
    except Exception:
        return None


def check_pin_auth() -> bool:
    if st.session_state.get("authenticated", False):
        return True

    st.markdown(
        '<div style="text-align:center;margin-top:3rem;margin-bottom:1.2rem;">'
        '<div style="background:#FF5722;width:44px;height:44px;border-radius:8px;display:inline-flex;'
        'align-items:center;justify-content:center;font-weight:900;color:white;font-size:1.5rem;">M</div>'
        '<h3 style="color:white;font-weight:900;margin:0.8rem 0 0.2rem 0;letter-spacing:0.5px;">MARCHON HYBRID OS</h3>'
        '<p style="color:#9CA3AF;font-size:0.8rem;">Introduce tu PIN</p></div>',
        unsafe_allow_html=True,
    )

    pin = _configured_pin()
    if not pin:
        st.error(
            "No hay PIN configurado. Añade APP_PIN en .streamlit/secrets.toml (local) "
            "o en Settings → Secrets (Streamlit Cloud)."
        )
        return False

    with st.form("pin_login_form"):
        entered = st.text_input("PIN", type="password", placeholder="PIN", label_visibility="collapsed")
        if st.form_submit_button("DESBLOQUEAR", use_container_width=True):
            if hmac.compare_digest(entered.strip(), pin):
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("PIN incorrecto")
    return False


def render_phase_snapshot(sessions: int, pbs: int, total_time: str) -> None:
    st.markdown(
        '<div class="stat-grid">'
        f'<div class="stat-box"><div class="stat-value">{sessions}</div><div class="stat-label">Sesiones</div></div>'
        f'<div class="stat-box"><div class="stat-value" style="color:#FF5722;">{pbs}</div><div class="stat-label">Récords</div></div>'
        f'<div class="stat-box"><div class="stat-value">{total_time}</div><div class="stat-label">Tiempo</div></div>'
        '</div>',
        unsafe_allow_html=True,
    )


def render_kpi_table(rows: List[Dict[str, str]]) -> None:
    for r in rows:
        st.markdown(
            '<div class="exercise-row">'
            f'<div><div class="exercise-name">{r["name"]}</div>'
            f'<div class="muted-small">1RM actual: {r["current"]}</div></div>'
            f'<div style="text-align:right;"><div class="exercise-reps">{r["best"]}</div>'
            f'<div class="muted-small">mejor estimado · {r["delta"]}</div></div>'
            '</div>',
            unsafe_allow_html=True,
        )


def render_exercise_item(name: str, target: str, notes: Optional[str] = None) -> None:
    notes_html = f'<div class="muted-small">{notes}</div>' if notes else ""
    st.markdown(
        f'<div class="exercise-row"><div><div class="exercise-name">{name}</div>{notes_html}</div>'
        f'<span class="exercise-reps">{target}</span></div>',
        unsafe_allow_html=True,
    )
