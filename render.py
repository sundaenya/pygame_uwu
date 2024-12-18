from typing import Literal
import pygame
from enemy import Enemy
from enums import GameSettings
from player import Player
from spatial_grid import SpatialGrid
from spritesheet import *
from tiles import *

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

pygame.init()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
static_objects = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
font = pygame.font.SysFont(None, 55)
screen_width = GameSettings.SCREEN_WIDTH
screen_height = GameSettings.SCREEN_HEIGHT
world_width = GameSettings.WORLD_WIDTH
world_height = GameSettings.WORLD_HEIGHT

# Set up the game window
screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
pygame.display.set_caption('Amelia Earheart Simulator')
crab = pygame.image.load('data/Kibty.png')
canvas = pygame.Surface((world_width, world_height))
spritesheet = Spritesheet('grassTileset.png')
canvas = pygame.image.load('./data/128map.png')
world_surface = pygame.Surface((world_width, world_height))
world_surface.fill("green")


def show_message(message, color, x, y):
    text = font.render(message, True, color)
    screen.blit(text, (x, y))


def draw_health_bar(x, y, current_health, max_health, bar_width, bar_height):
    current_health = max(0, current_health)
    health_percentage = current_health / max_health
    pygame.draw.rect(screen, WHITE, (x, y, bar_width, bar_height), 2)
    pygame.draw.rect(screen, RED, (x, y, bar_width, bar_height))
    pygame.draw.rect(screen, GREEN, (x, y, bar_width * health_percentage, bar_height))


def add_to_group(group: Literal['bullets', 'enemies', 'static_objects'], sprite):
    match group:
        case 'bullets':
            bullets.add(sprite)
        case 'enemies':
            enemies.add(sprite)
        case 'static_objects':
            static_objects.add(sprite)
        case _:
            pass
    all_sprites.add(sprite)


def render(camera):
    # Render world
    screen.blit(world_surface, (-camera.camera_offset.x, -camera.camera_offset.y))

    screen.blit(canvas, (-camera.get_offset().x, -camera.get_offset().y))

    # Render all game objects relative to the camera offset
    for sprite in all_sprites:
        offset_pos = pygame.Vector2(sprite.rect.topleft) - camera.get_offset()
        screen.blit(sprite.image, offset_pos)

    # draw_health_bar(screen, 50, 50, player.health, 100, 200, 20)

    # Display 'You Lose' message if game is over

    for obj in static_objects:
        offset_pos = obj.rect.topleft - camera.get_offset()
        screen.blit(obj.image, offset_pos)

    # Update the display
    pygame.display.flip()