import pygame

def check_collision(player, enemy):
    if pygame.sprite.collide_rect(player, enemy):
        print("Collision detected!")
        return True
    return False

def check_bullet_collisions(bullets, enemies):
    collisions = pygame.sprite.groupcollide(bullets, enemies, True, True)
    if collisions:
        print("Bullet hit an enemy!")
    return collisions
