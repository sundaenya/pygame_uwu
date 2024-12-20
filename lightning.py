import pygame
from bullet import Bullet
from enums import GameSettings
from explosion import Explosion
import sound
import render

class Lightning(pygame.sprite.Sprite):
    def __init__(self, target, damage):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('data/lightning.png'), (700, 2000))
        self.rect = self.image.get_rect()
        self.rect.centerx = target.rect.centerx
        self.rect.midbottom = target.rect.center
        self.damage = damage
        self.duration = 30
        render.add_to_group('bullets', Bullet(target,target, (0, 0, 0, 0), 0, self.damage))
        render.add_to_group('pbullets', Explosion(target, 200, 2, 20))

    def update(self):
        self.duration -= 1
        if self.duration <= 0:
            self.kill()