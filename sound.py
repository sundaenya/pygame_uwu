import pygame

def bg_music(volume):
    pygame.mixer.music.load('data/sounds/Universal Collapse.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(volume)

def play(path, volume):
    s = pygame.mixer.Sound(path)
    s.set_volume(volume)
    s.play()
    
