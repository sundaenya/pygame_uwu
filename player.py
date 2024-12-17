import pygame
from enums import GameSettings

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.size = GameSettings.PLAYER_SIZE
        self.image = pygame.transform.scale(pygame.image.load('./data/Kibty.png'), (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5


    def update(self, keys):
        world_width = GameSettings.WORLD_WIDTH 
        world_height = GameSettings.WORLD_HEIGHT 

        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed


        self.rect.x = max(0, min(world_width - self.size, self.rect.x))
        self.rect.y = max(0, min(world_height - self.size, self.rect.y))

    def get_closest_enemy(self, enemies):
        pos = pygame.math.Vector2(self.rect.x, self.rect.y)
        try:
            return min([e for e in enemies], key=lambda e: pos.distance_to(pygame.math.Vector2(e.rect.centerx, e.rect.centery)))
        except:
            return None
        
        # TODO Fix

