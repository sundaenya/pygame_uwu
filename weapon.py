import math
import pygame
from beam import Beam
from bullet import Bullet
import render
from wisp import Wisp

class Weapon(pygame.sprite.Sprite):
    def __init__(self, firerate, bullet_type, active):
        super().__init__()
        self.firerate = firerate
        self.bullet_type = bullet_type
        self.active = active
        self.rate = firerate


    def fire(self, player, target):
        if self.active:
            self.rate -= 1
            if self.rate < 0:
                match self.bullet_type:
                    case 'bullet':
                        render.add_to_group('bullets', Bullet(player, target, (255, 0, 0), 20, 1))
                    case 'beam':
                        render.add_to_group('other', Beam(player, target, (255, 0, 0)))
                        render.add_to_group('pbullets', Bullet(player, target, (0, 0, 0, 0), 50, 10))
                    case _:
                        pass
                self.rate = self.firerate