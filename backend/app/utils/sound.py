import os
import pygame
import logging

pygame.mixer.init()

def play_sound(sound_file):
    try:
        sound_path = os.path.join('assets/sounds', sound_file)
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()
    except Exception as e:
        logging.error(f"Error playing sound: {e}")
