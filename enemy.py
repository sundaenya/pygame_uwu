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
                self.image = pygame.transform.scale(pygame.image.load('./data/Crab_Frame_1.png'), (100, 100))
                self.speed = 3
                self.health = 5
            case 'heavy':
                self.image = pygame.transform.scale(pygame.image.load('./data/Crab_Frame_1.png'), (200, 200))
                self.speed = 2
                self.health = 10

        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.grid = grid  # Reference to the spatial grid
        self.grid.add(self)  # Add to the spatial grid

    def update(self, player):
        self.grid.update(self)  # Update spatial grid position

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
        if distance == 0:  # Prevent division by zero
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
        print(self.health)

        if self.health <= 0:
            self.die()

    def die(self):
        self.grid.remove(self)
        self.kill()

    def get_pos(self):
        return self.rect.centerx, self.rect.centery
