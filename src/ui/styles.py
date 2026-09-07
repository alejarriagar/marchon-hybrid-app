import streamlit as st

def apply_custom_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background-color: #0E1117;
    }

    div[data-testid="stForm"] {
        background: #161922;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 1.25rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
    }

    .marchon-card {
        background: #161922;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }

    /* Tarjeta de Serie para Móvil */
    .mobile-set-box {
        background: #191D26;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 0.75rem 0.85rem;
        margin-bottom: 0.6rem;
    }

    .mobile-set-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.4rem;
        padding-bottom: 0.3rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }

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
        font-size: 0.72rem;
        font-weight: 600;
        padding: 0.2rem 0.5rem;
        border-radius: 10px;
        display: inline-block;
        margin-right: 0.25rem;
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

    .exercise-row {
        background: #1D222E;
        border-radius: 8px;
        padding: 0.6rem 0.8rem;
        margin-bottom: 0.4rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-left: 3px solid #374151;
    }

    .exercise-name {
        color: #F3F4F6;
        font-weight: 500;
        font-size: 0.88rem;
    }

    .exercise-reps {
        color: #10B981;
        font-weight: 700;
        font-size: 0.82rem;
    }

    .stat-box {
        background: #1D222E;
        border-radius: 10px;
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
        font-size: 0.7rem;
        color: #9CA3AF;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    div.stButton > button {
        background-color: #242936;
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        font-weight: 600;
        min-height: 42px;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        background-color: #FF5722;
        border-color: #FF5722;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
