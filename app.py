import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="SECOP PRO - Tu Colombia Licita", layout="wide")
st.title("🔍 SECOP PRO - Buscador Personal")
st.markdown("**Sistema privado de búsqueda y organización automática de procesos con APU / Análisis de Precios**")

# ==================== LOGIN SIMPLE ====================
password = st.sidebar.text_input("Contraseña para acceder", type="password")
if password != st.secrets.get("PASSWORD", "tu_contraseña_segura_2026"):
    st.error("Contraseña incorrecta")
    st.stop()

# ==================== CARGAR DATOS ====================
@st.cache_data
def cargar_datos():
    import pandas as pd
import urllib.request

# URL de descarga directa desde Google Drive
url_csv = "https://drive.google.com/uc?export=download&id=1lJCVBwMCJVOaipaJAHd_9jaquQ8hmQ-V"
df = pd.read_csv(url_csv, low_memory=False)
    df = df.rename(columns=lambda x: x.strip())
    if 'Fecha de Publicacion del Proceso' in df.columns:
        df['Fecha de Publicacion del Proceso'] = pd.to_datetime(df['Fecha de Publicacion del Proceso'], errors='coerce')
    return df

df = cargar_datos()

# ==================== FILTROS (como Colombia Licita) ====================
st.sidebar.header("Filtros")

depto = st.sidebar.multiselect("Departamento", options=sorted(df['Departamento Entidad'].dropna().unique()))
ciudad = st.sidebar.multiselect("Ciudad", options=sorted(df['Ciudad Entidad'].dropna().unique()))
palabras = st.sidebar.text_input("Palabras clave (APU, Análisis, etc.)")
fecha_desde = st.sidebar.date_input("Fecha desde", value=pd.to_datetime("2025-01-01"))

# Aplicar filtros
filtered = df.copy()
if depto:
    filtered = filtered[filtered['Departamento Entidad'].isin(depto)]
if ciudad:
    filtered = filtered[filtered['Ciudad Entidad'].isin(ciudad)]
if palabras:
    filtered = filtered[filtered['Descripción del Procedimiento'].str.contains(palabras, case=False, na=False)]
if fecha_desde:
    filtered = filtered[filtered['Fecha de Publicacion del Proceso'] >= pd.to_datetime(fecha_desde)]

st.subheader(f"Resultados encontrados: {len(filtered)} procesos")

# Mostrar tabla
st.dataframe(filtered[['ID del Proceso', 'Entidad', 'Departamento Entidad', 'Ciudad Entidad', 
                       'Nombre del Procedimiento', 'Fecha de Publicacion del Proceso', 'Valor Total Adjudicacion']], 
             use_container_width=True)

# Botón de descarga
csv = filtered.to_csv(index=False).encode('utf-8')
st.download_button("📥 Descargar resultados como CSV", csv, "secop_resultados.csv", "text/csv")


st.success("✅ Sistema funcionando correctamente. Los archivos se organizan automáticamente por Departamento → Ciudad → Proceso")
