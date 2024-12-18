import random
from enums import GameSettings
import pygame

class Camera:
    def __init__(self):
        self.camera_offset = pygame.Vector2(0, 0)
        self.shake_duration = 0
        self.shake_intensity = 0

    def move(self, player_pos):
        screen_width = GameSettings.SCREEN_WIDTH 
        screen_height = GameSettings.SCREEN_HEIGHT 
        world_width = GameSettings.WORLD_WIDTH 
        world_height = GameSettings.WORLD_HEIGHT 
        player_dimension = GameSettings.PLAYER_SIZE 

        # Calculate desired camera offset based on player position
        desired_x = player_pos.x - screen_width / 2 + player_dimension // 2
        desired_y = player_pos.y - screen_height / 2 + player_dimension // 2

        # Clamp the desired offset to the world's boundaries
        self.camera_offset.x = max(0, min(world_width - screen_width, desired_x))
        self.camera_offset.y = max(0, min(world_height - screen_height, desired_y))

        if self.shake_duration > 0:
            self.camera_offset.x += random.uniform(-self.shake_intensity, self.shake_intensity)
            self.camera_offset.y += random.uniform(-self.shake_intensity, self.shake_intensity)
            self.shake_intensity *= 0.90
            self.shake_duration -= 1

        if self.shake_intensity < 0.1:
            self.shake_intensity = 0
            self.shake_duration = 0

    def shake(self, duration, intensity):
        self.shake_duration = duration
        self.shake_intensity = intensity

    def get_offset(self):
        return self.camera_offset
