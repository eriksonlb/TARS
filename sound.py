import pygame
import ipdb
from time import sleep

def speak_sound():
    pygame.init()
    sound = pygame.mixer.music.load('src\ok.mp3')
    pygame.mixer.music.play()
    sleep(0.3)