import streamlit as st
import pandas as pd
import urllib.request
import plotly.express as px
import json

# Configuración de página (ancho completo)
st.set_page_config(page_title="SECOP PRO - Portal de Búsqueda", layout="wide", initial_sidebar_state="collapsed")

# Fondo profesional con imagen corporativa
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
        background: transparent;
        padding: 40px;
        text-align: center;
        width: 100%;
        max-width: 800px;
    }
    
    /* Centrar el label de "Contraseña" */
    .stTextInput label {
        display: block !important;
        text-align: center !important;
        color: white !important;
        font-size: 1.2rem !important;
        margin-bottom: 10px !important;
    }

    .stTextInput > div > div > input {
        font-size: 1.5rem;
        padding: 10px;
        border-radius: 10px;
        border: 2px solid rgba(255,255,255,0.4);
        background: rgba(255,255,255,0.15);
        color: white;
        text-align: center;
        width: 100%;
        max-width: 500px;
        margin: 0 auto;
    }

    /* ESTA ES LA PARTE CLAVE PARA EL BOTÓN */
    .stButton {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }

    .stButton > button {
        background: #0d47a1;
        color: white;
        font-size: 1.2rem;
        padding: 12px 60px; /* Aumenté el padding lateral para que se vea mejor */
        border-radius: 10px;
        border: none;
        transition: all 0.3s;
    }

    .stButton > button:hover {
        background: #1565c0;
        transform: scale(1.05);
        box-shadow: 0 10px 20px rgba(13,71,161,0.4);
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


























