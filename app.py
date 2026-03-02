import streamlit as st
import pandas as pd

st.set_page_config(page_title="SECOP PRO - Portal de Búsqueda", layout="wide", initial_sidebar_state="collapsed")

# Estilos CSS para login limpio y centrado
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.65)),
                    url('https://images.unsplash.com/photo-1556155092-490a1ba16284?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80')
                    center/cover no-repeat fixed;
        min-height: 100vh;
        color: white;
    }
    .login-box {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: rgba(0,0,0,0.5);
        padding: 30px 40px;
        border-radius: 12px;
        text-align: center;
        max-width: 400px;
        width: 90%;
        box-shadow: 0 6px 18px rgba(0,0,0,0.6);
    }
    .login-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 5px;
        color: #fff;
    }
    .login-subtitle {
        font-size: 1.2rem;
        margin-bottom: 20px;
        color: #ddd;
    }
    .author {
        font-size: 0.9rem;
        color: #bbdefb;
        margin: 15px 0;
    }
    .stTextInput > div > div > input {
        font-size: 1rem;
        padding: 8px;
        border-radius: 6px;
        border: 1px solid rgba(255,255,255,0.4);
        background: rgba(255,255,255,0.15);
        color: white;
        text-align: center;
        width: 80%;
        max-width: 250px;
        margin: 0 auto;
        display: block;
    }
    .stButton > button {
        background: #0d47a1;
        color: white;
        font-size: 1rem;
        padding: 10px 20px;
        border-radius: 6px;
        border: none;
        margin-top: 15px;
        width: 60%;
        max-width: 200px;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    .stButton > button:hover {
        background: #1565c0;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(13,71,161,0.3);
    }
    </style>
""", unsafe_allow_html=True)

# ==================== LOGIN ====================
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">BIENVENIDO AL PORTAL DE BÚSQUEDA</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-subtitle">DE PROCESOS DE CONTRATACIÓN</div>', unsafe_allow_html=True)
    st.markdown("""
        <p class="author">
            ELABORADO POR EL INGENIERO<br>
            <strong>OSCAR ANDRÉS TARAZONA FIGUEROA</strong>
        </p>
    """, unsafe_allow_html=True)

    password = st.text_input("Contraseña:", type="password", key="login_pass")
    if st.button("Ingresar"):
        if password == st.secrets.get("PASSWORD", "tu_contraseña_segura_2026"):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Contraseña incorrecta")

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ==================== DASHBOARD PRINCIPAL ====================
st.title("SECOP PRO - Dashboard de Licitaciones en Colombia")
st.markdown("Sistema privado con organización automática por Departamento → Ciudad → Proceso")

# Aquí puedes seguir con tu lógica de carga de datos y filtros...
