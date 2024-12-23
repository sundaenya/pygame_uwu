from typing import Literal
from enums import GameSettings
from spritesheet import *
from tiles import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (188, 71, 73)
GREEN = (107, 170, 117)

pygame.init()
bullets = pygame.sprite.Group()
pbullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
other = pygame.sprite.Group()
static_objects = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
font = pygame.font.SysFont(None, 55)
screen_width = GameSettings.SCREEN_WIDTH
screen_height = GameSettings.SCREEN_HEIGHT
world_width = GameSettings.WORLD_WIDTH
world_height = GameSettings.WORLD_HEIGHT

screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
pygame.display.set_caption('Amelia Earheart Simulator')
crab = pygame.image.load('data/crab.png')
spritesheet = Spritesheet('grassTileset.png')
canvas = pygame.image.load('./data/Double_Grass_test.png')
world_surface = pygame.Surface((world_width, world_height))
world_surface.fill("green")


def show_message(message, color, x, y):
    text = font.render(message, True, color)
    screen.blit(text, (x, y))


def draw_health_bar(x, y, max_health, current_health, bar_width, bar_height):
    current_health = max(0, current_health)
    health_percentage = current_health / max_health
    # pygame.draw.rect(screen, WHITE, (x, y, bar_width, bar_height), 2)
    pygame.draw.rect(screen, RED, (x, y, bar_width, bar_height))
    pygame.draw.rect(screen, GREEN, (x, y, bar_width * health_percentage, bar_height))
    # hp_bar = pygame.image.load("data/HP_Bar.png").convert_alpha()
    # hp_bar = pygame.transform.scale(hp_bar, (bar_width, bar_height + 50))
    # screen.blit(hp_bar,(x,y))


def add_to_group(group: Literal['bullets', 'pbullets', 'enemies', 'static_objects'], sprite):
    match group:
        case 'bullets':
            bullets.add(sprite)
        case 'pbullets':
            pbullets.add(sprite)
        case 'enemies':
            enemies.add(sprite)
        case 'static_objects':
            static_objects.add(sprite)
        case 'other':
            other.add(sprite)
        case _:
            pass
    all_sprites.add(sprite)


def get_enemy_number():
    return len(enemies)


def get_number_of_trees():
    number = 0
    for enemy in enemies:
        if enemy.type == 'tree':
            number += 1

    return number


def render(camera, player, highscore):
    screen.blit(canvas, (-camera.get_offset().x, -camera.get_offset().y))

    list = all_sprites.sprites()
    list.sort(key=lambda sprite: sprite.rect.bottom)

    for sprite in list:
        offset_pos = pygame.Vector2(sprite.rect.topleft) - camera.get_offset()
        screen.blit(sprite.image, offset_pos)

    # for obj in static_objects:
    #     offset_pos = obj.rect.topleft - camera.get_offset()
    #     screen.blit(obj.image, offset_pos)

    draw_health_bar(50, 50, GameSettings.PLAYER_HEALTH, player.health, 200, 20)
    show_message('Highscore: ' + highscore, WHITE, 1600, 50)
    show_message('Your XP: ' + str(player.xp), WHITE, 1600, 100)

    for enemy in enemies:
        if enemy.max_health != enemy.health:
            enemy_pos = enemy.get_pos() - camera.get_offset()
            # draw_health_bar(enemy_pos[0], enemy_pos[1] - 20, enemy.max_health, enemy.health, 50, 5)

    pygame.display.flip()