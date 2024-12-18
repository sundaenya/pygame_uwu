import pygame
import math
from bullet import Bullet

class Beam(pygame.sprite.Sprite):
    def __init__(self, player, target):
        super().__init__()
        self.player = player
        self.target = target
        self.bullets = pygame.sprite.Group()
        self.create_beam()

    def create_beam(self):
        player_center = self.player.rect.center
        target_center = self.target.rect.center
        distance = math.hypot(target_center[0] - player_center[0], target_center[1] - player_center[1])
        steps = int(distance / 5)  # Adjust spacing between circles here
        for step in range(steps):
            x = player_center[0] + (target_center[0] - player_center[0]) * (step / steps)
            y = player_center[1] + (target_center[1] - player_center[1]) * (step / steps)
            bullet = Bullet(x, y, x + self.target.rect.width, y + self.target.rect.height)
            bullet.speed_x = bullet.speed_y = 0  # Make bullets stationary
            self.bullets.add(bullet)

    def update(self):
        self.bullets.update()
        # Remove the beam after a certain lifetime
        if len(self.bullets) == 0:
            self.kill()
