import streamlit as st

def apply_custom_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background-color: #0E1117;
        padding-bottom: 75px;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* TIRA DE CALENDARIO HORIZONTAL UNIFICADA */
    div[data-testid="stHorizontalBlock"]:has(button[key*="cal_strip_"]) {
        background: #161922;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 4px 6px;
        margin-bottom: 0.8rem;
        gap: 4px !important;
    }

    div.stButton > button[key*="cal_strip_"] {
        background: transparent !important;
        border: none !important;
        border-radius: 12px !important;
        color: #9CA3AF !important;
        padding: 4px 2px !important;
        min-height: 64px !important;
        font-size: 0.85rem !important;
        line-height: 1.25 !important;
        font-weight: 700 !important;
    }

    div.stButton > button[key*="cal_strip_"][kind="primary"] {
        background: #000000 !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.6) !important;
    }

    .marchon-subtabs {
        display: flex;
        gap: 1.5rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }

    .subtab-active {
        color: #FFFFFF;
        font-weight: 800;
        font-size: 0.95rem;
        position: relative;
    }
    .subtab-active::after {
        content: '';
        position: absolute;
        bottom: -9px;
        left: 0;
        right: 0;
        height: 2px;
        background: #FFFFFF;
    }

    .subtab-inactive {
        color: #6B7280;
        font-weight: 600;
        font-size: 0.95rem;
    }

    /* TARJETAS COLAPSABLES DE EJERCICIOS (EXPANDERS ESTILO NATIVO) */
    div[data-testid="stExpander"] {
        background: #161922 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        margin-bottom: 0.6rem !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25) !important;
    }

    div[data-testid="stExpander"] details summary {
        font-weight: 700 !important;
        color: #FFFFFF !important;
        font-size: 0.92rem !important;
        padding: 0.75rem 1rem !important;
    }

    div[data-testid="stExpander"] details summary:hover {
        color: #FF5722 !important;
    }

    .block-badge-circle {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background: #FFFFFF;
        color: #0E1117;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 900;
        font-size: 0.75rem;
        margin-right: 0.5rem;
    }

    .block-badge-accent {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background: #FF5722;
        color: #FFFFFF;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 900;
        font-size: 0.75rem;
        margin-right: 0.5rem;
    }

    .mobile-set-box {
        background: #1D222E;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        padding: 0.65rem 0.8rem;
        margin-bottom: 0.5rem;
    }

    .mobile-set-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.35rem;
        padding-bottom: 0.3rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }

    .badge-kpi {
        background-color: #FF5722;
        color: white;
        font-size: 0.7rem;
        font-weight: 800;
        padding: 0.15rem 0.45rem;
        border-radius: 3px;
        display: inline-block;
    }

    .badge-tag {
        background-color: #242936;
        color: #9CA3AF;
        font-size: 0.7rem;
        font-weight: 700;
        padding: 0.15rem 0.45rem;
        border-radius: 4px;
        display: inline-block;
        margin-right: 0.25rem;
        text-transform: uppercase;
    }

    .stat-box {
        background: #1D222E;
        border-radius: 8px;
        padding: 0.6rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .stat-value {
        font-size: 1.3rem;
        font-weight: 800;
        color: #FFFFFF;
    }
    .stat-label {
        font-size: 0.68rem;
        color: #9CA3AF;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 700;
    }

    div.stButton > button {
        background-color: #1D222E;
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        font-weight: 700;
        min-height: 42px;
    }
    div.stButton > button:hover {
        background-color: #FF5722;
        border-color: #FF5722;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
