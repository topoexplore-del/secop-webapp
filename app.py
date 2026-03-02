import streamlit as st
import pandas as pd
import urllib.request
import plotly.express as px  # Para gráficos y mapas dinámicos
import json  # Para cargar geojson

st.set_page_config(page_title="SECOP PRO - Buscador Personal", layout="wide")

st.title("🔍 SECOP PRO - Buscador Personal")
st.markdown("**Sistema privado de búsqueda y organización automática de procesos con APU / Análisis de Precios**")

# ==================== LOGIN SIMPLE ====================
password = st.sidebar.text_input("Contraseña para acceder", type="password")
if password != st.secrets.get("PASSWORD", "tu_contraseña_segura_2026"):
    st.error("Contraseña incorrecta")
    st.stop()

# ==================== CARGAR DATOS DESDE GOOGLE DRIVE ====================
@st.cache_data(ttl=3600)  # cache 1 hora
def cargar_datos():
    url_csv = "https://drive.google.com/uc?export=download&id=1lJCVBwMCJVOaipaJAHd_9jaquQ8hmQ-V"
    try:
        df = pd.read_csv(url_csv, low_memory=False, encoding='utf-8')
        df = df.rename(columns=lambda x: x.strip())
        if 'Fecha de Publicacion del Proceso' in df.columns:
            df['Fecha de Publicacion del Proceso'] = pd.to_datetime(df['Fecha de Publicacion del Proceso'], errors='coerce')
        if 'Valor Total Adjudicacion' in df.columns:
            df['Valor Total Adjudicacion'] = pd.to_numeric(df['Valor Total Adjudicacion'], errors='coerce').fillna(0)
        return df
    except Exception as e:
        st.error(f"Error al cargar el CSV desde Google Drive: {e}")
        return pd.DataFrame()

df = cargar_datos()

if df.empty:
    st.error("No se pudieron cargar los datos. Verifica el enlace de Google Drive.")
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

# ==================== DASHBOARD DINÁMICO ====================
st.header("Dashboard de Licitaciones en Colombia")

# Mapa de Colombia por departamento (coloreado por número de procesos)
@st.cache_resource
def load_geojson():
    url_geojson = "https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json"
    response = urllib.request.urlopen(url_geojson)
    geojson = json.loads(response.read().decode())
    return geojson

geojson = load_geojson()

map_data = filtered.groupby('Departamento Entidad').size().reset_index(name='Num Procesos')

fig_map = px.choropleth_mapbox(
    map_data,
    geojson=geojson,
    locations='Departamento Entidad',
    featureidkey='properties.NOMBRE_DPT',
    color='Num Procesos',
    color_continuous_scale="YlOrRd",
    mapbox_style="carto-positron",
    zoom=4,
    center={"lat": 4.57, "lon": -74.29},
    opacity=0.6,
    labels={'Num Procesos': 'Número de Procesos'}
)
fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig_map, use_container_width=True)

# Gráfico de pastel por Modalidad de Contratacion
if 'Modalidad de Contratacion' in filtered.columns:
    pie_data = filtered['Modalidad de Contratacion'].value_counts()
    fig_pie = px.pie(
        names=pie_data.index,
        values=pie_data.values,
        title="Distribución por Modalidad de Contratación"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# Barras por año (importe total)
if 'Fecha de Publicacion del Proceso' in filtered.columns:
    filtered['Año'] = filtered['Fecha de Publicacion del Proceso'].dt.year
    bar_data = filtered.groupby('Año')['Valor Total Adjudicacion'].sum().reset_index()
    fig_bar = px.bar(
        bar_data,
        x='Año',
        y='Valor Total Adjudicacion',
        title="Importe Total por Año"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# Tabla por departamento con totales
if not filtered.empty:
    table_data = filtered.groupby('Departamento Entidad').agg({
        'ID del Proceso': 'count',
        'Valor Total Adjudicacion': 'sum',
        'Entidad': 'nunique'  # Número de adjudicadores/ entidades únicas
    }).reset_index()
    table_data = table_data.rename(columns={
        'ID del Proceso': 'Núm. Licitaciones',
        'Valor Total Adjudicacion': 'Importe Estimado',
        'Entidad': 'Núm. Adjudicadores'
    })
    st.subheader("Tabla por Departamento")
    st.dataframe(table_data.style.format({
        'Importe Estimado': '${:,.2f} M'
    }), use_container_width=True)

# Mostrar tabla de resultados detallados
st.subheader("Resultados Detallados")
st.dataframe(
    filtered[[
        'ID del Proceso', 'Entidad', 'Departamento Entidad', 'Ciudad Entidad',
        'Nombre del Procedimiento', 'Descripción del Procedimiento',
        'Fecha de Publicacion del Proceso', 'Valor Total Adjudicacion', 'URLProceso'
    ]],
    use_container_width=True,
    hide_index=True
)

# Descarga de resultados
if not filtered.empty:
    csv = filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar resultados como CSV",
        data=csv,
        file_name="secop_resultados.csv",
        mime="text/csv"
    )

st.success("✅ Dashboard dinámico cargado. Los gráficos se actualizan con los filtros.")
