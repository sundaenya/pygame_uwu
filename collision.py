import pygame

def check_collision(player, enemy):
    if player.rect.colliderect(enemy.hitbox):
        return True
    return False

def check_bullet_collisions(bullets, enemies, player):
    collisions = []
    
    for bullet in bullets:
        for enemy in enemies:
            if bullet.rect.colliderect(enemy.hitbox):
                collisions.append((bullet, enemy))
                enemy.damage(bullet.damage, player)

    for bullet, _ in collisions:
        bullet.kill()

def check_pbullet_collisions(pbullets, enemies, player):
    collisions = []

    for bullet in pbullets:
        for enemy in enemies:
            if bullet.rect.colliderect(enemy.hitbox):
                collisions.append((bullet, enemy))
                enemy.damage(bullet.damage, player)
