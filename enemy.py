import pygame
import math
import os

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('./data/crab.png'), (100,100))  # Red color
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.speed = 2

    def update(self, player):
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist

        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def die(self):
        self.kill()
    
    def get_pos(self):
        return self.rect.x, self.rect.y
