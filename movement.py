# Example file showing a circle moving on screen
import pygame
import math

# pygame setup
pygame.init()

screenSize = width, height = 1280, 720
playerSize = 25
i = 0

screen = pygame.display.set_mode(screenSize)
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
 
# set the pygame window name
pygame.display.set_caption('Show Text')
 
# create a font object.
# 1st parameter is the font file
# which is present in pygame.
# 2nd parameter is size of the font
font = pygame.font.Font('freesansbold.ttf', 32)
 
#text = font.render(str(player_pos.x) + " " + str(player_pos.y), True, "white", "black")
 
# create a rectangular object for the
# text surface object
#textRect = text.get_rect()


# set the center of the rectangular object.

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    text = font.render(str(round(player_pos.x, 2)) + " " + str(round(player_pos.y, 2)), True, "white")
    textRect = text.get_rect()
    textRect.center = (100, 50)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    screen.blit(text, textRect)

    pygame.draw.circle(screen, "red", player_pos, playerSize)

    if player_pos.x <= (0 + (playerSize / 2)) or player_pos.x >= screenSize[0]:
        i = i + 1
        print("out of bound, count " + str(i))
        speed = 0
        player_pos.x = (player_pos.x*50 + screen.get_width() / 2) / 51

    if player_pos.y <= (0 + (playerSize / 2)) or player_pos.y >= screenSize[1]:
        i = i + 1
        print("out of bound, count " + str(i))
        speed = 0
        player_pos.y = (player_pos.y*50 + screen.get_width() / 2) / 51

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= speed * dt
    if keys[pygame.K_s]:
        player_pos.y += speed * dt
    if keys[pygame.K_a]:
        player_pos.x -= speed * dt
    if keys[pygame.K_d]:
        player_pos.x += speed * dt

    speed = 300
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()