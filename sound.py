import pygame

pygame.init()

class Sound:
    def __init__(self):
        self.volume = 0.05
        pygame.mixer.music.load('data/sounds/Universal Collapse.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(self.volume)
        self.sounds = {}

    def bg_music(self, volume):
        self.volume = volume
        pygame.mixer.music.set_volume(self.volume)


