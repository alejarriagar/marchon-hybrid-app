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

    /* 1. FORZAR TIRA HORIZONTAL EN MÓVIL (SCROLL HORIZONTAL) */
    div[data-testid="stHorizontalBlock"]:has(button[key*="cal_strip_"]) {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        background: #161922 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 6px !important;
        margin-bottom: 0.8rem !important;
        gap: 6px !important;
        scrollbar-width: none !important;
    }
    div[data-testid="stHorizontalBlock"]:has(button[key*="cal_strip_"])::-webkit-scrollbar {
        display: none !important;
    }
    div[data-testid="stHorizontalBlock"]:has(button[key*="cal_strip_"]) > div {
        min-width: 52px !important;
        flex: 0 0 auto !important;
    }

    /* Botones de días */
    div.stButton > button[key*="cal_strip_"] {
        background: transparent !important;
        border: none !important;
        border-radius: 12px !important;
        color: #9CA3AF !important;
        padding: 4px 2px !important;
        min-height: 60px !important;
        font-size: 0.82rem !important;
        line-height: 1.25 !important;
        font-weight: 700 !important;
    }

    /* Cápsula del día activo */
    div.stButton > button[key*="cal_strip_"][kind="primary"] {
        background: #000000 !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.6) !important;
    }

    /* 2. JERARQUÍA DE COLORES Y BORDES POR SECCIÓN */
    .block-header-w { border-left: 3px solid #10B981 !important; }
    .block-header-s { border-left: 3px solid #FF5722 !important; }
    .block-header-h { border-left: 3px solid #3B82F6 !important; }
    .block-header-r { border-left: 3px solid #10B981 !important; }

    /* Expanders de Sección (Nivel 1) */
    div[data-testid="stExpander"] {
        background: #161922 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        margin-bottom: 0.75rem !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25) !important;
    }

    div[data-testid="stExpander"] details summary {
        font-weight: 800 !important;
        color: #FFFFFF !important;
        font-size: 0.95rem !important;
        padding: 0.8rem 1rem !important;
        letter-spacing: 0.3px !important;
    }

    /* 3. INSIGNIAS CIRCULARES CON ESPACIADO CORREGIDO */
    .badge-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 24px;
        height: 24px;
        border-radius: 6px;
        font-weight: 900;
        font-size: 0.75rem;
        margin-right: 10px;
    }
    .badge-icon-w { background: #10B981; color: white; }
    .badge-icon-s { background: #FF5722; color: white; }
    .badge-icon-h { background: #3B82F6; color: white; }
    .badge-icon-r { background: #10B981; color: white; }

    /* 4. TARJETAS DE EJERCICIO (NIVEL 2) CON CONTRASTE ELEVADO */
    .exercise-card-container {
        background: #1F2430;
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 10px;
        padding: 0.8rem;
        margin-bottom: 0.6rem;
    }

    /* 5. TARJETAS DE SERIE (NIVEL 3) */
    .set-accordion-box {
        background: #252B3A;
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 8px;
        padding: 0.65rem 0.8rem;
        margin-bottom: 0.5rem;
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

    .badge-green {
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid #10B981;
        color: #10B981;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 0.15rem 0.45rem;
        border-radius: 4px;
        text-transform: uppercase;
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
