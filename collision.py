import pygame

import render

def check_collision(player, enemy):
    if pygame.sprite.collide_rect(player, enemy):

        return True
    return False

def check_bullet_collisions(bullets, enemies):
    list = pygame.sprite.groupcollide(bullets, enemies, True, True)

def check_pbullet_collisions(pbullets, enemies):
    list = pygame.sprite.groupcollide(pbullets, enemies, False, True)
