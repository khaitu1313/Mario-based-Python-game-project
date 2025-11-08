import pygame
import time
import os
from os.path import join

class Proj:
    def __init__(self, x, y, ally, special, direction, dmg = 10):
        self.rect = pygame.Rect(x,y,20,4)
        self.destroyed = False
        self.ally = ally
        self.special = special
        if direction == "left":
            self.direction_left = True
        elif direction == "right":
            self.direction_left = False
        
        
        
        self.speed = 10

        self.dmg = dmg
        
        # --- Assign color once ---
        if self.ally and not self.special:
            self.color = (0, 128, 255)      # Blue - ally normal
        elif self.ally and self.special:
            self.color = (0, 255, 100)      # Green - ally special
        elif not self.ally and not self.special:
            self.color = (255, 50, 50)      # Red - enemy normal
        else:
            self.color = (180, 0, 255)      # Purple - enemy special

    def update(self, objs, player, nor, spe, boss, sound):
        """Move projectile based on direction."""
        if self.direction_left:
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
        #Collision to wall
        for terrain in objs:
            if self.rect.colliderect(terrain.rect):
                self.destroyed = True
                
                if self.special:
                    print("removed spe(Wall)")
                else:
                    print("remove Nor(Wall)")
                return
            
        #Collision to Player/Enemy
        if not self.ally:
            if self.rect.colliderect(player.rect) and not player.Invin:
                player.Invin = True
                player.InvinTime = time.time()
                self.destroyed = True
                shoot_sound = pygame.mixer.Sound(join("assets", "sfx", "hit.mp3"))
                shoot_sound.set_volume(sound/100)  # adjust between 0.0–1.0
                shoot_sound.play()
                player.HP -= self.dmg
                if player.HP<0:
                    player.HP = 0
        else:
            if boss:
                if self.rect.colliderect(boss.rect):
                    self.destroyed = True
                    shoot_sound = pygame.mixer.Sound(join("assets", "sfx", "hit.mp3"))
                    shoot_sound.set_volume(sound/100)  # adjust between 0.0–1.0
                    shoot_sound.play()
                    if ((not self.special) and (not boss.special) ) or (self.special and boss.special):
                        boss.hp -=self.dmg
                        if boss.hp <0:
                            boss.hp =0
                    elif self.special and (not boss.special):
                        boss.hp -=self.dmg/2
                        if boss.hp <0:
                            boss.hp =0
                
                
                
                
                
            if self.special:
                # Special bullet: full dmg to special, half dmg to normal
                for enemy in spe:
                    if self.rect.colliderect(enemy.rect) and not self.destroyed:
                        enemy.HP -= self.dmg
                        if enemy.HP < 0:
                            enemy.HP = 0
                        self.destroyed = True
                        shoot_sound = pygame.mixer.Sound(join("assets", "sfx", "hit.mp3"))
                        shoot_sound.set_volume(sound/100)  # adjust between 0.0–1.0
                        shoot_sound.play()

                for enemy in nor:
                    if self.rect.colliderect(enemy.rect) and not self.destroyed:
                        # hit but half damage
                        enemy.HP -= self.dmg / 2
                        if enemy.HP < 0:
                            enemy.HP = 0
                        self.destroyed = True
                        shoot_sound = pygame.mixer.Sound(join("assets", "sfx", "hit.mp3"))
                        shoot_sound.set_volume(sound/100)  # adjust between 0.0–1.0
                        shoot_sound.play()

            else:
                # Normal bullet: full dmg to normal, 0 dmg to special (but still collides)
                for enemy in nor:
                    if self.rect.colliderect(enemy.rect) and not self.destroyed:
                        enemy.HP -= self.dmg
                        if enemy.HP < 0:
                            enemy.HP = 0
                        self.destroyed = True
                        shoot_sound = pygame.mixer.Sound(join("assets", "sfx", "hit.mp3"))
                        shoot_sound.set_volume(sound/100)  # adjust between 0.0–1.0
                        shoot_sound.play()

                for enemy in spe:
                    if self.rect.colliderect(enemy.rect) and not self.destroyed:
                        # Collides but deals no damage
                        self.destroyed = True
                        shoot_sound = pygame.mixer.Sound(join("assets", "sfx", "hit.mp3"))
                        shoot_sound.set_volume(sound/100)  # adjust between 0.0–1.0
                        shoot_sound.play()
                

    def draw(self, surface, offsetX, offsetY):
        """Draw projectile as a thin rectangle."""
        rect = pygame.Rect(
            int(self.rect.x - offsetX),
            int(self.rect.y - offsetY),
            self.rect.width,
            self.rect.height
        )
        pygame.draw.rect(surface, self.color, rect)
