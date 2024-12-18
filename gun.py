import pygame
import bullet

class Gun(pygame.sprite.Sprite):
    def __init__(self, firerate, bullet_type):
        super().__init__()
        self.firerate = firerate
        self.bullet_type = bullet_type

"""
    def fire(self):
        bullet = Bullet(player.rect.centerx, player.rect.centery, target_x, target_y)
        all_sprites.add(bullet)
        bullets.add(bullet)
"""