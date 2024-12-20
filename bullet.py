import pygame
import math
from enums import GameSettings

class Bullet(pygame.sprite.Sprite):
    def __init__(self, player, target, color, speed, damage):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('data/Fire.png'), (20, 20))
        self.rect = self.image.get_rect()
        self.rect.center = player.rect.center
        self.speed = speed
        s = pygame.mixer.Sound('data/sounds/fireball.wav')
        s.set_volume(0.7)
        s.play()


        try:
            angle = math.atan2(target.rect.centery - player.rect.centery, target.rect.centerx - player.rect.centerx)
            self.dx = math.cos(angle) * self.speed
            self.dy = math.sin(angle) * self.speed
        except:
            self.dx = 0
            self.dy = -self.speed
        self.damage = damage

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.rect.bottom < 0 or self.rect.top > GameSettings.WORLD_HEIGHT or self.rect.left > GameSettings.WORLD_WIDTH or self.rect.right < 0:
            self.kill()
