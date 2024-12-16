import pygame.display


class Camera():
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def draw(self, target_pos):
        self.offset.x = -(target_pos - 1280/2)
        for sprite in self:
            self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)