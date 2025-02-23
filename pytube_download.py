from pytubefix import YouTube
from pytubefix.cli import on_progress



def descargar(url, archivo):
    yt = YouTube(url, on_progress_callback=on_progress)

    print(yt.title)

    ys = yt.streams.get_audio_only()
    
    # Descargar el archivo con el nombre especificado
    ys.download(filename=archivo)

    
