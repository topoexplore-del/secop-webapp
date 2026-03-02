import streamlit as st
import pandas as pd
import urllib.request
import plotly.express as px
import json

# Configuración de página (ancho completo, título)
st.set_page_config(page_title="SECOP PRO - Portal de Búsqueda", layout="wide")

# Fondo profesional (oscuro suave con imagen corporativa de fondo)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://images.unsplash.com/photo-1556155092-490a1ba16284?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80') center/cover no-repeat fixed;
        color: white;
        min-height: 100vh;
    }
    .stSidebar {
        background-color: rgba(30, 30, 46, 0.9);
        backdrop-filter: blur(10px);
    }
    .login-container {
        max-width: 600px;
        margin: 15% auto 0 auto;
        padding: 40px;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 16px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        text-align: center;
        color: #1a1a1a;
    }
    .login-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0d47a1;
        margin-bottom: 10px;
    }
    .login-subtitle {
        font-size: 1.1rem;
        color: #424242;
        margin-bottom: 30px;
    }
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #d1d5db;
        padding: 12px;
    }
    .stButton > button {
        background: #0d47a1;
        color: white;
        border-radius: 8px;
        padding: 12px 32px;
        font-weight: bold;
        border: none;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background: #1565c0;
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)

# ==================== PÁGINA DE BIENVENIDA / LOGIN ====================
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    # Contenedor centrado con diseño profesional
    with st.container():
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        st.markdown('<div class="login-title">BIENVENIDO AL PORTAL DE BÚSQUEDA</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-subtitle">DE PROCESOS DE CONTRATACIÓN</div>', unsafe_allow_html=True)
        
        st.markdown("""
            <p style="font-size:1.1rem; color:#424242; margin:20px 0;">
                ELABORADO POR EL INGENIERO<br>
                <strong>OSCAR ANDRÉS TARAZONA FIGUEROA</strong>
            </p>
        """, unsafe_allow_html=True)

        password = st.text_input("Contraseña:", type="password", key="login_password")
        
        if st.button("Ingresar", use_container_width=True):
            if password == st.secrets.get("PASSWORD", "tu_contraseña_segura_2026"):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Ocultar el resto de la página hasta autenticar
    st.stop()

# ==================== CONTENIDO PRINCIPAL (solo si autenticado) ====================
st.title("🔍 SECOP PRO - Dashboard de Licitaciones en Colombia")
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

# Filtros en sidebar
with st.sidebar:
    st.header("Filtros")
    depto = st.multiselect("Departamento", options=sorted(df['Departamento Entidad'].dropna().unique()))
    ciudad = st.multiselect("Ciudad", options=sorted(df['Ciudad Entidad'].dropna().unique()))
    palabras = st.text_input("Palabras clave (APU, Análisis, etc.)")
    fecha_desde = st.date_input("Fecha desde", value=pd.to_datetime("2025-01-01"))

# Aplicar filtros
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

# Tabla principal
st.dataframe(
    filtered[[
        'ID del Proceso', 'Entidad', 'Departamento Entidad', 'Ciudad Entidad',
        'Nombre del Procedimiento', 'Descripción del Procedimiento',
        'Fecha de Publicacion del Proceso', 'Valor Total Adjudicacion', 'URLProceso'
    ]],
    use_container_width=True,
    hide_index=True
)

# Descarga
csv = filtered.to_csv(index=False).encode('utf-8')
st.download_button("📥 Descargar resultados como CSV", csv, "secop_resultados.csv", "text/csv")

st.success("✅ Sistema funcionando correctamente.")
