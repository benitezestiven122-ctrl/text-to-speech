import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64
from pydub import AudioSegment  # Importamos pydub para los efectos

st.title("Conversión de Texto a Audio con Efectos")

# Manejo de la imagen (comentado por si no tienes el archivo a mano)
try:
    image = Image.open('gato_raton.png')
    st.image(image, width=350)
except FileNotFoundError:
    st.warning("Imagen 'gato_raton.png' no encontrada.")

with st.sidebar:
    st.subheader("Escribe y/o selecciona texto para ser escuchado.")

# Crear carpeta temporal si no existe
if not os.path.exists("temp"):
    os.mkdir("temp")

st.subheader("Una pequeña Fábula.")
st.write('¡Ay! -dijo el ratón-. El mundo se hace cada día más pequeño. Al principio era tan grande que le tenía miedo. '  
         ' Corría y corría y por cierto que me alegraba ver esos muros, a diestra y siniestra, en la distancia. ' 
         ' Pero esas paredes se estrechan tan rápido que me encuentro en el último cuarto y ahí en el rincón está '  
         ' la trampa sobre la cual debo pasar. Todo lo que debes hacer es cambiar de rumbo dijo el gato...y se lo comió. ' 
         '\n\n Franz Kafka.')
           
st.markdown("¿Quieres escucharlo? Copia el texto o escribe el tuyo.")
text = st.text_area("Ingrese el texto a escuchar:")

# Selección de idioma
option_lang = st.selectbox("Selecciona el lenguaje", ("Español", "English"))
lg = 'es' if option_lang == "Español" else 'en'

# Función para generar el audio base con gTTS
def text_to_speech(text, lg):
    tts = gTTS(text, lang=lg)
    # Generar un nombre de archivo seguro
    my_file_name = "".join(x for x in text[0:15] if x.isalnum())
    if not my_file_name:
        my_file_name = "audio"
    
    base_path = f"temp/{my_file_name}.mp3"
    tts.save(base_path)
    return base_path, my_file_name

# Función para aplicar efectos de sonido
def aplicar_efecto(audio_path, efecto):
    audio = AudioSegment.from_mp3(audio_path)
    
    if efecto == "Rápido":
        # Aumenta la velocidad (y hace la voz más aguda)
        nuevo_frame_rate = int(audio.frame_rate * 1.5)
        audio = audio._spawn(audio.raw_data, overrides={'frame_rate': nuevo_frame_rate}).set_frame_rate(audio.frame_rate)
    
    elif efecto == "Lento":
        # Disminuye la velocidad (y hace la voz más grave)
        nuevo_frame_rate = int(audio.frame_rate * 0.7)
        audio = audio._spawn(audio.raw_data, overrides={'frame_rate': nuevo_frame_rate}).set_frame_rate(audio.frame_rate)
    
    elif efecto == "Eco":
        # Crea un eco superponiendo el audio con un retraso y menor volumen
        eco = audio - 10  # Reducimos 10 decibelios
        audio = audio.overlay(eco, position=300)  # Retraso de 300 ms
        
    elif efecto == "Reversa":
        # Invierte el audio
        audio = audio.reverse()

    # Guardar el nuevo archivo con el efecto aplicado
    nuevo_path = audio_path.replace(".mp3", f"_{efecto}.mp3")
    audio.export(nuevo_path, format="mp3")
    return nuevo_path

# Botones de efectos
st.write("### Selecciona el efecto y genera el audio:")
col1, col2, col3, col4, col5 = st.columns(5)

efecto_seleccionado = None

with col1:
    if st.button("Normal"): efecto_seleccionado = "Normal"
with col2:
    if st.button("Rápido"): efecto_seleccionado = "Rápido"
with col3:
    if st.button("Lento"): efecto_seleccionado = "Lento"
with col4:
    if st.button("Eco"): efecto_seleccionado = "Eco"
with col5:
    if st.button("Reversa"): efecto_seleccionado = "Reversa"

# Si el usuario hace clic en algún botón
if efecto_seleccionado:
    if text.strip() == "":
        st.warning("Por favor, ingresa un texto primero.")
    else:
        with st.spinner("Generando audio..."):
            # 1. Generar audio base
            base_path, file_name = text_to_speech(text, lg)
            
            # 2. Aplicar el efecto seleccionado
            final_path = aplicar_efecto(base_path, efecto_seleccionado)
            
            # 3. Mostrar el reproductor de audio
            with open(final_path, "rb") as audio_file:
                audio_bytes = audio_file.read()
                st.markdown(f"## Tu audio ({efecto_seleccionado}):")
                st.audio(audio_bytes, format="audio/mp3")

                # 4. Botón de descarga de Streamlit (más moderno y seguro que HTML custom)
                st.download_button(
                    label=f"Descargar Audio {efecto_seleccionado}",
                    data=audio_bytes,
                    file_name=f"{file_name}_{efecto_seleccionado}.mp3",
                    mime="audio/mp3"
                )

# Limpieza de archivos antiguos
def remove_files(n):
    mp3_files = glob.glob("temp/*.mp3")
    if mp3_files:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)

remove_files(7)
