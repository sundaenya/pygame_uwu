import pygame
import math
import enums

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 0), (5, 5), 5)  # Draw a yellow circle
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10

        # Calculate direction
        angle = math.atan2(target_y - y, target_x - x)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.rect.bottom < 0 or self.rect.top > enums.GameSettings.WORLD_HEIGHT.value or self.rect.left > enums.GameSettings.WORLD_WIDTH.value or self.rect.right < 0:
            self.kill()
    
    def die(self):
        self.kill()