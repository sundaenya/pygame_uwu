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

    # def load_sound(self, sound_name, file_path):
    #     self.sounds[sound_name] = pygame.mixer.Sound(file_path)
        

    # def play(self, sound_name, volume=None):
    #     if sound_name in self.sounds:
    #         sound = self.sounds[sound_name]
    #         if volume is not None:
    #             sound.set_volume(volume)
    #         sound.play()

