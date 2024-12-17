import pygame

def bg_music():
    pygame.mixer.music.load('data/Universal Collapse.mp3')
    pygame.mixer.music.play(-1)

def play(path, volume):
    s = pygame.mixer.Sound(path)
    s.set_volume(volume)
    s.play()
    
