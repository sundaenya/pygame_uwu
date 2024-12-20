import pygame
from enums import GameSettings

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.size = GameSettings.PLAYER_SIZE
        self.image = pygame.transform.scale(pygame.image.load('data/player/Kitty_Idle_Frame_1.png'), (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 7
        self.xp = 0
        self.health = 1000
        self.direction = 'idle'
        self.frames = {
            'left': [],
            'right': [],
            'idle': []
        }
        self.current_frame = 0
        self.animation_timer = pygame.time.get_ticks()
        self.animation_delay = 150
        self.load_images()

    def load_images(self):
        idle_frames = [
            'Kitty_Idle_Frame_1.png',
            'Kitty_Idle_Frame_2.png',
            'Kitty_Idle_Frame_3.png'
        ]
        walking_frames = [
            'Kitty_Idle_Frame_1.png',
            'Kitty_Walking_Frame_2.png',
            'Kitty_Walking_Frame_3.png'
        ]

        self.frames['idle'] = [
            pygame.transform.scale(pygame.image.load(f'data/player/{frame}'), (self.size, self.size)) for frame in idle_frames
        ]
        self.frames['left'] = [
            pygame.transform.scale(pygame.image.load(f'data/player/{frame}'), (self.size, self.size)) for frame in walking_frames
        ]
        self.frames['right'] = [
            pygame.transform.flip(frame, True, False) for frame in self.frames['left']
        ]

    def update(self, keys):
        world_width = GameSettings.WORLD_WIDTH
        world_height = GameSettings.WORLD_HEIGHT

        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.direction = 'left'
        elif keys[pygame.K_d]:
            self.rect.x += self.speed
            self.direction = 'right'
        else:
            self.direction = 'idle'

        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed

        self.rect.x = max(0, min(world_width - self.size, self.rect.x))
        self.rect.y = max(0, min(world_height - self.size, self.rect.y))

        self.animate()

    def animate(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.animation_timer >= self.animation_delay:
            self.animation_timer = current_time
            self.current_frame = (self.current_frame + 1) % len(self.frames[self.direction])
            self.image = self.frames[self.direction][self.current_frame]

        if self.direction != 'idle':
            if self.current_frame == 1:
                self.rect.y -= 2
            elif self.current_frame == 2:
                self.rect.y += 2


    def damage(self, amount):
        self.health -= amount

    def give_xp(self, amount):
        self.xp += amount

    def get_closest_enemy(self, enemies):
        pos = pygame.math.Vector2(self.rect.center)
        moving_enemies = [e for e in enemies if e.speed > 0]
        if not moving_enemies:
            return None
        return min(moving_enemies, key=lambda e: pos.distance_to(e.rect.center))
