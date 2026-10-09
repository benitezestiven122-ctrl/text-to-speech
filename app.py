import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image

# ==========================================
# 1. CONFIGURACIÓN Y ESTILO (AUDIO STUDIO)
# ==========================================
st.set_page_config(
    page_title="Narrative-Synth | Voice-Overs",
    page_icon="🎙️",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #121212 !important;
        color: #E0E0E0 !important;
    }
    
    .script-box {
        background-color: #1E1E1E;
        padding: 20px;
        border-left: 4px solid #FF8C00;
        border-radius: 5px;
        margin-bottom: 20px;
        font-style: italic;
        color: #B0B0B0;
    }
    
    h1, h2, h3 { color: #FF8C00 !important; }
    
    .stButton > button {
        background-color: #FF8C00 !important;
        color: #121212 !important;
        border: none !important;
        font-weight: 600 !important;
        transition: 0.3s !important;
    }
    .stButton > button:hover {
        background-color: #FFA500 !important;
        box-shadow: 0 0 15px rgba(255, 140, 0, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Crear directorio temporal si no existe
os.makedirs("temp", exist_ok=True)

# ==========================================
# 2. INTERFAZ Y PARÁMETROS
# ==========================================
st.title("🎙️ Narrative-Synth: Voice-Over Studio")
st.markdown("Generador de monólogos atmosféricos, diálogos para NPCs en Unity y narraciones para animaciones 3D. Convierte tus guiones en **Assets de Audio** instantáneos.")

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/860/860368.png", width=80)
    st.subheader("Configuración del Sintetizador")
    st.caption("Ajusta los parámetros de salida de la voz neuronal.")
    
    option_lang = st.selectbox(
        "Idioma del Narrador:",
        ("Español (Latam/ES)", "English (US/UK)")
    )
    lg = 'es' if option_lang == "Español (Latam/ES)" else 'en'
    
    st.divider()
    st.write("💡 **Tip para Diseño Sonoro:**")
    st.write("Descarga este audio, expórtalo a Premiere o Ableton, bájale un poco el tono (Pitch) y agrégale un efecto de Reverb para crear voces de inteligencia artificial o pensamientos internos para tus cortometrajes.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Guion Cinematográfico / Spoken Word")
    
    script_ejemplo = (
        "Respira profundamente. Recuerda que cada día es una nueva oportunidad para empezar de nuevo. "
        "No importa qué tan lento parezca tu progreso, lo importante es que sigues avanzando. "
        "Eres más fuerte de lo que crees, tienes la capacidad de superar los retos y mereces "
        "todo lo bueno que el universo tiene para ti. Confía en tu proceso, suelta lo que no puedes "
        "controlar y abraza el momento presente."
    )
    
    st.markdown(f"""
    <div class="script-box">
        "{script_ejemplo}"
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.subheader("Caja de Texto (Input)")
    text = st.text_area(
        "Pega aquí tu guion, reflexión o diálogo:",
        value=script_ejemplo,
        height=200
    )

# ==========================================
# 3. LÓGICA DE SÍNTESIS DE AUDIO (TTS)
# ==========================================
def text_to_speech(text, lg):
    tts = gTTS(text, lang=lg, slow=False)
    # Nombre de archivo seguro usando Timestamp para evitar errores con caracteres especiales
    file_name = f"voice_asset_{int(time.time())}"
    file_path = f"temp/{file_name}.mp3"
    tts.save(file_path)
    return file_name, file_path

if st.button("RENDERIZAR AUDIO 🎛️", use_container_width=True):
    if text.strip():
        with st.spinner("Sintetizando frecuencias vocales..."):
            file_name, file_path = text_to_speech(text, lg)
            
            with open(file_path, "rb") as audio_file:
                audio_bytes = audio_file.read()
            
            st.success("✅ ¡Renderizado completado!")
            
            # Reproductor Nativo
            st.audio(audio_bytes, format="audio/mp3")
            
            # Botón de Descarga Nativo (Reemplaza el código Base64 antiguo)
            st.download_button(
                label="💾 Descargar Asset de Audio (MP3)",
                data=audio_bytes,
                file_name=f"{file_name}.mp3",
                mime="audio/mp3",
                type="primary"
            )
    else:
        st.warning("El guion está vacío. Escribe algo para generar el audio.")

# ==========================================
# 4. LIMPIEZA DE SERVIDOR
# ==========================================
def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)

remove_files(1) # Limpia archivos de más de 1 día de antigüedad
