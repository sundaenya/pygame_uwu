import pygame

def check_collision(player, enemy):
    if pygame.sprite.collide_rect(player, enemy):

        return True
    return False

def check_bullet_collisions(bullets, enemies, player):
    collisions = pygame.sprite.groupcollide(bullets, enemies, True, False)

    for bullet, hit_enemies in collisions.items():
        for enemy in hit_enemies:
            enemy.damage(bullet.damage, player)

def check_pbullet_collisions(pbullets, enemies, player):
    list = pygame.sprite.groupcollide(pbullets, enemies, False, False)

    for bullet, hit_enemies in list.items():
        for enemy in hit_enemies:
            enemy.damage(bullet.damage, player)

