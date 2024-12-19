import pygame
import math
import sound

TREE_SIZE = 350
BASIC_SIZE = 100
HEAVY_SIZE = 200


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, etype, grid):
        super().__init__()
        self.type = etype
        self.state = 'moving'
        match self.type:
            case 'basic':
                self.original_image = pygame.transform.scale(pygame.image.load('data/fox/Fox_Frame_1.png'), (BASIC_SIZE, BASIC_SIZE))
                self.speed = 4
                self.health = 5
                self.max_health = 5
                self.damage_amount = 2
                self.xp = 2
                self.walk_frame_1 = self.original_image.copy()
                self.walk_frame_2 = pygame.transform.scale(pygame.image.load('data/fox/Fox_Frame_2.png'), (BASIC_SIZE, BASIC_SIZE))
                self.walk_frame_3 = pygame.transform.scale(pygame.image.load('data/fox/Fox_Frame_3.png'), (BASIC_SIZE, BASIC_SIZE))
                self.current_frame = 1
                self.frame_timer = pygame.time.get_ticks()
            case 'heavy':
                self.original_image = pygame.transform.scale(pygame.image.load('data/crab/Crab_Frame_1.png'), (HEAVY_SIZE, HEAVY_SIZE))
                self.speed = 2
                self.health = 40
                self.max_health = 40
                self.damage_amount = 20
                self.xp = 5
                self.walk_frame_1 = self.original_image.copy()
                self.walk_frame_2 = pygame.transform.scale(pygame.image.load('data/crab/Crab_Frame_2.png'), (HEAVY_SIZE, HEAVY_SIZE))
                self.walk_frame_3 = pygame.transform.scale(pygame.image.load('data/crab/Crab_Frame_3.png'), (HEAVY_SIZE, HEAVY_SIZE))
                self.current_frame = 1
                self.frame_timer = pygame.time.get_ticks()
            case 'tree':
                self.original_image = pygame.transform.flip(pygame.transform.scale(pygame.image.load('data/tree/Tree_Frame_1.png'), (TREE_SIZE, TREE_SIZE)), True, False)
                self.walk_frame_1 = pygame.transform.flip(pygame.transform.scale(pygame.image.load('data/tree/Tree_Frame_Walking_1.png'), (TREE_SIZE, TREE_SIZE)), True, False)
                self.walk_frame_2 = pygame.transform.flip(pygame.transform.scale(pygame.image.load('data/tree/Tree_Frame_Walking_2.png'), (TREE_SIZE, TREE_SIZE)), True, False)
                self.speed = 0
                self.health = 200
                self.max_health = 200
                self.damage_amount = 0
                self.xp = 20
                self.state = 'sleep'
                self.countdown = 20
                self.current_frame = 1
                self.frame_timer = pygame.time.get_ticks()
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.grid = grid
        self.grid.add(self)
        self.flash_time = 0
        self.direction = 'right'
        self.is_flashing = False

    def change_direction(self):
        self.original_image = pygame.transform.flip(self.original_image, True, False)
        self.image = pygame.transform.flip(self.image, True, False)
        if self.type == 'tree':
            self.walk_frame_1 = pygame.transform.flip(self.walk_frame_1, True, False)
            self.walk_frame_2 = pygame.transform.flip(self.walk_frame_2, True, False)

        if self.type == 'heavy' or  self.type == 'basic':
            self.walk_frame_1 = pygame.transform.flip(self.walk_frame_1, True, False)
            self.walk_frame_2 = pygame.transform.flip(self.walk_frame_2, True, False)
            self.walk_frame_3 = pygame.transform.flip(self.walk_frame_3, True, False)

    def is_player_left_or_right(player, enemy):
        if player.rect.centerx < enemy.rect.centerx:
            return "left"
        else:
            return "right"

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

        if distance <= 500 and self.state == 'sleep' and player.xp > 20:
            self.state = 'awake'
            camera.shake(50, 15)
            sound.play('./data/sounds/earthquake1.mp3', 2)
            self.image = pygame.transform.flip(pygame.transform.scale(pygame.image.load('data/tree/Tree_Frame_wakeup1.png'), (TREE_SIZE, TREE_SIZE)), True, False)

        if self.type == 'tree' and self.state == 'awake':
            self.countdown -= 1

        if self.type == 'tree' and self.countdown == 10:
            self.image = pygame.transform.flip(pygame.transform.scale(pygame.image.load('data/tree/Tree_Frame_wakeup2.png'), (TREE_SIZE + 1, TREE_SIZE + 1)),True, False)

        if self.type == 'tree' and self.countdown <= 0 and self.speed <= 0:
            self.speed = 1
            self.damage_amount = 25
            self.original_image = pygame.transform.flip(pygame.transform.scale(pygame.image.load('data/tree/Tree_Frame_Walking_2.png'),(TREE_SIZE, TREE_SIZE)), True, False)
            self.image = pygame.transform.flip(pygame.transform.scale(pygame.image.load('data/tree/Tree_Frame_Walking_2.png'), (TREE_SIZE, TREE_SIZE)), True, False)

        if self.type == 'tree' and self.state == 'awake' and self.speed > 0:
            current_time = pygame.time.get_ticks()
            if current_time - self.frame_timer >= 300:
                self.frame_timer = current_time
                self.current_frame = 2 if self.current_frame == 1 else 1
                self.image = self.walk_frame_1 if self.current_frame == 1 else self.walk_frame_2

        if self.type == 'basic':
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

        if self.type == 'heavy':
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

        if self.is_flashing:
            red_overlay = self.image.copy()
            red_overlay.fill((255, 0, 0), special_flags=pygame.BLEND_ADD)
            self.image = red_overlay

    def get_distance(self, player_pos):
        dx = self.rect.centerx - player_pos[0]
        dy = self.rect.centery - player_pos[1]
        return math.sqrt(dx ** 2 + dy ** 2)

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
