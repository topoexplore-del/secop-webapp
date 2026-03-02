import streamlit as st
import pandas as pd

# 1. Configuración de página obligatoria al inicio
st.set_page_config(page_title="SECOP PRO - Portal de Búsqueda", layout="wide", initial_sidebar_state="collapsed")

# 2. Estilos CSS corregidos para centrar TODO
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)),
                    url('https://images.unsplash.com/photo-1556155092-490a1ba16284?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80')
                    center/cover no-repeat fixed;
    }

    /* Contenedor principal del login */
    .login-box {
        text-align: center;
        padding: 40px;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 50px;
    }

    .login-title { font-size: 2.5rem; font-weight: 800; color: white; margin-bottom: 5px; }
    .login-subtitle { font-size: 1.2rem; color: #3b82f6; font-weight: 600; margin-bottom: 20px; }
    .author { font-size: 0.9rem; color: rgba(255,255,255,0.6); margin-bottom: 30px; }

    /* Centrar etiqueta de contraseña e input */
    .stTextInput label {
        display: block !important;
        text-align: center !important;
        color: white !important;
        width: 100% !important;
    }
    
    .stTextInput div div input {
        text-align: center !important;
        border-radius: 12px !important;
    }

    /* FORZAR CENTRADO DEL BOTÓN */
    .stButton {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
        margin-top: 20px !important;
    }

    .stButton > button {
        background: #3b82f6 !important;
        color: white !important;
        padding: 10px 40px !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Lógica de Login con columnas para centrado matemático
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    # Creamos 3 columnas: la del centro (col2) es donde irá nuestro contenido
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown('<div class="login-title">BIENVENIDO AL PORTAL</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-subtitle">DE PROCESOS DE CONTRATACIÓN</div>', unsafe_allow_html=True)
        st.markdown('<div class="author">ELABORADO POR EL ING. OSCAR ANDRÉS TARAZONA FIGUEROA</div>', unsafe_allow_html=True)

        # El input de contraseña
        password = st.text_input("Contraseña:", type="password", key="login_pass")
        
        # El botón ahora heredará el display:flex del CSS y se centrará
        if st.button("Ingresar"):
            if password == "tu_contraseña_2026": # Cambia esto por tu contraseña real
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta")
        
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# Si llega aquí, es porque está autenticado
st.title("SECOP PRO - Dashboard")
