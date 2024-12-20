import sys
from tiles import *
import random
import sound
import render
from player import Player
from enemy import Enemy, EnemyType
from camera import Camera
from enums import GameSettings, Difficulty, Level
from collision import *
from spatial_grid import SpatialGrid
from wave_attack import Wave_Attack
from weapon import Weapon
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

cell_size = 200
spatial_grid = SpatialGrid(cell_size, world_width, world_height)


def get_font(size):
    return pygame.font.Font('data/Grand9K Pixel.ttf', size)

def clear_all_enemies():
    # Clear spatial grid
    spatial_grid.clear()

    # Clear sprite group
    if hasattr(render, 'enemies'):
        render.enemies.empty()

    # Clear global list (if exists)
    global enemies
    if 'enemies' in globals():
        enemies.clear()


class StaticObject(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)


player = Player(screen_width // 2, screen_height // 2)

enemies = [player]

for _ in range(10):  # Add 10 trees
    while True:
        x = random.randint(100, world_width - 100)
        y = random.randint(100, world_height - 100)
        newTree = pygame.Rect((x, y), (1500, 1500))

        collision = False
        for i in enemies:
            if pygame.Rect.colliderect(newTree, i):
                collision = True
                break
        if not collision:
            newTree = Enemy((x, y), EnemyType.TREE, spatial_grid)
            enemies.append(newTree)
            render.add_to_group('enemies', newTree)
            break


def set_difficulty(xp):
    difficulty = Difficulty.EASY

    if Level.ONE < xp < Level.TWO:
        difficulty = Difficulty.MEDIUM
    elif Level.TWO < xp < Level.THREE:
        difficulty = Difficulty.HARD
    elif Level.THREE < xp < Level.FOUR:
        difficulty = Difficulty.EXTREMELY_HARD
    elif Level.FOUR < xp:
        difficulty = Difficulty.IMPOSSIBLE

    return difficulty

def reset_game():
    global player, game_over, spatial_grid
    player = Player(100, 100)  # Reset the player
    player.xp = 0
    game_over = False
    render.bullets.empty()
    render.pbullets.empty()
    render.enemies.empty()
    render.other.empty()
    render.static_objects.empty()
    render.all_sprites.empty()

    # Clear all enemies and other entities from the grid
    clear_all_enemies()

def main():
    clock = pygame.time.Clock()
    sound.bg_music(0.05)
    min_range = 500
    player = Player(screen_width // 2, screen_height // 2)
    render.add_to_group(None, player)

    game_over = False

    FIRE = pygame.USEREVENT + 1
    pygame.time.set_timer(FIRE, 100)

    SPAWN_ENEMY = pygame.USEREVENT + 2
    pygame.time.set_timer(SPAWN_ENEMY, 100)

    wisp = Wisp(player, 250, 0.5)
    render.add_to_group('pbullets', wisp)

    gun = Weapon(5, 'bullet', True)
    beam = Weapon(50, 'beam', True)
    running = True 
    while running:
        difficulty = set_difficulty(player.xp)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == FIRE:
                if not game_over:
                    closest_enemy = player.get_closest_enemy(render.enemies)
                    gun.fire(player, closest_enemy)
                    beam.fire(player, closest_enemy)

            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouse_pos = pygame.mouse.get_pos()
                world_pos = (mouse_pos[0] + camera.get_offset().x, mouse_pos[1] + camera.get_offset().y)
                enemy_type = random.choice([EnemyType.FOX, EnemyType.CRAB])
                enemy = Enemy(world_pos, enemy_type, spatial_grid)
                render.add_to_group('enemies', enemy)

            elif event.type == SPAWN_ENEMY and not game_over and render.get_enemy_number() < 25 * difficulty:
                while True:
                    spawn_x, spawn_y = randrange(world_width), randrange(world_height)
                    distance = math.sqrt((spawn_x - player.rect.centerx) ** 2 + (spawn_y - player.rect.centery) ** 2)
                    if distance >= min_range:
                        break

                if render.get_number_of_trees() < 10 * difficulty:
                    render.add_to_group('enemies', Enemy((spawn_x, spawn_y), EnemyType.TREE, spatial_grid))
                enemy = Enemy((spawn_x, spawn_y), random.choice((EnemyType.FOX, EnemyType.CRAB, EnemyType.MUSHROOM)), spatial_grid)
                render.add_to_group('enemies', enemy)

        if not game_over:
            keys = pygame.key.get_pressed()
            player.update(keys)

            if keys[pygame.K_ESCAPE]:
                running = False
                pygame.quit()
                sys.exit()
            if keys[pygame.K_SPACE]:
                running = False
                sys.exit()
            if keys[pygame.K_m]:
                camera.shake(20, 5)

            for e in render.enemies:
                e.update(player, camera)
                if check_collision(player, e):
                    player.damage(e.damage_amount)

                    if player.health <= 0:
                        game_over = True
            render.bullets.update()
            render.pbullets.update()
            render.other.update()

            check_bullet_collisions(render.bullets, render.enemies, player)
            check_pbullet_collisions(render.pbullets, render.enemies, player)

        render.render(camera, player)
        camera.move(player.rect)

        if game_over:
            render.show_message('You Lose', (255, 255, 255), screen_width // 2 - 100, screen_height // 2 - 50)
            pygame.display.update()
            # render.render(camera, player)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                # running = False
                # pygame.quit()
                # sys.exit()
                reset_game()
                return

        clock.tick(60)

os.chdir(os.path.dirname(__file__))
data_path = os.path.join("data", "Button_Frame_.png")

def main_menu():
    pygame.display.set_caption('Menu')

    image = pygame.image.load(data_path)

    w = 400
    h = 300

    n_image = pygame.transform.scale(image, (w, h))

    while True:
        # screen.blit(bg, (0,0)) 
        map_image = pygame.image.load("data/128map.png")

# Display the image at (0, 0)
        screen.blit(map_image, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render('MAIN MENU', True, '#b68f40')
        MENU_RECT = MENU_TEXT.get_rect(center=(screen_width // 2, 100))

        PLAY_BUTTON = Button(image=n_image,
                             pos=(screen_width // 2, 300), text_input="PLAY", font=get_font(75), base_color="#d7fcd4",
                             hovering_color="White")
        OPTIONS_BUTTON = Button(image=n_image, pos=(screen_width // 2, 600),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=n_image, pos=(screen_width // 2, 900),
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
