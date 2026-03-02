import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import os

# ==================== CONFIGURACIÓN DE PÁGINA ====================
st.set_page_config(page_title="SECOP PRO - Portal de Búsqueda", layout="wide", initial_sidebar_state="collapsed")

# ==================== ESTILOS CSS PROFESIONALES ====================
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)),
                    url('https://images.unsplash.com/photo-1556155092-490a1ba16284?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80')
                    center/cover no-repeat fixed;
        color: white;
    }

    /* Caja de login tipo 'tarjeta flotante' profesional */
    .login-box {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: auto;
        padding: 50px;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border-radius: 24px;
        
        /* ELIMINAR REFLEJOS Y BORDES */
        border: none !important;
        box-shadow: none !important;
        
        text-align: center;
        max-width: 650px;
        margin-top: 10vh;
    }

    .login-title { font-size: 2.2rem; font-weight: 800; color: white; margin-bottom: 5px; }
    .login-subtitle { font-size: 1.1rem; color: #3b82f6; font-weight: 600; text-transform: uppercase; margin-bottom: 20px; }
    .author { font-size: 0.95rem; color: rgba(255,255,255,0.7); margin-bottom: 30px; line-height: 1.5; }

    /* Forzar centrado de la etiqueta y el input */
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

    /* FORZAR CENTRADO DEL BOTÓN */
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
    # Usamos columnas para asegurar el centrado matemático
    _, col_central, _ = st.columns([1, 2, 1])
    
    with col_central:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown('<div class="login-title">BIENVENIDO AL PORTAL</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-subtitle">DE PROCESOS DE CONTRATACIÓN</div>', unsafe_allow_html=True)
        st.markdown('<div class="author">ELABORADO POR EL INGENIERO<br><strong>OSCAR ANDRÉS TARAZONA FIGUEROA</strong></div>', unsafe_allow_html=True)

        password = st.text_input("Contraseña:", type="password", key="login_pass")
        
        if st.button("Ingresar"):
            # IMPORTANTE: Configura PASSWORD en Streamlit Secrets
            if password == st.secrets.get("PASSWORD", "tu_contraseña_segura_2026"):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.stop() 

# ==================== LÓGICA AUTOMÁTICA DRIVE ====================
@st.cache_data(ttl=3600)
def cargar_datos_automatico():
    # 1. Configurar credenciales desde el archivo JSON en GitHub
    KEY_PATH = "credentials.json"
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    
    if not os.path.exists(KEY_PATH):
        st.error("Archivo credentials.json no encontrado en el repositorio.")
        return pd.DataFrame()
        
    creds = service_account.Credentials.from_service_account_file(KEY_PATH, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)

    # 2. ID de la carpeta que compartiste en Drive
    FOLDER_ID = '1cpzTb_oqrK8OYJMbsSrsqcNOXbd2GfXv' # <--- ID CONFIGURADO

    # 3. Buscar el archivo más reciente en la carpeta
    try:
        results = service.files().list(
            q=f"'{FOLDER_ID}' in parents and mimeType='text/csv'",
            spaces='drive',
            fields='files(id, name, modifiedTime)',
            orderBy='modifiedTime desc',
            pageSize=1
        ).execute()
        
        files = results.get('files', [])
        
        if not files:
            st.error("No se encontraron archivos CSV en la carpeta de Drive.")
            return pd.DataFrame()

        file_id = files[0]['id']
        
        # 4. Descargar el archivo
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        fh.seek(0)
        
        # 5. Leer con Pandas
        df = pd.read_csv(fh, low_memory=False, encoding='utf-8')
        df = df.rename(columns=lambda x: x.strip())
        
        # --- Limpieza de datos ---
        if 'Fecha de Publicacion del Proceso' in df.columns:
            df['Fecha de Publicacion del Proceso'] = pd.to_datetime(df['Fecha de Publicacion del Proceso'], errors='coerce')
        if 'Valor Total Adjudicacion' in df.columns:
            df['Valor Total Adjudicacion'] = pd.to_numeric(df['Valor Total Adjudicacion'], errors='coerce').fillna(0)
        
        return df

    except Exception as e:
        st.error(f"Error al conectar con Drive: {e}")
        return pd.DataFrame()

# ==================== DASHBOARD PRINCIPAL ====================
st.title("SECOP PRO - Dashboard de Licitaciones en Colombia")
st.markdown("Sistema privado con organización automática por Departamento → Ciudad → Proceso")

# Cargar datos
df = cargar_datos_automatico()

# Filtros en la barra lateral
with st.sidebar:
    st.header("Filtros")
    if not df.empty:
        depto = st.multiselect("Departamento", options=sorted(df['Departamento Entidad'].dropna().unique()))
        ciudad = st.multiselect("Ciudad", options=sorted(df['Ciudad Entidad'].dropna().unique()))
        palabras = st.text_input("Palabras clave (APU, Análisis, etc.)")
        fecha_desde = st.date_input("Fecha desde", value=pd.to_datetime("2025-01-01"))
    else:
        st.warning("No hay datos para filtrar.")

# Aplicar filtros
if not df.empty:
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

    # Mostrar Resultados
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

    # Descargar datos
    csv = filtered.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Descargar resultados como CSV", csv, "secop_resultados.csv", "text/csv")
    st.success("✅ Dashboard cargado correctamente.")
else:
    st.info("Esperando datos...")
