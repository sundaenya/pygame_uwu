import pygame
import math
from enums import GameSettings
from explosion import Explosion
import render
import sound

class Bomb(pygame.sprite.Sprite):
    def __init__(self, player, target, color, speed, damage, fuse):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('data/Bomb_Flask.png'), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = player.rect.center
        self.speed = speed
        self.fuse = fuse
        try:
            angle = math.atan2(target.rect.centery - player.rect.centery, target.rect.centerx - player.rect.centerx)
            self.dx = math.cos(angle) * self.speed
            self.dy = math.sin(angle) * self.speed
        except:
            self.dx = 0
            self.dy = -self.speed
        self.damage = 0
        self.bomb_damage = damage

    def update(self):
        self.fuse -= 1
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.rect.bottom < 0 or self.rect.top > GameSettings.WORLD_HEIGHT or self.rect.left > GameSettings.WORLD_WIDTH or self.rect.right < 0:
            self.kill()
        if self.fuse <= 0:
            self.explode()

    def explode(self):
        s = pygame.mixer.Sound('data/sounds/bomb.wav')
        s.set_volume(0.3)
        s.play()
        render.add_to_group('pbullets', Explosion(self, 200, self.bomb_damage, 20))
        self.kill()