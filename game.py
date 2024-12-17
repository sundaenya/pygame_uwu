import pygame
import sys
from tiles import *
from spritesheet import *
from player import Player
from enemy import Enemy
from bullet import Bullet
from camera import Camera
from enums import GameSettings
from collision import check_collision, check_bullet_collisions

# Initialize Pygame
pygame.init()

# Set up the game window

screen_width = GameSettings.SCREEN_WIDTH 
screen_height = GameSettings.SCREEN_HEIGHT 
world_width = GameSettings.WORLD_WIDTH 
world_height = GameSettings.WORLD_HEIGHT
screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
pygame.display.set_caption('Amelia Earheart Simulator')


# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

camera = Camera()

# Set up font
font = pygame.font.SysFont(None, 55)


canvas = pygame.Surface((world_width, world_height))
spritesheet = Spritesheet('grassTileset.png')
map1 = TileMap('data\grass.csv', spritesheet)



world_surface = pygame.Surface((world_width, world_height))
world_surface.fill("green")

# Function to display 'You Lose' text
def show_message(screen, message, color, x, y):
    text = font.render(message, True, color)
    screen.blit(text, (x, y))

# Main game loop
# Main game loop
def main():
    clock = pygame.time.Clock()

    # Create a player instance
    player = Player(screen_width // 2, screen_height // 2)
    
    # Create an enemy instance
    enemy = Enemy((screen_width // 4, screen_height // 4))
    

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player, enemy)

    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group(enemy)

    game_over = False

    FIRE  = pygame.USEREVENT + 1
    pygame.time.set_timer(FIRE, 250)

    # Game loop
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == FIRE:
                try:
                    target_x,target_y = player.get_closest_enemy(enemies).get_pos()
                except:
                    target_x, target_y = player.rect.centerx, player.rect.centery - 1

                bullet = Bullet(player.rect.centerx, player.rect.centery, target_x, target_y)
                all_sprites.add(bullet)
                bullets.add(bullet)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                enemy = Enemy(tuple(map(sum, zip(pygame.mouse.get_pos(), camera.get_offset()))))
                enemies.add(enemy)
                all_sprites.add(enemy)
            
        if not game_over:
            # Update game state
            keys = pygame.key.get_pressed()
            player.update(keys)

            for e in enemies:
                e.update(player)
                if check_collision(player, e):
                    game_over = True
            bullets.update()

            # Check for bullet-enemy collisions
            check_bullet_collisions(enemies, bullets)

        screen.blit(world_surface, (-camera.camera_offset.x, -camera.camera_offset.y))

        map1.draw_map(canvas)
        camera.move(player.rect)
        canvas.fill((0, 180, 240)) # Fills the entire screen with light blue
        map1.draw_map(canvas)
        screen.blit(canvas, (-camera.camera_offset.x, -camera.camera_offset.y))

        # Render all game objects relative to the camera offset
        for sprite in all_sprites:
            offset_pos = sprite.rect.topleft - camera.camera_offset
            screen.blit(sprite.image, offset_pos)

            pygame.draw.rect(screen, "red",pygame.Rect(offset_pos.x, offset_pos.y, sprite.rect.width, sprite.rect.height),width=2)


        # Display 'You Lose' message if game is over
        if game_over:
            show_message(screen, 'You Lose', WHITE, screen_width // 2 - 100, screen_height // 2 - 50)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(120)

# Run the game
if __name__ == "__main__":
    main()
