import pygame
import sys
import os
from player import Player
from enemy import Enemy
from bullet import Bullet
from collision import check_collision, check_bullet_collisions

# Initialize Pygame
pygame.init()

# Set up the game window
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
pygame.display.set_caption('Amelia Earheart Simulator')

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up font
font = pygame.font.SysFont(None, 55)

# Function to display 'You Lose' text
def show_message(screen, message, color, x, y):
    text = font.render(message, True, color)
    screen.blit(text, (x, y))

# Main game loop
def main():
    clock = pygame.time.Clock()
    
    # Create a player instance
    player = Player(screen_width // 2, screen_height // 2)
    
    # Create an enemy instance
    enemy = Enemy((screen_width // 4, screen_height // 4))
    
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(enemy)
    
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    enemies.add(enemy)
    
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
                    target_x, target_y = player.get_closest_enemy(enemies).get_pos()
                except:
                    target_x, target_y = player.rect.centerx, player.rect.centery - 1
                bullet = Bullet(player.rect.centerx, player.rect.centery, target_x, target_y)
                all_sprites.add(bullet)
                bullets.add(bullet)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                enemy = (Enemy(pygame.mouse.get_pos()))
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

        # Clear the screen
        screen.fill(BLACK)

        # Render the game
        all_sprites.draw(screen)

        # Display 'You Lose' message if game is over
        if game_over:
            show_message(screen, 'You Lose', WHITE, screen_width // 2 - 100, screen_height // 2 - 50)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

# Run the game
if __name__ == "__main__":
    main()
