import streamlit as st

# Configuración de página
st.set_page_config(page_title="SECOP PRO - Portal", layout="wide", initial_sidebar_state="collapsed")

# Estilos modernos y corporativos (fondo imagen, texto legible, centrado)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.65)), 
                    url('https://images.unsplash.com/photo-1556155092-490a1ba16284?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80') 
                    center/cover no-repeat fixed !important;
        min-height: 100vh;
        margin: 0;
        padding: 0;
        overflow: hidden;
    }
    .main-container {
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        color: white;
        padding: 20px;
    }
    .welcome-box {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        border-radius: 16px;
        padding: 50px 60px;
        max-width: 800px;
        width: 90%;
        box-shadow: 0 8px 32px rgba(0,0,0,0.37);
    }
    .welcome-title {
        font-size: 3.2rem;
        font-weight: 700;
        margin-bottom: 15px;
        text-shadow: 0 2px 10px rgba(0,0,0,0.6);
        color: #ffffff;
    }
    .welcome-subtitle {
        font-size: 1.5rem;
        font-weight: 500;
        margin-bottom: 30px;
        color: #e0e0e0;
        text-shadow: 0 1px 6px rgba(0,0,0,0.5);
    }
    .author {
        font-size: 1.3rem;
        color: #b0bec5;
        margin: 30px 0;
    }
    .password-container {
        margin-top: 40px;
        width: 100%;
        max-width: 400px;
    }
    .stTextInput > div > div > input {
        font-size: 1.1rem;
        padding: 14px 18px;
        border-radius: 12px;
        border: 2px solid rgba(255,255,255,0.3);
        background: rgba(255,255,255,0.15);
        color: white;
        backdrop-filter: blur(5px);
    }
    .stTextInput > div > div > input::placeholder {
        color: rgba(255,255,255,0.7);
    }
    .stButton > button {
        background: #0d47a1;
        color: white;
        font-size: 1.2rem;
        padding: 14px 40px;
        border-radius: 12px;
        border: none;
        margin-top: 20px;
        width: 100%;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background: #1565c0;
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(13,71,161,0.4);
    }
    /* Ocultar elementos innecesarios de Streamlit en login */
    header, footer, .stDeployButton, .stSidebarCollapseButton {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# Estado de autenticación
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Página de bienvenida / login
if not st.session_state.authenticated:
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.markdown('<div class="welcome-box">', unsafe_allow_html=True)
    
    st.markdown('<div class="welcome-title">BIENVENIDO AL PORTAL DE BÚSQUEDA</div>', unsafe_allow_html=True)
    st.markdown('<div class="welcome-subtitle">DE PROCESOS DE CONTRATACIÓN</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="author">ELABORADO POR EL INGENIERO<br><strong>OSCAR ANDRÉS TARAZONA FIGUEROA</strong></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="password-container">', unsafe_allow_html=True)
    password = st.text_input("Contraseña:", type="password", key="login_password", label_visibility="collapsed")
    if st.button("Ingresar"):
        if password == st.secrets.get("PASSWORD", "tu_contraseña_segura_2026"):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Contraseña incorrecta")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.stop()

# Dashboard principal (solo si autenticado)
st.title("SECOP PRO - Dashboard de Licitaciones en Colombia")
st.markdown("Sistema privado con organización automática por Departamento → Ciudad → Proceso")

# Cargar datos (tu código anterior de carga CSV)
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

# Filtros (sidebar ahora visible después del login)
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
