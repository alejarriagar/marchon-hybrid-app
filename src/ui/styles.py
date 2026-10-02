import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
html, body, [class*="css"] { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
.stApp { background-color: #0E1117; }
.block-container { padding-top: 1.2rem; padding-bottom: 6.5rem; max-width: 860px; }
header[data-testid="stHeader"] { background: transparent; }

/* Tira de días horizontal */
.st-key-cal_strip { background: #161922; border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 6px; margin-bottom: 0.6rem; }
.st-key-cal_strip [data-testid="stHorizontalBlock"],
.st-key-bottom_nav [data-testid="stHorizontalBlock"] {
    flex-wrap: nowrap !important; overflow-x: auto; gap: 6px !important; scrollbar-width: none;
}
.st-key-cal_strip [data-testid="stHorizontalBlock"]::-webkit-scrollbar { display: none; }
.st-key-cal_strip [data-testid="stColumn"], .st-key-cal_strip [data-testid="column"] {
    flex: 1 0 48px !important; min-width: 48px !important; width: auto !important;
}
.st-key-cal_strip button { min-height: 62px; padding: 4px 2px; border: none; background: transparent; }
.st-key-cal_strip button p { white-space: pre-line; line-height: 1.25; font-size: 0.8rem; font-weight: 700; }
.st-key-cal_strip button[kind="primary"],
.st-key-cal_strip [data-testid="stBaseButton-primary"] {
    background: #000000 !important; border: 1px solid rgba(255,255,255,0.3) !important; color: #FFFFFF !important;
}

/* Barra de navegación inferior fija */
.st-key-bottom_nav {
    position: fixed; left: 0; right: 0; bottom: 0; z-index: 1000;
    background: #0E1117; border-top: 1px solid rgba(255,255,255,0.08);
    padding: 6px 8px calc(6px + env(safe-area-inset-bottom));
}
.st-key-bottom_nav [data-testid="stColumn"], .st-key-bottom_nav [data-testid="column"] {
    flex: 1 0 60px !important; min-width: 60px !important; width: auto !important;
}
.st-key-bottom_nav button { min-height: 44px; padding: 2px; }
.st-key-bottom_nav button p { font-size: 0.68rem; font-weight: 800; letter-spacing: 0.4px; }

/* Cabecera del día */
.day-date { color: #9CA3AF; font-size: 0.78rem; font-weight: 800; letter-spacing: 0.4px; }
.day-program { color: #FFFFFF; font-size: 1.45rem; font-weight: 900; letter-spacing: -0.5px; margin-top: 2px; }
.day-title { color: #E5E7EB; font-size: 0.95rem; font-weight: 700; margin-top: 2px; }
.day-block { color: #10B981; font-size: 0.75rem; font-weight: 800; margin: 4px 0 10px 0; }

/* Tarjetas de ejercicio */
[class*="st-key-ex_"] { background: #1F2430; border-radius: 10px; }
.ex-head { display: flex; justify-content: space-between; align-items: center; gap: 8px; }
.ex-title { color: #FFFFFF; font-weight: 800; font-size: 0.95rem; }
.ex-status { color: #9CA3AF; font-size: 0.72rem; font-weight: 700; white-space: nowrap; }
.ex-status.ok { color: #10B981; }
.ex-sub { color: #9CA3AF; font-size: 0.75rem; margin-top: 2px; }

/* Temporizador de descanso */
.rest-banner {
    position: fixed; top: 10px; left: 50%; transform: translateX(-50%); z-index: 1001;
    background: #FF5722; color: #FFFFFF; font-weight: 900; padding: 0.55rem 1rem; border-radius: 999px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.45); font-size: 0.95rem; letter-spacing: 0.5px; white-space: nowrap;
}
.rest-banner span { font-weight: 600; font-size: 0.75rem; margin-left: 0.6rem; opacity: 0.9; }
.rest-banner.done { background: #10B981; }

/* Componentes generales */
.marchon-card { background: #161922; border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 1rem; margin-bottom: 0.8rem; }
.exercise-row {
    background: #1D222E; border-radius: 8px; padding: 0.6rem 0.8rem; margin-bottom: 0.4rem;
    display: flex; justify-content: space-between; align-items: center; gap: 8px; border-left: 2px solid #374151;
}
.exercise-name { color: #F3F4F6; font-weight: 600; font-size: 0.88rem; }
.exercise-reps { color: #10B981; font-weight: 700; font-size: 0.8rem; text-align: right; }
.muted-small { color: #9CA3AF; font-size: 0.72rem; margin-top: 2px; }
.badge-tag { background: #242936; color: #9CA3AF; font-size: 0.7rem; font-weight: 700; padding: 0.15rem 0.45rem; border-radius: 4px; display: inline-block; margin-right: 0.25rem; text-transform: uppercase; }
.badge-green { background: rgba(16,185,129,0.12); border: 1px solid #10B981; color: #10B981; font-size: 0.72rem; font-weight: 700; padding: 0.15rem 0.45rem; border-radius: 4px; text-transform: uppercase; }
.stat-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 1rem; }
.stat-box { background: #1D222E; border-radius: 8px; padding: 0.6rem; text-align: center; border: 1px solid rgba(255,255,255,0.05); }
.stat-value { font-size: 1.25rem; font-weight: 800; color: #FFFFFF; }
.stat-label { font-size: 0.66rem; color: #9CA3AF; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 700; }
div.stButton > button { border-radius: 10px; font-weight: 700; }
</style>
"""


def apply_custom_styles() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
