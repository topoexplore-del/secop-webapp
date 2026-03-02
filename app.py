st.markdown("""
    <style>
    /* 1. Fondo y contenedor principal */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)),
                    url('https://images.unsplash.com/photo-1556155092-490a1ba16284?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80')
                    center/cover no-repeat fixed;
    }

    /* 2. Centrado Absoluto del Login Box */
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
        border: 1px solid rgba(255, 255, 255, 0.1);
        max-width: 650px;
        box-shadow: 0 25px 50px rgba(0,0,0,0.5);
        text-align: center;
    }

    /* 3. Ajuste de Textos */
    .login-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: 1px;
        color: #ffffff;
        margin-bottom: 5px;
    }
    .login-subtitle {
        font-size: 1.1rem;
        color: #3b82f6; /* Azul vibrante */
        margin-bottom: 25px;
        font-weight: 500;
        text-transform: uppercase;
    }
    .author {
        font-size: 1rem;
        color: rgba(255,255,255,0.7);
        margin-bottom: 40px;
        line-height: 1.5;
    }

    /* 4. Inputs centrados */
    .stTextInput {
        width: 100% !important;
    }
    .stTextInput label {
        color: white !important;
        justify-content: center !important;
        display: flex !important;
        font-weight: 300 !important;
        margin-bottom: 10px !important;
    }
    .stTextInput div div input {
        background: rgba(0, 0, 0, 0.3) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 12px !important;
        color: white !important;
        text-align: center !important;
        height: 50px !important;
    }

    /* 5. EL BOTÓN: Centrado forzado */
    .stButton {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
        margin-top: 10px;
    }
    .stButton button {
        width: 200px !important; /* Ancho fijo para que se vea elegante */
        background: linear-gradient(90deg, #1e40af, #3b82f6) !important;
        border: none !important;
        padding: 10px 24px !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.4s ease !important;
    }
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 20px rgba(59, 130, 246, 0.4) !important;
    }
    </style>
""", unsafe_allow_html=True)
