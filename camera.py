from enums import GameSettings
import pygame

class Camera:
    def __init__(self):
        self.camera_offset = pygame.Vector2(0, 0)

    def move(self, player_pos):
        screen_width = GameSettings.SCREEN_WIDTH.value
        screen_height = GameSettings.SCREEN_HEIGHT.value
        world_width = GameSettings.WORLD_WIDTH.value
        world_height = GameSettings.WORLD_HEIGHT.value
        player_dimension = GameSettings.PLAYER_SIZE.value

        # Calculate desired camera offset based on player position
        desired_x = player_pos.x - screen_width / 2 + player_dimension // 2
        desired_y = player_pos.y - screen_height / 2 + player_dimension // 2

        # Clamp the desired offset to the world's boundaries
        self.camera_offset.x = max(0, min(world_width - screen_width, desired_x))
        self.camera_offset.y = max(0, min(world_height - screen_height, desired_y))

    def get_offset(self):
        return self.camera_offset
