import streamlit as st
import pandas as pd
import urllib.request
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime
from io import BytesIO
import matplotlib.pyplot as plt  # Para gradientes en tabla

st.set_page_config(page_title="SECOP PRO - Dashboard Colombia", layout="wide")

# Fondo oscuro elegante
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    .stSidebar {
        background-color: #161b22;
    }
    h1, h2, h3 {
        color: #ff4b4b;
    }
    .stButton > button {
        background-color: #ff4b4b;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Login
password = st.sidebar.text_input("Contraseña", type="password")
if password != st.secrets.get("PASSWORD", "tu_contraseña_segura_2026"):
    st.error("Contraseña incorrecta")
    st.stop()

st.title("🔍 SECOP PRO - Dashboard de Licitaciones en Colombia")
st.markdown("**Sistema privado con organización automática por Departamento → Ciudad → Proceso**")

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
    df['Año'] = df['Fecha de Publicacion del Proceso'].dt.year
    df['Trimestre'] = df['Fecha de Publicacion del Proceso'].dt.quarter
    df['Trimestre_Label'] = df.apply(lambda x: f"Q{x['Trimestre']} {x['Año']}", axis=1)
    return df

df = cargar_datos()

# Filtros
with st.sidebar:
    st.header("Filtros")
    depto = st.multiselect("Departamento", options=sorted(df['Departamento Entidad'].dropna().unique()))
    ciudad = st.multiselect("Ciudad", options=sorted(df['Ciudad Entidad'].dropna().unique()))
    modalidad = st.multiselect("Modalidad", options=sorted(df['Modalidad de Contratacion'].dropna().unique()))
    palabras = st.text_input("Palabras clave (APU, Análisis, Precios Unitarios, etc.)")
    valor_min = st.number_input("Valor mínimo (COP)", min_value=0, value=0, step=1000000)
    fecha_desde = st.date_input("Fecha desde", value=pd.to_datetime("2025-01-01"))

filtered = df.copy()
if depto:
    filtered = filtered[filtered['Departamento Entidad'].isin(depto)]
if ciudad:
    filtered = filtered[filtered['Ciudad Entidad'].isin(ciudad)]
if modalidad:
    filtered = filtered[filtered['Modalidad de Contratacion'].isin(modalidad)]
if palabras:
    palabras_list = [p.strip() for p in palabras.split(",")]
    mask = False
    for p in palabras_list:
        mask |= filtered['Descripción del Procedimiento'].str.contains(p, case=False, na=False)
    filtered = filtered[mask]
if valor_min > 0:
    filtered = filtered[filtered['Valor Total Adjudicacion'] >= valor_min]
if fecha_desde:
    filtered = filtered[filtered['Fecha de Publicacion del Proceso'] >= pd.to_datetime(fecha_desde)]

st.subheader(f"Resultados encontrados: **{len(filtered)}** procesos")

# Totales destacados
col1, col2, col3 = st.columns(3)
total_procesos = len(filtered)
total_importe = filtered['Valor Total Adjudicacion'].sum() / 1e9
total_adjudicadores = filtered['Entidad'].nunique()

with col1:
    st.metric("Total Procesos", f"{total_procesos:,}")
with col2:
    st.metric("Importe Total", f"{total_importe:,.2f} mil M COP")
with col3:
    st.metric("Entidades Adjudicadoras", total_adjudicadores)

# Mapa con municipios (más detalle)
st.header("Mapa de Colombia por Municipios (resaltado por filtros)")
geojson_mun_url = "https://raw.githubusercontent.com/diegovalle/mx-municipios/master/geojson/municipios_colombia.geojson"  # GeoJSON municipios
try:
    geojson_mun = json.loads(urllib.request.urlopen(geojson_mun_url).read())
    map_data_mun = filtered.groupby('Ciudad Entidad').agg({
        'ID del Proceso': 'count',
        'Valor Total Adjudicacion': 'sum'
    }).reset_index()
    map_data_mun = map_data_mun.rename(columns={'ID del Proceso': 'Procesos'})

    fig_map = px.choropleth_mapbox(
        map_data_mun,
        geojson=geojson_mun,
        locations='Ciudad Entidad',
        featureidkey='properties.NOMBRE_MUN',
        color='Procesos',
        color_continuous_scale="RdBu_r",  # Rojo intenso para alto
        range_color=(0, map_data_mun['Procesos'].max()),
        mapbox_style="carto-darkmatter",
        zoom=5.5,
        center={"lat": 4.57, "lon": -74.29},
        opacity=0.7,
        labels={'Procesos': 'Procesos'}
    )
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)
except:
    st.warning("Mapa de municipios no cargó. Usando por departamentos.")
    # Fallback mapa departamentos
    geojson_dep_url = "https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json"
    geojson_dep = json.loads(urllib.request.urlopen(geojson_dep_url).read())
    map_data_dep = filtered.groupby('Departamento Entidad').agg({
        'ID del Proceso': 'count'
    }).reset_index()
    fig_map_dep = px.choropleth_mapbox(
        map_data_dep,
        geojson=geojson_dep,
        locations='Departamento Entidad',
        featureidkey='properties.NOMBRE_DPT',
        color='ID del Proceso',
        color_continuous_scale="RdBu_r",
        mapbox_style="carto-darkmatter",
        zoom=4.5,
        center={"lat": 4.57, "lon": -74.29},
        opacity=0.7
    )
    st.plotly_chart(fig_map_dep, use_container_width=True)

# Timeline rojo continuo
st.header("Evolución Temporal (Timeline Rojo)")
timeline_data = filtered.groupby('Trimestre_Label')['Valor Total Adjudicacion'].sum().reset_index()
timeline_data = timeline_data.sort_values('Trimestre_Label')

fig_timeline = go.Figure()
fig_timeline.add_trace(go.Scatter(
    x=timeline_data['Trimestre_Label'],
    y=timeline_data['Valor Total Adjudicacion'] / 1e9,
    mode='lines+markers',
    line=dict(color='red', width=4),
    marker=dict(size=10, color='darkred', symbol='circle'),
    name='Importe Total'
))
fig_timeline.update_layout(
    title="Importe Total por Trimestre (Rojo Continuo)",
    xaxis_title="Trimestre",
    yaxis_title="Importe (miles de millones COP)",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='white',
    height=400
)
st.plotly_chart(fig_timeline, use_container_width=True)

# Exportar gráficos
if st.button("Exportar Mapa como PNG"):
    buf = BytesIO()
    fig_map.write_image(buf, format="png", engine="kaleido")
    buf.seek(0)
    st.download_button("Descargar Mapa", buf, "mapa_colombia.png", "image/png")

if st.button("Exportar Timeline como PNG"):
    buf = BytesIO()
    fig_timeline.write_image(buf, format="png", engine="kaleido")
    buf.seek(0)
    st.download_button("Descargar Timeline", buf, "timeline_importe.png", "image/png")

# Tabla por departamento
st.header("Resumen por Departamento")
table_data = filtered.groupby('Departamento Entidad').agg({
    'ID del Proceso': 'count',
    'Valor Total Adjudicacion': 'sum',
    'Entidad': 'nunique'
}).reset_index()
table_data = table_data.rename(columns={
    'ID del Proceso': 'Núm. Licitaciones',
    'Valor Total Adjudicacion': 'Importe Estimado',
    'Entidad': 'Núm. Adjudicadores'
})
st.dataframe(
    table_data.style.format({
        'Importe Estimado': '${:,.2f} M'
    }).background_gradient(cmap='Reds', subset=['Importe Estimado', 'Núm. Licitaciones']),
    use_container_width=True
)

# Resultados detallados
st.header("Resultados Detallados")
st.dataframe(
    filtered[[
        'ID del Proceso', 'Entidad', 'Departamento Entidad', 'Ciudad Entidad',
        'Nombre del Procedimiento', 'Descripción del Procedimiento',
        'Fecha de Publicacion del Proceso', 'Valor Total Adjudicacion', 'URLProceso'
    ]].style.format({'Valor Total Adjudicacion': '${:,.2f}'}),
    use_container_width=True,
    hide_index=True
)

# Descarga CSV
csv = filtered.to_csv(index=False).encode('utf-8')
st.download_button("📥 Descargar resultados como CSV", csv, "secop_filtrados.csv", "text/csv")

st.success("Dashboard dinámico cargado. Filtra y explora los datos de SECOP II.")
