import pygame
from enums import GameSettings
import sound
import render

class Explosion(pygame.sprite.Sprite):
    def __init__(self, target, diameter, damage, duration):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('data/Flask_Boom_Frame_1.png'), (diameter, diameter))
        self.rect = self.image.get_rect()
        self.rect.center = target.rect.center
        self.damage = damage
        self.duration = duration
        self.switch = True

    def update(self):
        self.duration -= 1
        if self.duration < 10 and self.switch:
            self.image = pygame.transform.scale(pygame.image.load('data/Flask_Boom_Frame_2.png'), (self.rect.width, self.rect.height))
            self.switch = False
        if self.duration <= 0:
            self.kill()