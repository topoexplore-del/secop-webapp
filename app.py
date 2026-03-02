import streamlit as st
import pandas as pd

# 1. SIEMPRE la configuración de página primero
st.set_page_config(page_title="SECOP PRO - Portal de Búsqueda", layout="wide", initial_sidebar_state="collapsed")

# 2. Definición de estilos CSS (El nuevo diseño centrado)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)),
                    url('https://images.unsplash.com/photo-1556155092-490a1ba16284?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80')
                    center/cover no-repeat fixed;
    }

    /* Caja de login tipo 'tarjeta flotante' */
    .login-box {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: auto;
        padding: 50px;
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        max-width: 600px;
        text-align: center;
        margin-top: 10vh;
    }

    .login-title { font-size: 2.2rem; font-weight: 800; color: white; margin-bottom: 5px; }
    .login-subtitle { font-size: 1rem; color: #4dabf7; font-weight: 600; text-transform: uppercase; margin-bottom: 20px; }
    .author { font-size: 0.9rem; color: rgba(255,255,255,0.6); margin-bottom: 30px; }

    /* Forzar centrado de la etiqueta y el input */
    .stTextInput label {
        display: block !important;
        text-align: center !important;
        width: 100% !important;
        color: white !important;
    }
    
    .stTextInput div div input {
        text-align: center !important;
        background-color: rgba(0,0,0,0.2) !important;
        color: white !important;
        border-radius: 12px !important;
    }

    /* EL BOTÓN: Centrado total */
    .stButton {
        display: flex !important;
        justify-content: center !important;
        padding-top: 20px;
    }

    .stButton button {
        background: linear-gradient(90deg, #1971c2, #228be6) !important;
        color: white !important;
        border: none !important;
        padding: 10px 50px !important;
        border-radius: 12px !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Lógica de Autenticación
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    # Usamos columnas para ayudar al centrado de Streamlit
    _, col_central, _ = st.columns([1, 2, 1])
    
    with col_central:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown('<div class="login-title">BIENVENIDO AL PORTAL</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-subtitle">DE PROCESOS DE CONTRATACIÓN</div>', unsafe_allow_html=True)
        st.markdown('<div class="author">ELABORADO POR EL ING. OSCAR ANDRÉS TARAZONA FIGUEROA</div>', unsafe_allow_html=True)

        password = st.text_input("Contraseña:", type="password")
        
        if st.button("Ingresar"):
            if password == "tu_contraseña_segura_2026": # Cambia esto por tu secreto
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta")
        
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# 4. Resto del código (Dashboard)
st.title("SECOP PRO - Dashboard")
# ... (tu código de carga de datos aquí)
