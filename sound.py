from playsound import playsound
import ipdb
from time import sleep

def speak_sound():
    playsound('src\ok.wav')
    sleep(0.3)

def start_sound():
    playsound('src\start.wav')
    sleep(0.3)

def end_sound():
    playsound('src\end.wav')
    sleep(0.3)
