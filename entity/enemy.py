import pygame
import sys
import os
import time
from entity.obj import Object
from entity.proj import Proj

class Enemy(Object):
    def __init__(self, x, y, width, height,special = False, HP = 100, name = "Melee"):
        super().__init__(x, y, width, height, name)
        self.maxHP = HP
        self.HP = HP
        self.special = special
        self.dir_left = True
        
        self.baseX = x
        self.baseY = y
        
    def draw(self, screen, offset_x, offset_y, setting):
        # Calculate position with camera offset
        draw_x = self.rect.x - offset_x
        draw_y = self.rect.y - offset_y
        color = (255, 255, 0) if not self.special else (160, 32, 240)
        highlight_color = (255, 255, 255)
        if self.name == "Melee":
            # Draw a red rectangle for melee enemy
            pygame.draw.rect(screen, color, (draw_x, draw_y, self.width, self.height))
            if self.special and setting:
                pygame.draw.rect(screen, highlight_color, (draw_x, draw_y, self.width, self.height), 3)
        elif self.name == "Range":
            # Draw a yellow triangle for ranged enemy
            w, h = self.width, self.height

            if self.dir_left:
                # Triangle pointing left
                points = [
                    (draw_x, draw_y + h // 2),          # left tip
                    (draw_x + w, draw_y),               # top-right
                    (draw_x + w, draw_y + h)            # bottom-right
                ]
            else:
                # Triangle pointing right
                points = [
                    (draw_x + w, draw_y + h // 2),      # right tip
                    (draw_x, draw_y),                   # top-left
                    (draw_x, draw_y + h)                # bottom-left
                ]

            pygame.draw.polygon(screen, color, points)
            if self.special and setting:
                pygame.draw.polygon(screen, highlight_color, points, 3)

        else:
            # Default gray rectangle for other enemy types
            pygame.draw.rect(screen, (128, 128, 128), (draw_x, draw_y, self.width, self.height))
            if self.special and setting:
                pygame.draw.rect(screen, highlight_color, (draw_x, draw_y, self.width, self.height), 3)
        hp_ratio = max(self.HP / self.maxHP, 0)
        bar_width = self.width
        bar_height = 6
        bar_x = draw_x
        bar_y = draw_y - 12
        # Background bar (gray)
        pygame.draw.rect(screen, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height))
        # HP portion (green to red)
        pygame.draw.rect(screen, (255 * (1 - hp_ratio), 255 * hp_ratio, 0), (bar_x, bar_y, bar_width * hp_ratio, bar_height))
        # If special, draw a glowing barrier around it
        if self.special and setting == False:
            # Calculate center and radius for barrier
            center_x = draw_x + self.width // 2
            center_y = draw_y + self.height // 2
            radius = max(self.width, self.height) // 2 + 20  # slightly larger than enemy size
            barrier_color = (200, 0, 255)  # bright magenta
            pygame.draw.circle(screen, barrier_color, (center_x, center_y), radius, 3)
            

class MeleeEnemy(Enemy):
    def __init__(self, x, y, width, height, special = False):
        super().__init__(x, y, width, height,special, 100,  "Melee") 
        self.speed = 2
    def update(self, nor, spe, setting):
        if not self.special and setting:
            return
        if abs(self.rect.x - self.baseX) >=150:
            self.dir_left = not self.dir_left
        if self.dir_left:
            self.rect.x -= self.speed
        else:
            self.rect.x +=self.speed
            
class RangeEnemy(Enemy):
    RangeShootCD = 1.0 #one sec
    def __init__(self, x, y, width, height, special = False, dir_Left = True):
        super().__init__(x, y, width, height,special, 50,  "Range") 
        self.last_shot_time = time.time()  # thời điểm lần bắn cuối
        self.shootCD = RangeEnemy.RangeShootCD
        self.dir_left = dir_Left
    def update(self, nor, spe, setting):
        """Không di chuyển, chỉ bắn mỗi 1 giây."""
        current_time = time.time()
        proj_x = self.rect.centerx
        proj_y = self.rect.centery
        proj_dir = ("left" if self.dir_left else "right")
        if current_time - self.last_shot_time >= self.shootCD:
            if not self.special:
                if not setting:
                    nor.append(Proj(proj_x, proj_y, False, False, proj_dir))
            else:
                spe.append(Proj(proj_x, proj_y, False, True, proj_dir))
            self.last_shot_time = current_time
        
        
            
        