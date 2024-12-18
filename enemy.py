import pygame
import math
import sound

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, etype, grid):
        super().__init__()
        self.type = etype
        self.state = 'moving'
        match self.type:
            case 'basic':
                self.original_image = pygame.transform.scale(pygame.image.load('./data/Crab_Frame_1.png'), (100, 100))
                self.speed = 3
                self.health = 5
                self.max_health = 5
                self.damage_amount = 2
                self.xp = 2
            case 'heavy':
                self.original_image = pygame.transform.scale(pygame.image.load('./data/Crab_Frame_1.png'), (200, 200))
                self.speed = 2
                self.health = 40
                self.max_health = 40
                self.damage_amount = 20
                self.xp = 5
            case 'tree':
                self.original_image = pygame.transform.scale(pygame.image.load('./data/Tree_Frame_1.png'), (200, 200))
                self.speed = 0
                self.health = 200
                self.max_health = 200
                self.damage_amount = 50
                self.xp = 20
                self.state = 'sleep'
                self.countdown = 50
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.grid = grid
        self.grid.add(self)
        self.flash_time = 0
        self.direction = 'right'

    def change_direction(self):
        self.original_image = pygame.transform.flip(self.original_image, True, False)
        self.image = pygame.transform.flip(self.image, True, False)

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

        # Movement towards the player
        dx, dy = player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx, dy = dx / dist, dy / dist
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

        # Check and resolve overlaps
        overlapping_enemies = self.grid.get_nearby(self)
        for enemy in overlapping_enemies:
            if enemy != self and self.rect.colliderect(enemy.rect):
                self.resolve_overlap(enemy)

        distance = self.get_distance(player.rect.center)

        if distance <= 500 and self.state == 'sleep':
            self.state = 'awake'
            camera.shake(50, 15)
            sound.play('./data/sounds/earthquake1.mp3', 2)

        if self.type == 'tree' and self.state == 'awake':
            self.countdown -= 1

        if self.type == 'tree' and self.countdown <= 0:
            self.speed = 1

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

        self.flash_red()

        if self.health <= 0:
            self.die()
            player.give_xp(self.xp)

    def flash_red(self):
        self.image.fill((255, 0, 0), special_flags=pygame.BLEND_ADD)
        self.flash_time = pygame.time.get_ticks()

    def die(self):
        self.grid.remove(self)
        self.kill()

    def get_pos(self):
        return self.rect.topleft
