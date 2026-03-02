import streamlit as st

# Configuración de página (ocultar sidebar inicial, ancho completo)
st.set_page_config(page_title="SECOP PRO - Portal", layout="wide", initial_sidebar_state="collapsed")

# Estilos profesionales (fondo imagen, todo centrado, sin espacios muertos)
st.markdown("""
    <style>
    /* Fondo imagen corporativa */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.68), rgba(0,0,0,0.68)), 
                    url('https://images.unsplash.com/photo-1556155092-490a1ba16284?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80') 
                    center/cover no-repeat fixed !important;
        min-height: 100vh;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Ocultar header negro, footer y elementos innecesarios */
    header, footer, .stDeployButton, .stSidebarCollapseButton, .css-1d391kg, .css-1v3fvcr, .css-qri22k, .css-1l269bu {
        display: none !important;
    }

    /* Contenedor principal centrado vertical y horizontal */
    .main-login {
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        color: white;
        padding: 0 20px;
    }

    /* Cuadro de bienvenida transparente y elegante (sin blanco grande) */
    .welcome-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 20px;
        padding: 50px 70px;
        max-width: 850px;
        width: 90%;
        box-shadow: 0 15px 50px rgba(0,0,0,0.6);
    }

    .welcome-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 15px;
        text-shadow: 0 4px 15px rgba(0,0,0,0.8);
        color: #ffffff;
        line-height: 1.1;
    }

    .welcome-subtitle {
        font-size: 1.7rem;
        font-weight: 500;
        margin-bottom: 30px;
        color: #e3f2fd;
        text-shadow: 0 2px 10px rgba(0,0,0,0.7);
    }

    .author {
        font-size: 1.45rem;
        color: #bbdefb;
        margin: 40px 0 60px 0;
        font-weight: 500;
        text-shadow: 0 2px 8px rgba(0,0,0,0.6);
    }

    /* Barra contraseña pequeña y centrada */
    .password-box {
        width: 100%;
        max-width: 380px;
        margin: 0 auto;
    }

    .stTextInput > div > div > input {
        font-size: 1.2rem;
        padding: 14px 20px;
        border-radius: 12px;
        border: 2px solid rgba(255,255,255,0.4);
        background: rgba(255,255,255,0.15);
        color: white;
        text-align: center;
        backdrop-filter: blur(8px);
    }

    .stTextInput > div > div > input::placeholder {
        color: rgba(255,255,255,0.8);
    }

    /* Botón Ingresar centrado y elegante */
    .stButton > button {
        background: #0d47a1;
        color: white;
        font-size: 1.3rem;
        padding: 14px 60px;
        border-radius: 12px;
        border: none;
        margin-top: 30px;
        width: 100%;
        font-weight: bold;
        transition: all 0.3s;
    }

    .stButton > button:hover {
        background: #1565c0;
        transform: translateY(-4px);
        box-shadow: 0 15px 35px rgba(13,71,161,0.5);
    }
    </style>
""", unsafe_allow_html=True)

# Estado de autenticación
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Página de login (todo centrado, sin rectángulo grande)
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

# Dashboard principal (solo después del login)
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

