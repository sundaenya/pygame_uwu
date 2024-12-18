# enemy.py

import pygame
import math
from spatial_grid import SpatialGrid  # Ensure this import is correct based on your project structure

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, etype, grid):
        super().__init__()
        self.type = etype
        match self.type:
            case 'basic':
                self.original_image = pygame.transform.scale(pygame.image.load('./data/Crab_Frame_1.png'), (50, 50))
                self.speed = 3
                self.health = 5
                self.damage_amount = 2
            case 'heavy':
                self.original_image = pygame.transform.scale(pygame.image.load('./data/Crab_Frame_1.png'), (200, 200))
                self.speed = 2
                self.health = 40
                self.damage_amount = 20
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.grid = grid  # Reference to the spatial grid
        self.grid.add(self)
        self.flash_time = 0

    def update(self, player):
        self.grid.update(self)

        if self.flash_time and pygame.time.get_ticks() - self.flash_time > 10:
            self.image = self.original_image.copy()
            self.flash_time = 0

        # Movement towards the player
        dx, dy = player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx, dy = dx / dist, dy / dist
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

        # Check and resolve overlaps
        overlapping_enemies = self.grid.get_nearby(self)
        for enemy in overlapping_enemies:
            if enemy != self and self.rect.colliderect(enemy.rect):
                self.resolve_overlap(enemy)

    def resolve_overlap(self, other):
        dx = self.rect.centerx - other.rect.centerx
        dy = self.rect.centery - other.rect.centery
        distance = math.hypot(dx, dy)
        if distance == 0:
            distance = 1
        overlap = (self.rect.width / 2 + other.rect.width / 2) - distance
        if overlap > 0:
            dx /= distance
            dy /= distance
            self.rect.x += dx * overlap / 2
            self.rect.y += dy * overlap / 2
            other.rect.x -= dx * overlap / 2
            other.rect.y -= dy * overlap / 2

    def damage(self, amount):
        self.health -= amount

        self.flash_red()

        if self.health <= 0:
            self.die()

    def flash_red(self):
        self.image.fill((255, 0, 0), special_flags=pygame.BLEND_ADD)
        self.flash_time = pygame.time.get_ticks()

    def die(self):
        self.grid.remove(self)
        self.kill()

    def get_pos(self):
        return self.rect.centerx, self.rect.centery
