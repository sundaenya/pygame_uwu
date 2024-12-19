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
FOX_SIZE = 100
SHROOM_SIZE = 50
CRAB_SIZE = 200


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, etype, grid, player):
        super().__init__()
        self.type = etype
        self.state = State.MOVING
        self.frames = {
            'left': {'normal': [], 'red': []},
            'right': {'normal': [], 'red': []},
            'static': [],
        }
        match self.type:
            case EnemyType.MUSHROOM:
                self.original_image = pygame.transform.scale(pygame.image.load('data/shroom/Shroom_Frame_1.png'),
                                                             (SHROOM_SIZE, SHROOM_SIZE))
                self.frames['right']['normal'] = [
                    pygame.transform.scale(pygame.image.load('data/shroom/Shroom_Frame_1.png'),
                                           (SHROOM_SIZE, SHROOM_SIZE)),
                    pygame.transform.scale(pygame.image.load('data/shroom/Shroom_Frame_2.png'),
                                           (SHROOM_SIZE, SHROOM_SIZE)),
                    pygame.transform.scale(pygame.image.load('data/shroom/Shroom_Frame_3.png'),
                                           (SHROOM_SIZE, SHROOM_SIZE)),
                ]
                self.frames['right']['red'] = [
                    self._create_red_frame(frame) for frame in self.frames['right']['normal']
                ]
                self.frames['left']['normal'] = [
                    pygame.transform.flip(frame, True, False) for frame in self.frames['right']['normal']
                ]
                self.frames['left']['red'] = [
                    self._create_red_frame(frame) for frame in self.frames['left']['normal']
                ]
                self.speed = 5
                self.health = 3
                self.max_health = 3
                self.damage_amount = 2
                self.xp = 2
                self.current_frame = 1
                self.frame_timer = pygame.time.get_ticks()
                self.hitbox_width = SHROOM_SIZE * 0.9
                self.hitbox_height = SHROOM_SIZE * 0.9
                self.frame_rate = 200
            case EnemyType.FOX:
                self.original_image = pygame.transform.scale(pygame.image.load('data/fox/Fox_Frame_1.png'),
                                                             (FOX_SIZE, FOX_SIZE))
                self.frames['right']['normal'] = [
                    pygame.transform.scale(pygame.image.load('data/fox/Fox_Frame_1.png'), (FOX_SIZE, FOX_SIZE)),
                    pygame.transform.scale(pygame.image.load('data/fox/Fox_Frame_2.png'), (FOX_SIZE, FOX_SIZE)),
                    pygame.transform.scale(pygame.image.load('data/fox/Fox_Frame_3.png'), (FOX_SIZE, FOX_SIZE)),
                ]
                self.frames['right']['red'] = [
                    self._create_red_frame(frame) for frame in self.frames['right']['normal']
                ]
                self.frames['left']['normal'] = [
                    pygame.transform.flip(frame, True, False) for frame in self.frames['right']['normal']
                ]
                self.frames['left']['red'] = [
                    self._create_red_frame(frame) for frame in self.frames['left']['normal']
                ]
                self.speed = 4
                self.health = 5
                self.max_health = 5
                self.damage_amount = 2
                self.xp = 2
                self.walk_frame_1 = self.original_image.copy()
                self.current_frame = 1
                self.frame_timer = pygame.time.get_ticks()
                self.hitbox_width = FOX_SIZE * 0.65
                self.hitbox_height = FOX_SIZE * 0.5
                self.frame_rate = 150
                # if self.is_player_left_or_right(player) == "left":
                #     self.flip_frames()
                #     self.direction = "left"
                # else:
                #     self.direction = "right"
            case EnemyType.CRAB:
                self.original_image = pygame.transform.scale(pygame.image.load('data/crab/Crab_Frame_1.png'),
                                                             (CRAB_SIZE, CRAB_SIZE))
                self.frames['right']['normal'] = [
                    pygame.transform.scale(pygame.image.load('data/crab/Crab_Frame_1.png'), (CRAB_SIZE, CRAB_SIZE)),
                    pygame.transform.scale(pygame.image.load('data/crab/Crab_Frame_2.png'), (CRAB_SIZE, CRAB_SIZE)),
                    pygame.transform.scale(pygame.image.load('data/crab/Crab_Frame_3.png'), (CRAB_SIZE, CRAB_SIZE)),
                ]
                self.frames['right']['red'] = [
                    self._create_red_frame(frame) for frame in self.frames['right']['normal']
                ]
                self.frames['left']['normal'] = [
                    pygame.transform.flip(frame, True, False) for frame in self.frames['right']['normal']
                ]
                self.frames['left']['red'] = [
                    self._create_red_frame(frame) for frame in self.frames['left']['normal']
                ]
                self.speed = 2
                self.health = 40
                self.max_health = 40
                self.damage_amount = 20
                self.xp = 5
                self.current_frame = 1
                self.frame_timer = pygame.time.get_ticks()
                self.hitbox_width = CRAB_SIZE * 0.65
                self.hitbox_height = CRAB_SIZE * 0.5
                self.frame_rate = 200
            case EnemyType.TREE:
                self.frames['right']['normal'] = [
                    pygame.transform.flip(
                        pygame.transform.scale(pygame.image.load('data/tree/Tree_Frame_Walking_1.png'),
                                               (TREE_SIZE, TREE_SIZE)), True, False),
                    pygame.transform.flip(
                        pygame.transform.scale(pygame.image.load('data/tree/Tree_Frame_Walking_2.png'),
                                               (TREE_SIZE, TREE_SIZE)), True, False),
                ]
                self.frames['right']['red'] = [
                    self._create_red_frame(frame) for frame in self.frames['right']['normal']
                ]
                self.frames['left']['normal'] = [
                    pygame.transform.flip(frame, True, False) for frame in self.frames['right']['normal']
                ]
                self.frames['left']['red'] = [
                    self._create_red_frame(frame) for frame in self.frames['left']['normal']
                ]
                self.frames['static'] = [
                    pygame.transform.flip(
                        pygame.transform.scale(pygame.image.load('data/tree/Tree_Frame_1.png'),
                                               (TREE_SIZE, TREE_SIZE)), True, False),
                ]
                self.speed = 0
                self.health = 100
                self.max_health = 100
                self.damage_amount = 0
                self.xp = 20
                self.state = State.SLEEP
                self.countdown = 20
                self.current_frame = 1
                self.frame_timer = pygame.time.get_ticks()
                self.hitbox_width = FOX_SIZE * 0.6
                self.hitbox_height = FOX_SIZE * 0.7
                self.frame_rate = 200
        self.flashing_state = 'normal'
        self.direction = 'left'
        self.image = self.frames['static'][0] if self.type == EnemyType.TREE else \
        self.frames[self.direction][self.flashing_state][0]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.hitbox = pygame.Rect(
            self.rect.centerx - self.hitbox_width // 2,
            self.rect.centery - self.hitbox_height // 2,
            self.hitbox_width,
            self.hitbox_height, )
        self.grid = grid
        self.grid.add(self)
        self.flash_time = 0

    def change_direction(self, player):
        if player.rect.centerx > self.rect.centerx:
            self.direction = Direction.LEFT
        else:
            self.direction = Direction.RIGHT

    def update(self, player, camera):
        self.grid.update(self)

        if self.flash_time >= 0:
            self.flash_time -= 1

        if self.flash_time <= 0:
            self.is_flashing = False

        self.change_direction(player)

        dx, dy = player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx, dy = dx / dist, dy / dist
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

        self.hitbox.center = self.rect.center

        overlapping_enemies = self.grid.get_nearby(self)
        for enemy in overlapping_enemies:
            if enemy != self and self.hitbox.colliderect(enemy.hitbox):
                self.resolve_overlap(enemy)

        distance = self.get_distance(player.rect.center)

        if distance <= 500 and self.state == State.SLEEP and player.xp > 20:
            self.state = State.AWAKE
            camera.shake(50, 15)
            sound.play('./data/sounds/earthquake1.mp3', 2)
            self.image = pygame.transform.flip(
                pygame.transform.scale(pygame.image.load('data/tree/Tree_Frame_wakeup1.png'), (TREE_SIZE, TREE_SIZE)),
                True, False)

        if self.type == EnemyType.TREE:
            if self.state == State.AWAKE:
                self.countdown -= 1

            if self.countdown == 10:
                self.image = pygame.transform.flip(
                    pygame.transform.scale(pygame.image.load('data/tree/Tree_Frame_wakeup2.png'),
                                           (TREE_SIZE + 1, TREE_SIZE + 1)), True, False)

            if self.countdown <= 0 and self.speed <= 0:
                self.speed = 1
                self.damage_amount = 25
                self.image = pygame.transform.flip(
                    pygame.transform.scale(pygame.image.load('data/tree/Tree_Frame_Walking_2.png'),
                                           (TREE_SIZE, TREE_SIZE)),
                    True, False)

        self.animation()

    def get_distance(self, player_pos):
        dx = self.rect.centerx - player_pos[0]
        dy = self.rect.centery - player_pos[1]
        return math.sqrt(dx ** 2 + dy ** 2)

    def animation(self):
        if self.is_flashing:
            self.flashing_state = 'red'
        else:
            self.flashing_state = 'normal'

        current_time = pygame.time.get_ticks()

        if self.type == EnemyType.TREE:
            if self.state == State.AWAKE and self.speed > 0:
                if current_time - self.frame_timer >= self.frame_rate:
                    self.frame_timer = current_time
                    self.current_frame = (self.current_frame % 2)
                    self.image = self.frames[self.direction][self.flashing_state][self.current_frame]


        else:
            if current_time - self.frame_timer >= self.frame_rate:
                self.frame_timer = current_time

                self.current_frame = (self.current_frame % 4) + 1

                if self.current_frame == 1:
                    self.image = self.frames[self.direction][self.flashing_state][0]
                elif self.current_frame == 2:
                    self.image = self.frames[self.direction][self.flashing_state][1]
                elif self.current_frame == 3:
                    self.image = self.frames[self.direction][self.flashing_state][2]
                else:
                    self.image = self.frames[self.direction][self.flashing_state][1]


    def resolve_overlap(self, other):
        dx = self.hitbox.centerx - other.hitbox.centerx
        dy = self.hitbox.centery - other.hitbox.centery
        distance = math.hypot(dx, dy)
        if distance == 0:
            distance = 1
        overlap = (self.hitbox.width / 2 + other.hitbox.width / 2) - distance
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

        self.flash_red()

        self.health -= amount

        if self.health <= 0:
            self.die()
            player.give_xp(self.xp)

    def _create_red_frame(self, frame):
        red_frame = frame.copy()
        red_frame.fill((70, 40, 40), special_flags=pygame.BLEND_ADD)
        return red_frame

    def flash_red(self):
        self.is_flashing = True
        self.flash_time = 7

    def die(self):
        self.grid.remove(self)
        self.hitbox = pygame.Rect(0, 0, 0, 0)
        self.kill()

    def get_pos(self):
        return self.rect.topleft
