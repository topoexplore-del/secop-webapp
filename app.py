import streamlit as st
import pandas as pd
import urllib.request
import plotly.express as px
import json

st.set_page_config(page_title="SECOP PRO - Buscador Personal", layout="wide")

# Fondo claro (blanco/gris suave) para toda la página
st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;  /* Gris muy claro / blanco suave */
        color: #212529;
    }
    .stSidebar {
        background-color: #ffffff;  /* Blanco puro para sidebar */
        border-right: 1px solid #dee2e6;
    }
    h1, h2, h3 {
        color: #0d6efd;  /* Azul primario para títulos */
    }
    .stButton > button {
        background-color: #0d6efd;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔍 SECOP PRO - Buscador Personal")
st.markdown("**Sistema privado de búsqueda y organización automática de procesos con APU / Análisis de Precios**")

# ==================== LOGIN SIMPLE ====================
password = st.sidebar.text_input("Contraseña para acceder", type="password")
if password != st.secrets.get("PASSWORD", "Udes12201032*/*T"):
    st.error("Contraseña incorrecta")
    st.stop()

# ==================== CARGAR DATOS ====================
@st.cache_data(ttl=3600)
def cargar_datos():
    url_csv = "https://drive.google.com/uc?export=download&id=1lJCVBwMCJVOaipaJAHd_9jaquQ8hmQ-V"
    try:
        df = pd.read_csv(url_csv, low_memory=False, encoding='utf-8')
        df = df.rename(columns=lambda x: x.strip())
        if 'Fecha de Publicacion del Proceso' in df.columns:
            df['Fecha de Publicacion del Proceso'] = pd.to_datetime(df['Fecha de Publicacion del Proceso'], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Error al cargar el CSV: {e}")
        return pd.DataFrame()

df = cargar_datos()

if df.empty:
    st.error("No se pudieron cargar los datos.")
    st.stop()

# ==================== FILTROS ====================
st.sidebar.header("Filtros")

depto = st.sidebar.multiselect("Departamento", options=sorted(df['Departamento Entidad'].dropna().unique()))
ciudad = st.sidebar.multiselect("Ciudad", options=sorted(df['Ciudad Entidad'].dropna().unique()))
palabras = st.sidebar.text_input("Palabras clave (ej: APU, Análisis, Precios Unitarios)")
fecha_desde = st.sidebar.date_input("Fecha desde", value=pd.to_datetime("2025-01-01"))

# Aplicar filtros
filtered = df.copy()
if depto:
    filtered = filtered[filtered['Departamento Entidad'].isin(depto)]
if ciudad:
    filtered = filtered[filtered['Ciudad Entidad'].isin(ciudad)]
if palabras:
    palabras_list = [p.strip() for p in palabras.split(",")]
    mask = False
    for p in palabras_list:
        mask |= filtered['Descripción del Procedimiento'].str.contains(p, case=False, na=False)
    filtered = filtered[mask]
if fecha_desde:
    filtered = filtered[filtered['Fecha de Publicacion del Proceso'] >= pd.to_datetime(fecha_desde)]

st.subheader(f"Resultados encontrados: {len(filtered)} procesos")

# Tabla de resultados
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
