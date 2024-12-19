import random
import pygame
import math
import sound
from enums import GameSettings


class EnemyType:
    MUSHROOM = "mushroom"
    FOX = "fox"
    CRAB = "crab"
    TREE = "tree"


class State:
    SLEEP = "sleep"
    AWAKE = "awake"
    MOVING = "moving"

class Direction:
    LEFT = "left"
    RIGHT = "right"


world_width = GameSettings.WORLD_WIDTH
world_height = GameSettings.WORLD_HEIGHT

TREE_SIZE = 350
BASIC_SIZE = 100
SHROOM_SIZE = 50
HEAVY_SIZE = 200


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, etype, grid):
        super().__init__()
        self.type = etype
        self.state = State.MOVING
        match self.type:
            case EnemyType.MUSHROOM:
                self.original_image = pygame.transform.scale(pygame.image.load('data/shroom/Shroom_Frame_1.png'),(SHROOM_SIZE, SHROOM_SIZE))
                self.speed = 5
                self.health = 3
                self.max_health = 3
                self.damage_amount = 2
                self.xp = 2
                self.walk_frame_1 = self.original_image.copy()
                self.walk_frame_2 = pygame.transform.scale(pygame.image.load('data/shroom/Shroom_Frame_2.png'),(SHROOM_SIZE, SHROOM_SIZE))
                self.walk_frame_3 = pygame.transform.scale(pygame.image.load('data/shroom/Shroom_Frame_3.png'),(SHROOM_SIZE, SHROOM_SIZE))
                self.current_frame = 1
                self.frame_timer = pygame.time.get_ticks()
            case EnemyType.FOX:
                self.original_image = pygame.transform.scale(pygame.image.load('data/fox/Fox_Frame_1.png'),(BASIC_SIZE, BASIC_SIZE))
                self.speed = 4
                self.health = 5
                self.max_health = 5
                self.damage_amount = 2
                self.xp = 2
                self.walk_frame_1 = self.original_image.copy()
                self.walk_frame_2 = pygame.transform.scale(pygame.image.load('data/fox/Fox_Frame_2.png'),(BASIC_SIZE, BASIC_SIZE))
                self.walk_frame_3 = pygame.transform.scale(pygame.image.load('data/fox/Fox_Frame_3.png'),(BASIC_SIZE, BASIC_SIZE))
                self.current_frame = 1
                self.frame_timer = pygame.time.get_ticks()
            case EnemyType.CRAB:
                self.original_image = pygame.transform.scale(pygame.image.load('data/crab/Crab_Frame_1.png'),(HEAVY_SIZE, HEAVY_SIZE))
                self.speed = 2
                self.health = 40
                self.max_health = 40
                self.damage_amount = 20
                self.xp = 5
                self.walk_frame_1 = self.original_image.copy()
                self.walk_frame_2 = pygame.transform.scale(pygame.image.load('data/crab/Crab_Frame_2.png'),(HEAVY_SIZE, HEAVY_SIZE))
                self.walk_frame_3 = pygame.transform.scale(pygame.image.load('data/crab/Crab_Frame_3.png'),(HEAVY_SIZE, HEAVY_SIZE))
                self.current_frame = 1
                self.frame_timer = pygame.time.get_ticks()
            case EnemyType.TREE:
                self.original_image = pygame.transform.flip(pygame.transform.scale(pygame.image.load('data/tree/Tree_Frame_1.png'), (TREE_SIZE, TREE_SIZE)),True, False)
                self.walk_frame_1 = pygame.transform.flip( pygame.transform.scale(pygame.image.load('data/tree/Tree_Frame_Walking_1.png'),(TREE_SIZE, TREE_SIZE)), True, False)
                self.walk_frame_2 = pygame.transform.flip(pygame.transform.scale(pygame.image.load('data/tree/Tree_Frame_Walking_2.png'),(TREE_SIZE, TREE_SIZE)), True, False)
                self.speed = 0
                self.health = 100
                self.max_health = 100
                self.damage_amount = 0
                self.xp = 20
                self.state = State.SLEEP
                self.countdown = 20
                self.current_frame = 1
                self.frame_timer = pygame.time.get_ticks()
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.grid = grid
        self.grid.add(self)
        self.flash_time = 0
        self.direction = Direction.RIGHT
        self.is_flashing = False

    def change_direction(self):
        self.original_image = pygame.transform.flip(self.original_image, True, False)
        self.image = pygame.transform.flip(self.image, True, False)
        if self.type == EnemyType.TREE:
            self.walk_frame_1 = pygame.transform.flip(self.walk_frame_1, True, False)
            self.walk_frame_2 = pygame.transform.flip(self.walk_frame_2, True, False)

        if self.type == EnemyType.FOX or self.type == EnemyType.CRAB or self.type == EnemyType.MUSHROOM:
            self.walk_frame_1 = pygame.transform.flip(self.walk_frame_1, True, False)
            self.walk_frame_2 = pygame.transform.flip(self.walk_frame_2, True, False)
            self.walk_frame_3 = pygame.transform.flip(self.walk_frame_3, True, False)

    def is_player_left_or_right(player, enemy):
        if player.rect.centerx < enemy.rect.centerx:
            return Direction.LEFT
        else:
            return Direction.RIGHT

    def update(self, player, camera):
        self.grid.update(self)

        if self.flash_time and pygame.time.get_ticks() - self.flash_time > 10:
            self.image = self.original_image.copy()
            self.flash_time = 0

        direction = self.is_player_left_or_right(player)
        if self.direction != direction and self.speed != 0:
            self.change_direction()
            self.direction = direction

        dx, dy = player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx, dy = dx / dist, dy / dist
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

        overlapping_enemies = self.grid.get_nearby(self)
        for enemy in overlapping_enemies:
            if enemy != self and self.rect.colliderect(enemy.rect):
                self.resolve_overlap(enemy)

        distance = self.get_distance(player.rect.center)

        if distance <= 500 and self.state == State.SLEEP and player.xp > 20:
            self.state = State.AWAKE
            camera.shake(50, 15)
            # sound.play('./data/sounds/earthquake1.mp3', 2)
            
            s = pygame.mixer.Sound('./data/sounds/earthquake1.mp3')
            s.set_volume(2)
            s.play()

            self.image = pygame.transform.flip(
                pygame.transform.scale(pygame.image.load('data/tree/Tree_Frame_wakeup1.png'), (TREE_SIZE, TREE_SIZE)),
                True, False)

        if self.type == EnemyType.TREE and self.state == State.AWAKE:
            self.countdown -= 1

        if self.type == EnemyType.TREE and self.countdown == 10:
            self.image = pygame.transform.flip(
                pygame.transform.scale(pygame.image.load('data/tree/Tree_Frame_wakeup2.png'),
                                       (TREE_SIZE + 1, TREE_SIZE + 1)), True, False)

        if self.type == EnemyType.TREE and self.countdown <= 0 and self.speed <= 0:
            self.speed = 1
            self.damage_amount = 25
            self.original_image = pygame.transform.flip(
                pygame.transform.scale(pygame.image.load('data/tree/Tree_Frame_Walking_2.png'), (TREE_SIZE, TREE_SIZE)),
                True, False)
            self.image = pygame.transform.flip(
                pygame.transform.scale(pygame.image.load('data/tree/Tree_Frame_Walking_2.png'), (TREE_SIZE, TREE_SIZE)),
                True, False)

        if self.type == EnemyType.TREE and self.state == State.AWAKE and self.speed > 0:
            current_time = pygame.time.get_ticks()
            if current_time - self.frame_timer >= 300:
                self.frame_timer = current_time
                self.current_frame = 2 if self.current_frame == 1 else 1
                self.image = self.walk_frame_1 if self.current_frame == 1 else self.walk_frame_2

        self.animation()

        if self.is_flashing:
            red_overlay = self.image.copy()
            red_overlay.fill((255, 0, 0), special_flags=pygame.BLEND_ADD)
            self.image = red_overlay

    def get_distance(self, player_pos):
        dx = self.rect.centerx - player_pos[0]
        dy = self.rect.centery - player_pos[1]
        return math.sqrt(dx ** 2 + dy ** 2)

    def animation(self):
        if self.type == EnemyType.MUSHROOM:
            current_time = pygame.time.get_ticks()
            if current_time - self.frame_timer >= 200:
                self.frame_timer = current_time

                self.current_frame = (self.current_frame % 4) + 1

                if self.current_frame == 1:
                    self.image = self.walk_frame_1
                elif self.current_frame == 2:
                    self.image = self.walk_frame_2
                elif self.current_frame == 3:
                    self.image = self.walk_frame_3
                else:
                    self.image = self.walk_frame_2

        if self.type == EnemyType.FOX:
            current_time = pygame.time.get_ticks()
            if current_time - self.frame_timer >= 150:
                self.frame_timer = current_time

                self.current_frame = (self.current_frame % 4) + 1

                if self.current_frame == 1:
                    self.image = self.walk_frame_1
                elif self.current_frame == 2:
                    self.image = self.walk_frame_2
                elif self.current_frame == 3:
                    self.image = self.walk_frame_3
                else:
                    self.image = self.walk_frame_2

        if self.type == EnemyType.CRAB:
            current_time = pygame.time.get_ticks()
            if current_time - self.frame_timer >= 200:
                self.frame_timer = current_time

                self.current_frame = (self.current_frame % 4) + 1

                if self.current_frame == 1:
                    self.image = self.walk_frame_1
                elif self.current_frame == 2:
                    self.image = self.walk_frame_2
                elif self.current_frame == 3:
                    self.image = self.walk_frame_3
                else:
                    self.image = self.walk_frame_2

    def resolve_overlap(self, other):
        dx = self.rect.centerx - other.rect.centerx
        dy = self.rect.centery - other.rect.centery
        distance = math.hypot(dx, dy)
        if distance == 0:
            distance = 1
        overlap = (self.rect.width / 2 + other.rect.width / 2) - distance
        if overlap > 0:
            dx /= distance
            dy /= distance
            if self.speed != 0:
                self.rect.x += dx * overlap / 2
                self.rect.y += dy * overlap / 2
            if other.speed != 0:
                other.rect.x -= dx * overlap / 2
                other.rect.y -= dy * overlap / 2

            if self.speed == 0 and other.speed == 0:
                self_x = random.randint(100, world_width - 100)
                other_x = random.randint(100, world_width - 100)
                self_y = random.randint(100, world_height - 100)
                other_y = random.randint(100, world_height - 100)
                self.rect.x += dx * self_x
                self.rect.y += dy * self_y
                other.rect.x -= dx * other_x
                other.rect.y -= dy * other_y

    def damage(self, amount, player):
        if self.speed == 0:
            return

        self.health -= amount

        # self.flash_red()

        if self.health <= 0:
            self.die()
            player.give_xp(self.xp)

    def flash_red(self):
        self.is_flashing = True
        self.flash_time = pygame.time.get_ticks()

    def die(self):
        self.grid.remove(self)
        self.kill()

    def get_pos(self):
        return self.rect.topleft
