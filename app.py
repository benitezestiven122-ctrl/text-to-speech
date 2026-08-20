import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

# --- NUEVOS TEXTOS DE AUTOAYUDA Y MOTIVACIÓN ---
st.title("Tu Espacio de Inspiración y Calma 🌻")

# Nota: Recuerda cambiar 'gato_raton.png' por una imagen acorde al tema (ej. un paisaje, meditación, etc.)
# Si no tienes la imagen en tu carpeta, Streamlit mostrará un error, asegúrate de agregarla.
try:
    image = Image.open('motivacion.png')
    st.image(image, width=350)
except:
    pass # Evita que la app falle si aún no pones una imagen llamada motivacion.png

with st.sidebar:
    st.subheader("Escribe o selecciona afirmaciones positivas para escucharlas en voz alta y reprogramar tu mente.")

try:
    os.mkdir("temp")
except:
    pass

st.subheader("Reflexión del Día ✨")
st.write('Respira profundamente. Recuerda que cada día es una nueva oportunidad para empezar de nuevo. '  
         'No importa qué tan lento parezca tu progreso, lo importante es que sigues avanzando. ' 
         'Eres más fuerte de lo que crees, tienes la capacidad de superar los retos y mereces '  
         'todo lo bueno que el universo tiene para ti. Confía en tu proceso, suelta lo que no puedes ' 
         'controlar y abraza el momento presente.' 
         '\n\n- Tu voz interior.'
        )
            
st.markdown(f"¿Necesitas escuchar esto hoy? Copia el texto de arriba o escribe tus propias palabras.")
text = st.text_area("Ingresa el mensaje que necesitas escuchar hoy:")

tld='com'
option_lang = st.selectbox(
    "Selecciona el idioma de tu voz:",
    ("Español", "English"))

if option_lang=="Español":
    lg='es'
if option_lang=="English":
    lg='en'


# --- LÓGICA DE TEXT TO SPEECH (INTACTA) ---
def text_to_speech(text, tld, lg):
    
    tts = gTTS(text,lang=lg) # tts = gTTS(text,'en', tld, slow=False)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, text


#display_output_text = st.checkbox("Verifica el texto")

if st.button("Escuchar Mensaje"):
     result, output_text = text_to_speech(text, 'com',lg)#'tld
     audio_file = open(f"temp/{result}.mp3", "rb")
     audio_bytes = audio_file.read()
     st.markdown(f"## Tu audio de bienestar:")
     st.audio(audio_bytes, format="audio/mp3", start_time=0)

     #if display_output_text:
     
     #st.write(f" {output_text}")
    
#if st.button("ElevenLAabs",key=2):
#     from elevenlabs import play
#     from elevenlabs.client import ElevenLabs
#     client = ElevenLabs(api_key="a71bb432d643bbf80986c0cf0970d91a", # Defaults to ELEVEN_API_KEY)
#     audio = client.generate(text=f" {output_text}",voice="Rachel",model="eleven_multilingual_v1")
#     audio_file = open(f"temp/{audio}.mp3", "rb")

     with open(f"temp/{result}.mp3", "rb") as f:
         data = f.read()

     def get_binary_file_downloader_html(bin_file, file_label='File'):
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
        return href
     st.markdown(get_binary_file_downloader_html("audio.mp3", file_label="Audio File"), unsafe_allow_html=True)

def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)

remove_files(7)
