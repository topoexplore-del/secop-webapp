import streamlit as st
import pandas as pd
import urllib.request
import plotly.express as px
import json

# ==================== CONFIGURACIÓN DE PÁGINA ====================
st.set_page_config(page_title="SECOP PRO - Portal de Búsqueda", layout="wide", initial_sidebar_state="collapsed")

# ==================== ESTILOS CSS PROFESIONALES ====================
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.65)),
                    url('https://images.unsplash.com/photo-1556155092-490a1ba16284?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80')
                    center/cover no-repeat fixed;
        min-height: 100vh;
        color: white;
        margin: 0;
        padding: 0;
    }
    .login-box {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: transparent;
        padding: 40px 60px;
        border-radius: 16px;
        box-shadow: none;
        text-align: center;
        max-width: 800px;
        width: 90%;
        margin: 0 auto;
    }
    .login-title {
        font-size: 2.8rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 1px;
        line-height: 0.5;
        text-shadow: 0 2px 8px rgba(0,0,0,0.8);
        text-align: center;
    }
    .login-subtitle {
        font-size: 2.8rem;
        color: #ffffff;
        margin-bottom: 0px;
        font-weight: 700;
        text-shadow: 0 2px 8px rgba(0,0,0,0.8);
        text-align: center;
    }
    .author {
        font-size: 1.3rem;
        color: #bbdefb;
        margin: 30px 0;
        font-weight: 400;
        text-shadow: 0 1px 6px rgba(0,0,0,0.7);
        text-align: center;
    }
    .stTextInput label {
        display: block !important;
        text-align: center !important;
        width: 100% !important;
        color: white !important;
        margin-bottom: 5px !important;
    }
    .stTextInput div div input {
        text-align: center !important;
        background-color: rgba(0,0,0,0.3) !important;
        color: white !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
    }
    .stButton {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
        margin-top: 15px !important;
    }
    .stButton button {
        background: linear-gradient(90deg, #1e40af, #3b82f6) !important;
        color: white !important;
        border: none !important;
        padding: 10px 60px !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
    }
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 20px rgba(59, 130, 246, 0.3) !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== LÓGICA DE AUTENTICACIÓN ====================
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    _, col_central, _ = st.columns([1, 2, 1])
    
    with col_central:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown('<div class="login-title">BIENVENIDO AL PORTAL</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-subtitle">DE PROCESOS DE CONTRATACIÓN</div>', unsafe_allow_html=True)
        st.markdown('<div class="author">ELABORADO POR EL INGENIERO<br><strong>OSCAR ANDRÉS TARAZONA FIGUEROA</strong></div>', unsafe_allow_html=True)
        
        password = st.text_input("Contraseña:", type="password", key="login_pass")
        
        if st.button("Ingresar"):
            if password == st.secrets.get("PASSWORD", "tu_contraseña_segura_2026"):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.stop()

# ==================== DASHBOARD PRINCIPAL ====================
st.title("SECOP PRO - Dashboard de Licitaciones en Colombia")
st.markdown("Sistema privado con organización automática por Departamento → Ciudad → Proceso")

# ==================== CARGAR DATOS DESDE API ====================
@st.cache_data(ttl=3600)  # Cache por 1 hora
def cargar_datos():
    try:
        # URL de la API que compartiste (consulta completa de datos.gov.co)
        url = "https://www.datos.gov.co/resource/p6dx-8zbt.json?$query=SELECT%20%60entidad%60%2C%20%60nit_entidad%60%2C%20%60departamento_entidad%60%2C%20%60ciudad_entidad%60%2C%20%60ordenentidad%60%2C%20%60codigo_pci%60%2C%20%60id_del_proceso%60%2C%20%60referencia_del_proceso%60%2C%20%60ppi%60%2C%20%60id_del_portafolio%60%2C%20%60nombre_del_procedimiento%60%2C%20%60descripci_n_del_procedimiento%60%2C%20%60fase%60%2C%20%60fecha_de_publicacion_del%60%2C%20%60fecha_de_ultima_publicaci%60%2C%20%60fecha_de_publicacion_fase%60%2C%20%60fecha_de_publicacion_fase_1%60%2C%20%60fecha_de_publicacion%60%2C%20%60fecha_de_publicacion_fase_2%60%2C%20%60fecha_de_publicacion_fase_3%60%2C%20%60precio_base%60%2C%20%60modalidad_de_contratacion%60%2C%20%60justificaci_n_modalidad_de%60%2C%20%60duracion%60%2C%20%60unidad_de_duracion%60%2C%20%60fecha_de_recepcion_de%60%2C%20%60fecha_de_apertura_de_respuesta%60%2C%20%60fecha_de_apertura_efectiva%60%2C%20%60ciudad_de_la_unidad_de%60%2C%20%60nombre_de_la_unidad_de%60%2C%20%60proveedores_invitados%60%2C%20%60proveedores_con_invitacion%60%2C%20%60visualizaciones_del%60%2C%20%60proveedores_que_manifestaron%60%2C%20%60respuestas_al_procedimiento%60%2C%20%60respuestas_externas%60%2C%20%60conteo_de_respuestas_a_ofertas%60%2C%20%60proveedores_unicos_con%60%2C%20%60numero_de_lotes%60%2C%20%60estado_del_procedimiento%60%2C%20%60id_estado_del_procedimiento%60%2C%20%60adjudicado%60%2C%20%60id_adjudicacion%60%2C%20%60codigoproveedor%60%2C%20%60departamento_proveedor%60%2C%20%60ciudad_proveedor%60%2C%20%60fecha_adjudicacion%60%2C%20%60valor_total_adjudicacion%60%2C%20%60nombre_del_adjudicador%60%2C%20%60nombre_del_proveedor%60%2C%20%60nit_del_proveedor_adjudicado%60%2C%20%60codigo_principal_de_categoria%60%2C%20%60estado_de_apertura_del_proceso%60%2C%20%60tipo_de_contrato%60%2C%20%60subtipo_de_contrato%60%2C%20%60categorias_adicionales%60%2C%20%60urlproceso%60%2C%20%60codigo_entidad%60%2C%20%60estado_resumen%60"
        
        df = pd.read_json(url)
        df = df.rename(columns=lambda x: x.strip())
        
        # Limpieza de columnas clave
        if 'fecha_de_publicacion_del' in df.columns:
            df['fecha_de_publicacion_del'] = pd.to_datetime(df['fecha_de_publicacion_del'], errors='coerce')
        if 'valor_total_adjudicacion' in df.columns:
            df['valor_total_adjudicacion'] = pd.to_numeric(df['valor_total_adjudicacion'], errors='coerce').fillna(0)
        
        return df
    except Exception as e:
        st.error(f"Error al cargar datos desde la API: {e}")
        return pd.DataFrame()

df = cargar_datos()

# Filtros en la barra lateral
with st.sidebar:
    st.header("Filtros")
    if not df.empty:
        depto = st.multiselect("Departamento", options=sorted(df['departamento_entidad'].dropna().unique()))
        ciudad = st.multiselect("Ciudad", options=sorted(df['ciudad_entidad'].dropna().unique()))
        palabras = st.text_input("Palabras clave (APU, Análisis, etc.)")
        fecha_desde = st.date_input("Fecha desde", value=pd.to_datetime("2025-01-01"))
    else:
        st.warning("No hay datos para filtrar.")

# Aplicar filtros
if not df.empty:
    filtered = df.copy()
    if depto:
        filtered = filtered[filtered['departamento_entidad'].isin(depto)]
    if ciudad:
        filtered = filtered[filtered['ciudad_entidad'].isin(ciudad)]
    if palabras:
        mask = filtered['descripci_n_del_procedimiento'].str.contains(palabras, case=False, na=False)
        filtered = filtered[mask]
    if fecha_desde:
        filtered = filtered[filtered['fecha_de_publicacion_del'] >= pd.to_datetime(fecha_desde)]

    st.subheader(f"Resultados encontrados: {len(filtered)} procesos")

    st.dataframe(
        filtered[[
            'id_del_proceso', 'entidad', 'departamento_entidad', 'ciudad_entidad',
            'nombre_del_procedimiento', 'descripci_n_del_procedimiento',
            'fecha_de_publicacion_del', 'valor_total_adjudicacion', 'urlproceso'
        ]],
        use_container_width=True,
        hide_index=True
    )

    csv = filtered.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Descargar resultados como CSV", csv, "secop_resultados.csv", "text/csv")

    st.success("✅ Dashboard cargado correctamente desde la API.")
else:
    st.info("Esperando datos de la API...")
