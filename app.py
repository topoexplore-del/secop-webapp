import streamlit as st
import pandas as pd
import urllib.request
import plotly.express as px
import json
# Configuración de página (ancho completo)
st.set_page_config(page_title="SECOP PRO - Portal de Búsqueda", layout="wide", initial_sidebar_state="collapsed")
# Fondo profesional con imagen corporativa (la misma que te gustó)
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
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: rgba(255, 255, 255, 0.95);
        padding: 50px 60px;
        border-radius: 16px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        text-align: center;
        max-width: 700px;
        width: 90%;
    }
    .login-title {
        font-size: 2.8rem;
        font-weight: 700;
        color: #0d47a1;
        margin-bottom: 15px;
        line-height: 1.2;
    }
    .login-subtitle {
        font-size: 1.3rem;
        color: #424242;
        margin-bottom: 40px;
        font-weight: 500;
    }
    .stTextInput > div > div > input {
        font-size: 1.2rem;
        padding: 14px;
        border-radius: 10px;
        border: 2px solid #d1d5db;
    }
    .stButton > button {
        background: #0d47a1;
        color: white;
        font-size: 1.2rem;
        padding: 14px 40px;
        border-radius: 10px;
        border: none;
        margin-top: 20px;
        width: 100%;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background: #1565c0;
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(13,71,161,0.3);
    }
    </style>
""", unsafe_allow_html=True)
# ==================== PÁGINA DE INICIO / LOGIN ====================
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if not st.session_state.authenticated:
    # Contenedor centrado con diseño corporativo
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
   
    st.markdown('<div class="login-title">BIENVENIDO AL PORTAL DE BÚSQUEDA</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-subtitle">DE PROCESOS DE CONTRATACIÓN</div>', unsafe_allow_html=True)
   
    st.markdown("""
        <p style="font-size:1.4rem; color:#424242; margin:30px 0; font-weight:500;">
            ELABORADO POR EL INGENIERO

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
   
    # Ocultar todo lo demás hasta autenticar
    st.stop()
# ==================== DASHBOARD PRINCIPAL (solo si autenticado) ====================
st.title("SECOP PRO - Dashboard de Licitaciones en Colombia")
st.markdown("Sistema privado con organización automática por Departamento → Ciudad → Proceso")
# Cargar datos
@st.cache_data(ttl=3600)
def cargar_datos():
    url_csv = "https://drive.google.com/uc?export=download&id=1lJCVBwMCJVOaipaJAHd_9jaquQ8hmQ-V"
    df = pd.read_csv(url_csv, low_memory=False, encoding='utf-8')
    df = df.rename(columns=lambda x: x.strip())
    if 'Fecha de Publicacion del Proceso' in df.columns:
        df['Fecha de Publicacion del Proceso'] = pd.to_datetime(df['Fecha de Publicacion del Proceso'], errors='coerce')
    if 'Valor Total Adjudicacion' in df.columns:
        df['Valor Total Adjudicacion'] = pd.to_numeric(df['Valor Total Adjudicacion'], errors='coerce').fillna(0)
    return df
df = cargar_datos()
# Filtros
with st.sidebar:
    st.header("Filtros")
    depto = st.multiselect("Departamento", options=sorted(df['Departamento Entidad'].dropna().unique()))
    ciudad = st.multiselect("Ciudad", options=sorted(df['Ciudad Entidad'].dropna().unique()))
    palabras = st.text_input("Palabras clave (APU, Análisis, etc.)")
    fecha_desde = st.date_input("Fecha desde", value=pd.to_datetime("2025-01-01"))
filtered = df.copy()
if depto:
    filtered = filtered[filtered['Departamento Entidad'].isin(depto)]
if ciudad:
    filtered = filtered[filtered['Ciudad Entidad'].isin(ciudad)]
if palabras:
    mask = filtered['Descripción del Procedimiento'].str.contains(palabras, case=False, na=False)
    filtered = filtered[mask]
if fecha_desde:
    filtered = filtered[filtered['Fecha de Publicacion del Proceso'] >= pd.to_datetime(fecha_desde)]
st.subheader(f"Resultados encontrados: {len(filtered)} procesos")
st.dataframe(
    filtered[[
        'ID del Proceso', 'Entidad', 'Departamento Entidad', 'Ciudad Entidad',
        'Nombre del Procedimiento', 'Descripción del Procedimiento',
        'Fecha de Publicacion del Proceso', 'Valor Total Adjudicacion', 'URLProceso'
    ]],
    use_container_width=True,
    hide_index=True
)
csv = filtered.to_csv(index=False).encode('utf-8')
st.download_button("📥 Descargar resultados como CSV", csv, "secop_resultados.csv", "text/csv")
st.success("✅ Dashboard cargado correctamente.")
" y seguiremos trabajando sobre el,listo
