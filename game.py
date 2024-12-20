import sys
from tiles import *
import random
import sound
import render
import weapon
from player import Player
from enemy import Enemy, EnemyType
from camera import Camera
from enums import GameSettings, Difficulty, Level
from collision import *
from spatial_grid import SpatialGrid
from wisp import Wisp
from random import randrange
from render import screen
from button import Button
import math
from sound import Sound

f = open("./data/score.txt", "r")
highscore = f.read()

pygame.init()

os.chdir(os.path.dirname(__file__))
data_path = os.path.join("data", "Kibty.png")
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

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
    spatial_grid.clear()

    if hasattr(render, 'enemies'):
        render.enemies.empty()

    global enemies
    if 'enemies' in globals():
        enemies.clear()


class StaticObject(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)


player = Player(world_width // 2, world_width // 2)
enemies = [player]
weapon.active_weapon_list = weapon.weapon_list[:1]

for _ in range(10):
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
            newTree = Enemy((x, y), EnemyType.TREE, spatial_grid, player)
            enemies.append(newTree)
            render.add_to_group('enemies', newTree)
            break


def set_difficulty(xp):
    if xp < Level.ONE:
        difficulty = Difficulty.EASY
        weapon.active_weapon_list = []
    elif Level.ONE < xp < Level.TWO:
        difficulty = Difficulty.MEDIUM
        weapon.active_weapon_list = weapon.weapon_list[:1]
    elif Level.TWO < xp < Level.THREE:
        difficulty = Difficulty.HARD
        weapon.active_weapon_list = weapon.weapon_list[:2]
    elif Level.THREE < xp < Level.FOUR:
        difficulty = Difficulty.EXTREMELY_HARD
        weapon.active_weapon_list = weapon.weapon_list[:3]
    elif Level.FOUR < xp:
        difficulty = Difficulty.IMPOSSIBLE
        weapon.active_weapon_list = weapon.weapon_list[:4]

    return difficulty


def reset_game():
    global player, game_over, spatial_grid
    player = Player(100, 100)
    player.xp = 0
    game_over = False
    render.bullets.empty()
    render.pbullets.empty()
    render.enemies.empty()
    render.other.empty()
    render.static_objects.empty()
    render.all_sprites.empty()

    clear_all_enemies()
    main_menu()


sound = Sound()


def main():
    clock = pygame.time.Clock()
    min_range = 500
    player = Player(screen_width // 2, screen_height // 2)
    render.add_to_group(None, player)
    game_over = False

    wisp = Wisp(player, 200, 0.1)
    render.add_to_group('pbullets', wisp)

    FIRE = pygame.USEREVENT + 1
    pygame.time.set_timer(FIRE, 100)

    SPAWN_ENEMY = pygame.USEREVENT + 2
    pygame.time.set_timer(SPAWN_ENEMY, 100)

    render.add_to_group('pbullets', wisp)
    difficulty = set_difficulty(player.xp)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == FIRE:

                if not game_over:
                    closest_enemy = player.get_closest_enemy(render.enemies)
                    for w in weapon.active_weapon_list:
                        w.fire(player, closest_enemy)

            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouse_pos = pygame.mouse.get_pos()
                world_pos = (mouse_pos[0] + camera.get_offset().x, mouse_pos[1] + camera.get_offset().y)
                enemy_type = random.choice([EnemyType.FOX, EnemyType.CRAB, EnemyType.MUSHROOM])
                enemy = Enemy(world_pos, enemy_type, spatial_grid, player)
                render.add_to_group('enemies', enemy)

            elif event.type == SPAWN_ENEMY and not game_over and render.get_enemy_number() < 25 * difficulty:
                while True:
                    spawn_x, spawn_y = randrange(world_width), randrange(world_height)
                    distance = math.sqrt((spawn_x - player.rect.centerx) ** 2 + (spawn_y - player.rect.centery) ** 2)
                    if distance >= min_range:
                        break

                if render.get_number_of_trees() < 10 * difficulty:
                    render.add_to_group('enemies', Enemy((spawn_x, spawn_y), EnemyType.TREE, spatial_grid, player))
                enemy = Enemy((spawn_x, spawn_y), random.choice((EnemyType.FOX, EnemyType.CRAB, EnemyType.MUSHROOM)),
                              spatial_grid, player)
                render.add_to_group('enemies', enemy)

        if not game_over:
            keys = pygame.key.get_pressed()
            player.update(keys)

            if keys[pygame.K_ESCAPE]:
                reset_game()
                main_menu()
            if keys[pygame.K_SPACE]:
                running = False
                sys.exit()
            if keys[pygame.K_m]:
                camera.shake(20, 5)

            if keys[pygame.K_1]:
                player.xp = 0
            elif keys[pygame.K_2]:
                player.xp = 26
            elif keys[pygame.K_3]:
                player.xp = 76
            elif keys[pygame.K_4]:
                player.xp = 151
            elif keys[pygame.K_5]:
                player.xp = 251

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

        render.render(camera, player, highscore)
        camera.move(player.rect)

        if game_over:
            render.show_message('You Lose', (255, 255, 255), screen_width // 2 - 100, screen_height // 2 - 50)
            pygame.display.update()
            # render.render(camera, player)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                if player.xp > int(highscore):
                    file = open("./data/score.txt", "w")
                    file.write(str(player.xp))
                reset_game()
                return

        clock.tick(60)


os.chdir(os.path.dirname(__file__))
data_path = os.path.join("data", "Button_Frame_.png")


def options():
    image = pygame.image.load(data_path)

    w = 400
    h = 300

    n_image = pygame.transform.scale(image, (w, h))
    while True:
        map_image = pygame.image.load("data/128map.png")

        screen.blit(map_image, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # OPTIONS_TEXT = get_font(50).render('OPTIONS', True, 'white')
        # OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(screen_width // 2, 100))
        # screen.blit(OPTIONS_TEXT, OPTIONS_RECT)
        keys = pygame.key.get_pressed()

        SCREEN_BUTTON = Button(image=n_image,
                               pos=(screen_width // 2, 300), text_input="PLAY", font=get_font(75), base_color="#d7fcd4",
                               hovering_color="White")
        VOLUP_BUTTON = Button(image=n_image, pos=(screen_width // 2, 600),
                              text_input="+VOL", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        VOLDOWN_BUTTON = Button(image=n_image, pos=(screen_width // 2, 900),
                                text_input="-VOL", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        for button in [SCREEN_BUTTON, VOLUP_BUTTON, VOLDOWN_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SCREEN_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main()
                if VOLUP_BUTTON.checkForInput(MENU_MOUSE_POS):
                    sound.volume += 0.05
                    sound.bg_music(sound.volume)
                if VOLDOWN_BUTTON.checkForInput(MENU_MOUSE_POS):
                    sound.volume -= 0.05
                    sound.bg_music(sound.volume)
                # if VOLDOWN_BUTTON.checkForInput(MENU_MOUSE_POS):
                #     main()
        pygame.display.update()


def main_menu():
    pygame.display.set_caption('Menu')

    image = pygame.image.load(data_path)

    w = 400
    h = 300

    n_image = pygame.transform.scale(image, (w, h))

    while True:
        map_image = pygame.image.load("data/Title.png")
        map_image = pygame.transform.scale(map_image, (screen_width, screen_height))

        screen.blit(map_image, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # MENU_TEXT = get_font(50).render('MAIN MENU', True, 'white')
        # MENU_RECT = MENU_TEXT.get_rect(center=(screen_width // 2, 100))

        PLAY_BUTTON = Button(image=n_image,
                             pos=(screen_width // 2, 625), text_input="PLAY", font=get_font(75), base_color="#d7fcd4",
                             hovering_color="White")
        OPTIONS_BUTTON = Button(image=n_image, pos=(screen_width // 2, 800),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=n_image, pos=(screen_width // 2, 975),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        # screen.blit(MENU_TEXT, MENU_RECT)

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
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


if __name__ == "__main__":
    main_menu()
