import time
from pytube_download import descargar
from transcripcion import procesar_audio
from raggi import rag_chat
import os
import warnings

import warnings
warnings.filterwarnings("ignore")


def mostrar_cargando(func, func_name, *args, **kwargs):
    print(f"Cargando {func_name}...", end="", flush=True)
    result = func(*args, **kwargs)
    print(f"\r{func_name} completado!      ")  # Limpiar la línea
    return result


url = "https://www.youtube.com/watch?v=tBaOQeyXYqg"
archivo = "audio.mp3"

os.system('cls')

# Llamada a la función de descarga con animación
nombre = mostrar_cargando(descargar, "Descarga", url, archivo)

os.system('cls')

# Llamada a la función de transcripción con animación
texto = mostrar_cargando(procesar_audio, "Transcripción", nombre, archivo)
os.system('cls')
print("Transcripcion terminada...")

rag_chat(texto)
