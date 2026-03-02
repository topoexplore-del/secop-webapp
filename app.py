# 1. Importaciones primero
import streamlit as st
import pandas as pd
# ... otros imports ...

# 2. Configuración de la página (opcional pero recomendado)
st.set_page_config(page_title="SECOP PRO", layout="wide")

# 3. Ahora sí puedes usar st.markdown
st.markdown("""
    <style>
    /* ... tus estilos ... */
    </style>
""", unsafe_allow_html=True)

# ... resto de tu lógica ...
