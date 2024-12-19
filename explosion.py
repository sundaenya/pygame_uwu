import pygame
from enums import GameSettings
import sound
import render

class Explosion(pygame.sprite.Sprite):
    def __init__(self, target, diameter, damage, duration):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('data/explode.png'), (diameter, diameter))
        self.rect = self.image.get_rect()
        self.rect.center = target
        self.damage = damage
        self.duration = duration

    def update(self):
        self.duration -= 1
        if self.duration <= 0:
            self.kill()