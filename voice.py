from gtts import gTTS 
from playsound import playsound 
import json
import os.path
import ipdb
import unicodedata
import re

def remover_acentos(frase):
    nfkd = unicodedata.normalize('NFKD', frase)
    final_text = u"".join([c for c in nfkd if not unicodedata.combining(c)])
    final_text = re.sub('[^a-zA-Z0-9 \\\]', '', final_text)
    final_text = final_text.lower().replace(" ", "")
    return final_text

def reproduce(text):
    fixed_text = remover_acentos(text)
    if os.path.isfile(f"src\dialogue\{fixed_text[:14]}.mp3"):
        playsound(f"src\dialogue\{fixed_text}.mp3")
    else:
        set_audio = gTTS(text=text, lang='pt', slow=False)
        path = f"src\\dialogue\\{fixed_text[:14]}.mp3"
        set_audio.save(path)
        playsound(path)

    fixed_text = ""
        


