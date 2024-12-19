import pygame

def check_collision(player, enemy):
    # Check collision between player and enemy's hitbox
    if player.rect.colliderect(enemy.hitbox):
        return True
    return False

def check_bullet_collisions(bullets, enemies, player):
    # Use groupcollide for bullets and enemies
    collisions = pygame.sprite.groupcollide(bullets, enemies, True, False)

    for bullet, hit_enemies in collisions.items():
        for enemy in hit_enemies:
            # Check collision using the enemy's hitbox
            if bullet.rect.colliderect(enemy.hitbox):
                enemy.damage(bullet.damage, player)

def check_pbullet_collisions(pbullets, enemies, player):
    # Use groupcollide for pbullets and enemies (no removal of bullets)
    collisions = pygame.sprite.groupcollide(pbullets, enemies, False, False)

    for bullet, hit_enemies in collisions.items():
        for enemy in hit_enemies:
            # Check collision using the enemy's hitbox
            if bullet.rect.colliderect(enemy.hitbox):
                enemy.damage(bullet.damage, player)


