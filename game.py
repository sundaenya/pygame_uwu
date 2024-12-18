import pygame
import sys
from tiles import *
from spritesheet import *
import random
import sound
import render
from player import Player
from enemy import Enemy
from bullet import Bullet
from camera import Camera
from enums import GameSettings
from collision import check_collision, check_bullet_collisions
from spatial_grid import SpatialGrid
from random import randrange  

# Initialize Pygame
pygame.init()

os.chdir(os.path.dirname(__file__))
data_path = os.path.join("data", "Kibty.png")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up the game window
screen_width = GameSettings.SCREEN_WIDTH
screen_height = GameSettings.SCREEN_HEIGHT
world_width = GameSettings.WORLD_WIDTH
world_height = GameSettings.WORLD_HEIGHT

camera = Camera()

# Initialize spatial grid
cell_size = 200  # Adjust cell size as needed
spatial_grid = SpatialGrid(cell_size, world_width, world_height)

tree_sprite = pygame.image.load('data/corrupted_tree.png')
rock_sprite = pygame.image.load('data/small_rock.png').convert_alpha()

# Scale sprites if needed
tree_sprite = pygame.transform.scale(tree_sprite, (200, 200))
rock_sprite = pygame.transform.scale(rock_sprite, (100, 100))
#static_objects = pygame.sprite.Group()

# Static objects class
class StaticObject(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)


for _ in range(10):  # Add 10 trees
    x = random.randint(100, world_width - 100)
    y = random.randint(100, world_height - 100)
    render.add_to_group('static_objects', StaticObject(tree_sprite, (x, y)) )

for _ in range(10):  # Add 10 rocks
    x = random.randint(100, world_width - 100)
    y = random.randint(100, world_height - 100)
    render.add_to_group('static_objects', StaticObject(rock_sprite, (x, y)))

# Main game loop
def main():
    clock = pygame.time.Clock()
    sound.bg_music()


    
    player = Player(screen_width // 2, screen_height // 2)
    render.add_to_group(None, player)
    enemy = Enemy((1000, 1000), 'basic', spatial_grid)  # Pass spatial_grid to Enemy

    game_over = False

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
                    closest_enemy = player.get_closest_enemy(render.enemies)
                    if closest_enemy:
                        target_x, target_y = closest_enemy.get_pos()
                    else:
                        target_x, target_y = player.rect.centerx, player.rect.centery - 1
                except:
                    target_x, target_y = player.rect.centerx, player.rect.centery - 1

                bullet = Bullet(player.rect.centerx, player.rect.centery, target_x, target_y)
                render.add_to_group('bullets', bullet)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                world_pos = (mouse_pos[0] + camera.get_offset().x, mouse_pos[1] + camera.get_offset().y)
                enemy_type = random.choice(['basic', 'heavy'])
                enemy = Enemy(world_pos, enemy_type, spatial_grid)
                render.add_to_group('enemies', enemy)
            
            # Randomly spawn enemies
            elif event.type == SPAWN_ENEMY and not game_over:

                spawn_x, spawn_y = randrange(world_width), randrange(world_height)

                while player.rect.collidepoint(spawn_x, spawn_y):
                    spawn_x, spawn_y = randrange(world_width), randrange(world_height)

                enemy = Enemy((spawn_x, spawn_y), random.choice(('basic', 'heavy')), spatial_grid)

                render.add_to_group('enemies', enemy)

           
        if not game_over:
            keys = pygame.key.get_pressed()
            player.update(keys)
            if keys[pygame.K_o]:
                hitbox = not hitbox

            for e in render.enemies:
                e.update(player)
                if check_collision(player, e):
                    player.damage(1)

                    if player.health == 0:
                        game_over = True
            render.bullets.update()

            check_bullet_collisions(render.bullets, render.enemies)  # Note: Ensure parameters are correct

        render.render(camera)
        camera.move(player.rect)
        render.draw_health_bar(50, 50, player.health, 100, 200, 20)
        
        
        # Display 'You Lose' message if game is over
        if game_over:
            render.show_message('You Lose', (255, 255, 255), screen_width // 2 - 100, screen_height // 2 - 50)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False
                pygame.quit()
            if keys[pygame.K_SPACE]:
                main()          
        
        # Cap the frame rate
        clock.tick(60)
        

# Run the game
if __name__ == "__main__":
    main()
