# game.py

import pygame
import sys
from tiles import *
from spritesheet import *
import random
import sound
from player import Player
from enemy import Enemy
from bullet import Bullet
from camera import Camera
from enums import GameSettings
from collision import check_collision, check_bullet_collisions
from spatial_grid import SpatialGrid

# Initialize Pygame
pygame.init()

from random import randrange  

# Initialize Pygame
pygame.init()

os.chdir(os.path.dirname(__file__))
data_path = os.path.join("data", "Kibty.png")

# Set up the game window


# Set up the game window
screen_width = GameSettings.SCREEN_WIDTH
screen_height = GameSettings.SCREEN_HEIGHT
world_width = GameSettings.WORLD_WIDTH
world_height = GameSettings.WORLD_HEIGHT
screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
pygame.display.set_caption('Amelia Earheart Simulator')
crab = pygame.image.load(data_path)

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


camera = Camera()

# Set up font
font = pygame.font.SysFont(None, 55)

canvas = pygame.Surface((world_width, world_height))
spritesheet = Spritesheet('grassTileset.png')
map1 = TileMap('data\grass.csv', spritesheet)
world_surface = pygame.Surface((world_width, world_height))
world_surface.fill("green")

# Initialize spatial grid
cell_size = 200  # Adjust cell size as needed
spatial_grid = SpatialGrid(cell_size, world_width, world_height)

# Function to display 'You Lose' text
def show_message(screen, message, color, x, y):
    text = font.render(message, True, color)
    screen.blit(text, (x, y))

def draw_health_bar(surface, x, y, current_health, max_health, bar_width, bar_height):
    # Ensure health doesn't go below 0
    current_health = max(0, current_health)

    # Calculate health bar fill percentage
    health_percentage = current_health / max_health

    # Outline of the health bar
    pygame.draw.rect(surface, WHITE, (x, y, bar_width, bar_height), 2)

    # Red background
    pygame.draw.rect(surface, RED, (x, y, bar_width, bar_height))

    # Green foreground (health remaining)
    pygame.draw.rect(surface, GREEN, (x, y, bar_width * health_percentage, bar_height))

# Main game loop
def main():
    clock = pygame.time.Clock()
    sound.bg_music()

    player = Player(screen_width // 2, screen_height // 2)
    enemy = Enemy((1000, 1000), 'basic', spatial_grid)  # Pass spatial_grid to Enemy

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player, enemy)

    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group(enemy)

    game_over = False
    hitbox = False

    FIRE  = pygame.USEREVENT + 1
    pygame.time.set_timer(FIRE, 200)

    SPAWN_ENEMY = pygame.USEREVENT + 2  # Define a new event
    pygame.time.set_timer(SPAWN_ENEMY, 100) 


    # Game loop
    running = True
    while running:
        # Handle events

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == FIRE:
                try:
                    closest_enemy = player.get_closest_enemy(enemies)
                    if closest_enemy:
                        target_x, target_y = closest_enemy.get_pos()
                    else:
                        target_x, target_y = player.rect.centerx, player.rect.centery - 1
                except:
                    target_x, target_y = player.rect.centerx, player.rect.centery - 1

                bullet = Bullet(player.rect.centerx, player.rect.centery, target_x, target_y)
                all_sprites.add(bullet)
                bullets.add(bullet)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                world_pos = (mouse_pos[0] + camera.get_offset().x, mouse_pos[1] + camera.get_offset().y)
                enemy_type = random.choice(['basic', 'heavy'])
                enemy = Enemy(world_pos, enemy_type, spatial_grid)
                enemies.add(enemy)
                all_sprites.add(enemy)
            
            # Randomly spawn enemies
            elif event.type == SPAWN_ENEMY and not game_over:

                spawn_x, spawn_y = randrange(world_width), randrange(world_height)

                while player.rect.collidepoint(spawn_x, spawn_y):
                    spawn_x, spawn_y = randrange(world_width), randrange(world_height)

                enemy = Enemy((spawn_x, spawn_y), random.choice(('basic', 'heavy')), spatial_grid)

                enemies.add(enemy)
                all_sprites.add(enemy)
           
        if not game_over:
            keys = pygame.key.get_pressed()
            player.update(keys)
            if keys[pygame.K_o]:
                hitbox = not hitbox

            for e in enemies:
                e.update(player)
                if check_collision(player, e):
                    player.damage(1)

                    if player.health == 0:
                        game_over = True
            bullets.update()

            check_bullet_collisions(bullets, enemies)  # Note: Ensure parameters are correct

        # Render world
        screen.blit(world_surface, (-camera.camera_offset.x, -camera.camera_offset.y))

        map1.draw_map(canvas)
        camera.move(player.rect)
        canvas.fill((0, 180, 240))  # Fills the entire screen with light blue
        map1.draw_map(canvas)
        screen.blit(canvas, (-camera.camera_offset.x, -camera.camera_offset.y))

        # Render all game objects relative to the camera offset
        for sprite in all_sprites:
            offset_pos = pygame.Vector2(sprite.rect.topleft) - camera.get_offset()
            screen.blit(sprite.image, offset_pos)

            if hitbox:
                pygame.draw.rect(screen, "red",pygame.Rect(offset_pos.x, offset_pos.y, sprite.rect.width, sprite.rect.height), width=2)

        draw_health_bar(screen, 50, 50, player.health, 100, 200, 20)

        # Display 'You Lose' message if game is over

        pygame.draw.rect(screen, "red",
                             pygame.Rect(offset_pos.x, offset_pos.y, sprite.rect.width, sprite.rect.height),width=2)


        # Display 'You Lose' message if game is over
        if game_over:
            show_message(screen, 'You Lose', WHITE, screen_width // 2 - 100, screen_height // 2 - 50)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False
                pygame.quit()
            if keys[pygame.K_SPACE]:
                main()          

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

# Run the game
if __name__ == "__main__":
    main()
