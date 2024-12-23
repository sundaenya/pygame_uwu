import pygame
import math

class Wisp(pygame.sprite.Sprite):
    def __init__(self, player, radius, speed):
        super().__init__()
        # self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        # pygame.draw.circle(self.image, (0, 255, 0), (5, 5), 25)  # Draw a green circle
        self.image = pygame.transform.scale(pygame.image.load('data/Wisp.png'), (50, 50))

        self.rect = self.image.get_rect()
        self.player = player
        self.radius = radius
        self.speed = speed
        self.angle = 0
        self.damage = 2

    def update(self):
        self.angle += self.speed  # Adjust this value to change the speed of orbit
        if self.angle >= 2 * math.pi:
            self.angle = 0

        # Calculate the new position of the bullet
        self.rect.centerx = self.player.rect.centerx + int(self.radius * math.cos(self.angle))
        self.rect.centery = self.player.rect.centery + int(self.radius * math.sin(self.angle))
