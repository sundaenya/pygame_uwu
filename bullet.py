import pygame
import math
from enums import GameSettings
import sound
import render

class Bullet(pygame.sprite.Sprite):
    def __init__(self, player, target):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 0), (5, 5), 5)  # Draw a yellow circle
        self.rect = self.image.get_rect()
        self.rect.center = player.rect.center
        self.speed = 20
        # sound.play('data/sounds/pew.wav', 0.2)

        try:
            angle = math.atan2(target.rect.centery - player.rect.centery, target.rect.centerx - player.rect.centerx)
            self.dx = math.cos(angle) * self.speed
            self.dy = math.sin(angle) * self.speed
        except:
            self.dx = 0
            self.dy = -self.speed
        self.damage = 1

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.rect.bottom < 0 or self.rect.top > GameSettings.WORLD_HEIGHT or self.rect.left > GameSettings.WORLD_WIDTH or self.rect.right < 0:
            self.kill()
