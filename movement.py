import pygame

# pygame setup
pygame.init()

# Screen and world setup
screenSize = SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
playerSize = 25

WORLD_WIDTH, WORLD_HEIGHT = 2000, 2000
world_surface = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))
world_surface.fill("green")  # World background

screen = pygame.display.set_mode(screenSize)
clock = pygame.time.Clock()
running = True
dt = 0

# Player and camera setup
player_pos = pygame.Vector2(WORLD_WIDTH / 2, WORLD_HEIGHT / 2)
camera_offset = pygame.Vector2(0, 0)

# Font for rendering text
pygame.display.set_caption('Player Near Borders')
font = pygame.font.Font('freesansbold.ttf', 32)

speed = 300  # Player movement speed

# Create objects in the world
trees = [
    pygame.Rect(400, 300, 50, 100),
    pygame.Rect(1000, 800, 50, 100),
    pygame.Rect(2000, 1500, 50, 100)
]

while running:
    # Poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Text rendering
    text = font.render(f"{round(player_pos.x, 2)}, {round(player_pos.y, 2)}", True, "white")
    textRect = text.get_rect()
    textRect.center = (100, 50)

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= speed * dt
    if keys[pygame.K_s]:
        player_pos.y += speed * dt
    if keys[pygame.K_a]:
        player_pos.x -= speed * dt
    if keys[pygame.K_d]:
        player_pos.x += speed * dt

    # Clamp player position within the world boundaries
    player_pos.x = max(0 + playerSize, min(WORLD_WIDTH - playerSize, player_pos.x))
    player_pos.y = max(0 + playerSize, min(WORLD_HEIGHT - playerSize, player_pos.y))

    camera_offset.x = max(0 + SCREEN_WIDTH // 2, min(WORLD_WIDTH - SCREEN_WIDTH // 2, player_pos.x - SCREEN_WIDTH // 2))
    camera_offset.y = max(0 + SCREEN_HEIGHT // 2, min(WORLD_HEIGHT - SCREEN_HEIGHT // 2, player_pos.y - SCREEN_HEIGHT // 2))

    # Adjust camera offset
    if player_pos.x < SCREEN_WIDTH // 2:
        camera_offset.x = 0
    elif player_pos.x > WORLD_WIDTH - SCREEN_WIDTH // 2:
        camera_offset.x = WORLD_WIDTH - SCREEN_WIDTH
    else:
        camera_offset.x = player_pos.x - SCREEN_WIDTH // 2

    if player_pos.y < SCREEN_HEIGHT // 2:
        camera_offset.y = 0
    elif player_pos.y > WORLD_HEIGHT - SCREEN_HEIGHT // 2:
        camera_offset.y = WORLD_HEIGHT - SCREEN_HEIGHT
    else:
        camera_offset.y = player_pos.y - SCREEN_HEIGHT // 2

    # Clear the screen
    screen.fill("purple")

    # Render the world
    screen.blit(world_surface, (-camera_offset.x, -camera_offset.y))

    # Draw objects in the world (trees)
    for tree in trees:
        pygame.draw.rect(world_surface, "brown", tree)
        pygame.draw.ellipse(world_surface, "darkgreen", tree.inflate(50, 50))

    # Render player
    player_screen_x = player_pos.x - camera_offset.x
    player_screen_y = player_pos.y - camera_offset.y
    pygame.draw.circle(screen, "red", (player_screen_x, player_screen_y), playerSize)

    # Render text
    screen.blit(text, textRect)

    # Update the display
    pygame.display.flip()

    # Cap FPS and calculate delta time
    dt = clock.tick(60) / 1000

pygame.quit()
