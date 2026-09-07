import streamlit as st

def apply_custom_styles():
    st.markdown("""
    <style>
    /* Estilos globales y reset */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .main {
        background-color: #0E1117;
        padding-top: 1rem;
    }

    /* Ocultar barra superior y footer de Streamlit */
    #MainMenu, header, footer {visibility: hidden;}

    /* Contenedor principal de tarjetas */
    .marchon-card {
        background: #161922;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }

    /* Badges / Pastillas */
    .badge-kpi {
        background-color: #FF5722;
        color: white;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        display: inline-block;
        letter-spacing: 0.5px;
    }

    .badge-tag {
        background-color: #242936;
        color: #E2E8F0;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        display: inline-block;
        margin-right: 0.3rem;
    }

    .badge-green {
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid #10B981;
        color: #10B981;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.15rem 0.5rem;
        border-radius: 6px;
    }

    /* Bloque de entrenamiento (W, S, H, E) */
    .block-header {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-size: 1.1rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 0.75rem;
    }

    .block-letter {
        width: 28px;
        height: 28px;
        border-radius: 6px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 0.85rem;
    }

    .letter-w { background: #374151; color: #9CA3AF; }
    .letter-s { background: #FF5722; color: #FFFFFF; }
    .letter-h { background: #3B82F6; color: #FFFFFF; }
    .letter-e { background: #10B981; color: #FFFFFF; }

    /* Fila de ejercicios */
    .exercise-row {
        background: #1D222E;
        border-radius: 8px;
        padding: 0.6rem 0.9rem;
        margin-bottom: 0.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-left: 3px solid #374151;
    }

    .exercise-name {
        color: #F3F4F6;
        font-weight: 500;
        font-size: 0.9rem;
    }

    .exercise-reps {
        color: #10B981;
        font-weight: 700;
        font-size: 0.85rem;
    }

    /* KPI Snapshot Cards */
    .stat-box {
        background: #1D222E;
        border-radius: 10px;
        padding: 0.75rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .stat-value {
        font-size: 1.5rem;
        font-weight: 800;
        color: #FFFFFF;
    }
    .stat-label {
        font-size: 0.75rem;
        color: #9CA3AF;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Botones y Radio Pills */
    div.stButton > button {
        background-color: #242936;
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        background-color: #FF5722;
        border-color: #FF5722;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
