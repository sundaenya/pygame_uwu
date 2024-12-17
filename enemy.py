import pygame
import math
import os

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, etype):
        super().__init__()
        self.type = etype
        match self.type:
            case 'basic':
                self.image = pygame.transform.scale(pygame.image.load('./data/crab.png'), (100,100))
                self.speed = 3
            case 'heavy':
                self.image = pygame.transform.scale(pygame.image.load('./data/crab.png'), (200,200))
                self.speed = 2

        self.rect = self.image.get_rect()
        self.rect.center = pos                

    def update(self, player):
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist

        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def die(self):
        self.kill()
    
    def get_pos(self):
        return self.rect.centerx, self.rect.centery
