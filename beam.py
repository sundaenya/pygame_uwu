import pygame
import render

class Beam(pygame.sprite.Sprite):
    def __init__(self, player, target):
        super().__init__()
        self.player = player
        self.target = target
        self.lifetime = 30  # Lifetime of the beam in frames
        self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.update_rect()

    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()
        self.update_rect()

    def update_rect(self):
        self.rect = pygame.Rect(player_center, (1, 1)).union(pygame.Rect(target_center, (1, 1)))
        pygame.draw.line(render.screen, (0,0,255), player_center, target_center)