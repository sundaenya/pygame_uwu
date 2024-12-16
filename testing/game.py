import pygame
import sys
from player import Player
from enemy import Enemy

# Initialize Pygame
pygame.init()

# Set up the game window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Roguelike Game')

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
    enemy = Enemy(screen_width // 4, screen_height // 4)
    enemy1 = Enemy(screen_width // 4, screen_height // 4)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(enemy)
    all_sprites.add(enemy1)
    
    game_over = False

    # Game loop
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not game_over:
            # Update game state
            keys = pygame.key.get_pressed()
            player.update(keys)
            enemy.update(player)
            enemy1.update(player)

            # Check for collisions
            if pygame.sprite.collide_rect(player, enemy):
                game_over = True

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
