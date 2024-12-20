import pygame
import math

class Beam(pygame.sprite.Sprite):
    def __init__(self, player, target, color):
        super().__init__()
        self.player = player
        self.target = target
        self.color = color
        self.bullets = pygame.sprite.Group()
        self.lifespan = 3
        try:
            self.angle = math.atan2(target.rect.centery - player.rect.centery, target.rect.centerx - player.rect.centerx)
        except:
            self.angle = 0
        self.damage = 1
        self.create_beam()
        s = pygame.mixer.Sound('data/sounds/pew.wav')
        s.set_volume(0.5)
        s.play()

    def create_beam(self):
        beam_length = 1500  # Define the length of the beam
        beam_width = 30  # Define the width of the beam
        start_pos = (self.player.rect.centerx, self.player.rect.centery)
        
        self.image = pygame.transform.scale(pygame.image.load('data/beam.png'), (beam_length, beam_width))
        # Create a surface for the beam
        # self.image = pygame.Surface((beam_length, beam_width), pygame.SRCALPHA)
        # self.image.fill(self.color)  # Fill the beam with the specified color
        
        # Rotate the beam surface to match the angle
        self.image = pygame.transform.rotate(self.image, -math.degrees(self.angle))
        
        # Set the position of the beam
        self.rect = self.image.get_rect()
        self.rect.center = start_pos

        # Adjust the position to start from the player
        offset_x = beam_length / 2 * math.cos(self.angle)
        offset_y = beam_length / 2 * math.sin(self.angle)
        self.rect.centerx += offset_x
        self.rect.centery += offset_y

    def update(self):
        if self.lifespan <= 0:
            self.kill()
        self.lifespan -= 1
