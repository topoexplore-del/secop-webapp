import streamlit as st
import pandas as pd
import urllib.request
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime

st.set_page_config(page_title="SECOP PRO - Dashboard Colombia", layout="wide")

# ==================== LOGIN ====================
password = st.sidebar.text_input("Contraseña", type="password")
if password != st.secrets.get("PASSWORD", "tu_contraseña_segura_2026"):
    st.error("Contraseña incorrecta")
    st.stop()

st.title("🔍 SECOP PRO - Dashboard de Licitaciones en Colombia")
st.markdown("Sistema privado con organización automática por Departamento → Ciudad → Proceso")

# ==================== CARGAR DATOS ====================
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
    return df

df = cargar_datos()

# ==================== FILTROS AVANZADOS ====================
st.sidebar.header("Filtros")

depto = st.sidebar.multiselect("Departamento", options=sorted(df['Departamento Entidad'].dropna().unique()))
ciudad = st.sidebar.multiselect("Ciudad", options=sorted(df['Ciudad Entidad'].dropna().unique()))
modalidad = st.sidebar.multiselect("Modalidad", options=sorted(df['Modalidad de Contratacion'].dropna().unique()))
palabras = st.sidebar.text_input("Palabras clave (APU, Análisis, Precios Unitarios, etc.)")
valor_min = st.sidebar.number_input("Valor mínimo (COP)", min_value=0, value=0, step=1000000)
fecha_desde = st.sidebar.date_input("Fecha desde", value=pd.to_datetime("2025-01-01"))

# Aplicar filtros
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

# ==================== DASHBOARD ====================
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Mapa de Colombia por Departamento")
    geojson_url = "https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json"
    geojson = json.loads(urllib.request.urlopen(geojson_url).read())

    map_data = filtered.groupby('Departamento Entidad').agg({
        'ID del Proceso': 'count',
        'Valor Total Adjudicacion': 'sum'
    }).reset_index()
    map_data = map_data.rename(columns={'ID del Proceso': 'Número de Procesos'})

    fig_map = px.choropleth_mapbox(
        map_data,
        geojson=geojson,
        locations='Departamento Entidad',
        featureidkey='properties.NOMBRE_DPT',
        color='Número de Procesos',
        color_continuous_scale="RdYlBu_r",  # Rojo intenso para alto número
        range_color=(0, map_data['Número de Procesos'].max()),
        mapbox_style="carto-positron",
        zoom=4.2,
        center={"lat": 4.57, "lon": -74.29},
        opacity=0.7,
        labels={'Número de Procesos': 'Procesos'}
    )
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig_map.update_traces(marker_line_width=0.5, marker_opacity=0.8)
    st.plotly_chart(fig_map, use_container_width=True)

with col2:
    st.header("Distribución por Modalidad")
    pie_data = filtered['Modalidad de Contratacion'].value_counts().reset_index()
    pie_data.columns = ['Modalidad', 'Cantidad']
    fig_pie = px.pie(
        pie_data,
        values='Cantidad',
        names='Modalidad',
        color_discrete_sequence=px.colors.qualitative.Set3,
        hole=0.4
    )
    fig_pie.update_layout(margin=dict(t=0, b=0))
    st.plotly_chart(fig_pie, use_container_width=True)

# Timeline rojo con trimestres
st.header("Evolución Temporal")
timeline_data = filtered.groupby(['Año', 'Trimestre'])['Valor Total Adjudicacion'].sum().reset_index()
timeline_data['Trimestre'] = timeline_data['Trimestre'].astype(str)
fig_timeline = px.bar(
    timeline_data,
    x='Trimestre',
    y='Valor Total Adjudicacion',
    color='Año',
    color_continuous_scale="Reds",
    title="Importe Total por Trimestre y Año",
    barmode='group'
)
fig_timeline.update_layout(xaxis_title="Trimestre", yaxis_title="Importe Total (COP)")
st.plotly_chart(fig_timeline, use_container_width=True)

# Totales grandes destacados
total_procesos = len(filtered)
total_importe = filtered['Valor Total Adjudicacion'].sum() / 1e9  # en miles de millones
total_adjudicadores = filtered['Entidad'].nunique()

st.markdown(f"""
<div style='display: flex; justify-content: space-around; margin: 20px 0;'>
    <div style='background: #ff4b4b; color: white; padding: 20px; border-radius: 10px; text-align: center; width: 30%;'>
        <h3>Total Procesos</h3>
        <h1>{total_procesos}</h1>
    </div>
    <div style='background: #4b8cff; color: white; padding: 20px; border-radius: 10px; text-align: center; width: 30%;'>
        <h3>Importe Total</h3>
        <h1>{total_importe:.2f} mil M</h1>
    </div>
    <div style='background: #4caf50; color: white; padding: 20px; border-radius: 10px; text-align: center; width: 30%;'>
        <h3>Entidades Adjudicadoras</h3>
        <h1>{total_adjudicadores}</h1>
    </div>
</div>
""", unsafe_allow_html=True)

# Tabla por departamento
st.header("Tabla por Departamento")
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

# Descarga
csv = filtered.to_csv(index=False).encode('utf-8')
st.download_button("📥 Descargar resultados como CSV", csv, "secop_filtrados.csv", "text/csv")

st.success("Dashboard dinámico cargado. Filtra y explora los datos de SECOP II.")
