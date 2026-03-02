import streamlit as st

# Configuración de página
st.set_page_config(page_title="SECOP PRO - Portal", layout="wide", initial_sidebar_state="collapsed")

# Estilos profesionales (fondo imagen centrada, todo centrado, barra contraseña pequeña)
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
    .main-login {
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        color: white;
        padding: 20px;
    }
    .welcome-card {
        background: rgba(255, 255, 255, 0.10);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.20);
        border-radius: 20px;
        padding: 50px 60px;
        max-width: 800px;
        width: 90%;
        box-shadow: 0 15px 40px rgba(0,0,0,0.5);
    }
    .welcome-title {
        font-size: 3.4rem;
        font-weight: 800;
        margin-bottom: 12px;
        text-shadow: 0 3px 12px rgba(0,0,0,0.7);
        color: #ffffff;
        line-height: 1.1;
    }
    .welcome-subtitle {
        font-size: 1.6rem;
        font-weight: 500;
        margin-bottom: 25px;
        color: #e0f2ff;
        text-shadow: 0 2px 8px rgba(0,0,0,0.6);
    }
    .author {
        font-size: 1.4rem;
        color: #b3e5fc;
        margin: 35px 0 50px 0;
        font-weight: 500;
        text-shadow: 0 1px 6px rgba(0,0,0,0.5);
    }
    .password-box {
        width: 100%;
        max-width: 420px;
        margin: 0 auto;
    }
    .stTextInput > div > div > input {
        font-size: 1.15rem;
        padding: 14px 18px;
        border-radius: 12px;
        border: 2px solid rgba(255,255,255,0.35);
        background: rgba(255,255,255,0.18);
        color: white;
        backdrop-filter: blur(6px);
        text-align: center;
    }
    .stTextInput > div > div > input::placeholder {
        color: rgba(255,255,255,0.75);
    }
    .stButton > button {
        background: #0d47a1;
        color: white;
        font-size: 1.25rem;
        padding: 14px 50px;
        border-radius: 12px;
        border: none;
        margin-top: 25px;
        width: 100%;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background: #1565c0;
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(13,71,161,0.45);
    }
    /* Ocultar elementos innecesarios de Streamlit en login */
    header, footer, .stDeployButton, .stSidebarCollapseButton, .css-1d391kg, .css-1v3fvcr {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# Estado de autenticación
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Página de bienvenida / login (todo centrado)
if not st.session_state.authenticated:
    st.markdown('<div class="main-login">', unsafe_allow_html=True)
    
    st.markdown('<div class="welcome-card">', unsafe_allow_html=True)
    
    st.markdown('<div class="welcome-title">BIENVENIDO AL PORTAL DE BÚSQUEDA</div>', unsafe_allow_html=True)
    st.markdown('<div class="welcome-subtitle">DE PROCESOS DE CONTRATACIÓN</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="author">ELABORADO POR EL INGENIERO<br><strong>OSCAR ANDRÉS TARAZONA FIGUEROA</strong></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="password-box">', unsafe_allow_html=True)
    password = st.text_input("Contraseña:", type="password", key="login_pass", label_visibility="collapsed")
    
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

# Dashboard principal (solo después de login)
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

# Filtros en sidebar (ahora visible)
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
