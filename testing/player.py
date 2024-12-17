import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('data/Kibty.png'), (100,100))  # Blue color
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 5


    def update(self, keys):
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed

    def get_closest_enemy(self, enemies):
        pos = pygame.math.Vector2(self.rect.x, self.rect.y)
        try:
            return min([e for e in enemies], key=lambda e: pos.distance_to(pygame.math.Vector2(e.rect.x, e.rect.y)))
        except:
            return None
        
        # TODO Fix