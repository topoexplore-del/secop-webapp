st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)),
                    url('https://images.unsplash.com/photo-1556155092-490a1ba16284?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80')
                    center/cover no-repeat fixed;
    }

    /* Caja de login sin reflejos ni sombras pesadas */
    .login-box {
        text-align: center;
        padding: 40px;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        
        /* SOLUCIÓN AL REFEJO: Quitamos sombras y bordes innecesarios */
        border: none !important;
        box-shadow: none !important;
        
        margin-top: 50px;
    }

    .login-title { font-size: 2.5rem; font-weight: 800; color: white; margin-bottom: 5px; }
    .login-subtitle { font-size: 1.2rem; color: #3b82f6; font-weight: 600; margin-bottom: 20px; }
    .author { font-size: 0.9rem; color: rgba(255,255,255,0.6); margin-bottom: 30px; }

    /* Centrar etiqueta de contraseña e input */
    .stTextInput label {
        display: block !important;
        text-align: center !important;
        color: white !important;
        width: 100% !important;
    }
    
    .stTextInput div div input {
        text-align: center !important;
        border-radius: 12px !important;
        background-color: rgba(0,0,0,0.3) !important;
        color: white !important;
    }

    /* FORZAR CENTRADO DEL BOTÓN */
    .stButton {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
        margin-top: 20px !important;
    }

    .stButton > button {
        background: #3b82f6 !important;
        color: white !important;
        padding: 10px 40px !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)
