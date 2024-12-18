import sys
from tiles import *
from spritesheet import *
import random
import sound
import render
from beam import Beam
from player import Player
from enemy import Enemy
from bullet import Bullet
from camera import Camera
from enums import GameSettings
from collision import *
from spatial_grid import SpatialGrid
from wisp import Wisp
from random import randrange
from render import screen
from button import Button
import math

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

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("C:/Windows/Fonts/arial.ttf", size)

# Static objects class
class StaticObject(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)


for _ in range(10):  # Add 10 trees
    x = random.randint(100, world_width - 100)
    y = random.randint(100, world_height - 100)
    render.add_to_group('static_objects', StaticObject(tree_sprite, (x, y)))

for _ in range(10):  # Add 10 rocks
    x = random.randint(100, world_width - 100)
    y = random.randint(100, world_height - 100)
    render.add_to_group('static_objects', StaticObject(rock_sprite, (x, y)))


# Main game loop

def main():
    clock = pygame.time.Clock()
    sound.bg_music()
    min_range = 300
    player = Player(screen_width // 2, screen_height // 2)
    render.add_to_group(None, player)

    game_over = False

    FIRE = pygame.USEREVENT + 1
    pygame.time.set_timer(FIRE, 2000)

    SPAWN_ENEMY = pygame.USEREVENT + 2  # Define a new event
    pygame.time.set_timer(SPAWN_ENEMY, 100)

    wisp = Wisp(player, 250)
    render.add_to_group('pbullets', wisp)

    # Game loop
    running = True
    while running:
        # Handle events

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == FIRE:
                closest_enemy = player.get_closest_enemy(render.enemies)
                try:
                    if closest_enemy:
                        target_x, target_y = closest_enemy.get_pos()
                    else:
                        target_x, target_y = player.rect.centerx, player.rect.centery - 1
                        closest_enemy = (target_x, target_y)
                except:
                    target_x, target_y = player.rect.centerx, player.rect.centery - 1

                bullet = Bullet(player.rect.centerx, player.rect.centery, target_x, target_y)
                render.add_to_group('bullets', bullet)

            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouse_pos = pygame.mouse.get_pos()
                world_pos = (mouse_pos[0] + camera.get_offset().x, mouse_pos[1] + camera.get_offset().y)
                enemy_type = random.choice(['basic', 'heavy'])
                enemy = Enemy(world_pos, enemy_type, spatial_grid)
                render.add_to_group('enemies', enemy)

            # Randomly spawn enemies

            elif event.type == SPAWN_ENEMY and not game_over:
                while True:
        # Generate random spawn coordinates
                    spawn_x, spawn_y = randrange(world_width), randrange(world_height)

        # Calculate distance from the player
                    distance = math.sqrt((spawn_x - player.rect.centerx) ** 2 + (spawn_y - player.rect.centery) ** 2)

        # Break if the spawn point is far enough
                    if distance >= min_range:
                        break

    # Create the enemy after finding a valid spawn point
                enemy = Enemy((spawn_x, spawn_y), random.choice(('basic', 'heavy')), spatial_grid)

    # Add the enemy to the rendering group
                render.add_to_group('enemies', enemy)

        if not game_over:

            # for x in range (player.animationStops):
            #     screen.blit(player.animationList[x + 1])

            keys = pygame.key.get_pressed()
            player.update(keys)

            if keys[pygame.K_ESCAPE]:
                running = False
                pygame.quit()
            if keys[pygame.K_SPACE]:
                running = False

            for e in render.enemies:
                e.update(player)
                if check_collision(player, e):
                    player.damage(e.damage_amount)

                    if player.health <= 0:
                        game_over = True
            render.bullets.update()
            render.pbullets.update()

            check_bullet_collisions(render.bullets, render.enemies)
            check_pbullet_collisions(render.pbullets, render.enemies)

        render.render(camera, player)
        camera.move(player.rect)

        # Display 'You Lose' message if game is over
        if game_over:
            render.show_message('You Lose', (255, 255, 255), screen_width // 2 - 100, screen_height // 2 - 50)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False
                pygame.quit()

        clock.tick(60)

def main_menu():
    pygame.display.set_caption('Menu')

    image = pygame.image.load('data/button.png')

    w = 400
    h = 300

    n_image = pygame.transform.scale(image, (w,h))

    while True:
        # screen.blit(bg, (0,0)) 
        screen.fill((0, 0 , 255))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render('MAIN MENU', True, '#b68f40')
        MENU_RECT = MENU_TEXT.get_rect(center=(screen_width//2, 100))

        PLAY_BUTTON =  Button(image = n_image, 
                              pos = (screen_width//2, 300), text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image= n_image, pos=(screen_width//2, 600), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image= n_image, pos=(screen_width//2, 900), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main()  
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


# Run the game
if __name__ == "__main__":
   main_menu()