import pygame
import sys
import os
import time
import math
from entity.obj import Object
from entity.proj import Proj

from os.path import join

class Enemy(Object):
    def __init__(self, x, y, width, height,special = False, HP = 100, name = "Melee"):
        super().__init__(x, y, width, height, name)
        self.maxHP = HP
        self.HP = HP
        self.special = special
        self.dir_left = True
        self.contactDmg = 10
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
    def update(self, nor, spe, setting, player, sound):
        if not self.special and setting:
            return
        if abs(self.rect.x - self.baseX) >=150:
            self.dir_left = not self.dir_left
        if self.dir_left:
            self.rect.x -= self.speed
        else:
            self.rect.x +=self.speed
        if self.rect.colliderect(player.rect) and not player.Invin:
            player.Invin = True
            player.InvinTime = time.time()
            player.HP-=self.contactDmg
            
class RangeEnemy(Enemy):
    RangeShootCD = 1.0 #one sec
    def __init__(self, x, y, width, height, special = False, dir_Left = True):
        super().__init__(x, y, width, height,special, 50,  "Range") 
        self.last_shot_time = time.time()  # thời điểm lần bắn cuối
        self.shootCD = RangeEnemy.RangeShootCD
        self.dir_left = dir_Left
    def update(self, nor, spe, setting, player, sound):
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
            if abs(self.rect.x-player.rect.x) <=640:
                shoot_sound = pygame.mixer.Sound(join("assets", "sfx", "shoot.mp3"))
                shoot_sound.set_volume(sound/400)  # adjust between 0.0–1.0
                shoot_sound.play()
            self.last_shot_time = current_time
        
        
# ==================== BOSS ====================
class BossBullet:
    def __init__(self, x, y, vx, vy, size):
        half = size // 2
        self.rect = pygame.Rect(x - half, y - half, size, size)
        self.vx, self.vy = vx, vy
        self.dmg = 10
        self.destroyed = False
    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

    def draw(self, surf, ox, oy):
        pygame.draw.circle(surf, (255, 100, 100),
                           (int(self.rect.centerx - ox), int(self.rect.centery - oy)),
                           self.rect.width // 2)


class Boss:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.hp = self.max_hp = 500
        self.phase = 1
        
        self.special = False

        # patrol on the right edge
        self.patrol_x = 1160
        self.center_y = 360
        self.amp = 260
        self.freq = 0.1
        self.freq2 = 0.15

        # shooting
        self.last_shot = 0
        self.shot_interval = 3000          # ms
        self.burst = 3
        self.b_speed = 5.0                # 1.5× normal
        self.b_size = 40                   # 2.5× normal
        self.shots_since_slam = 0

        # slam
        self.state = "patrol"
        self.state_t = 0
        self.last_t = 0
        self.appear_delay = 200
        self.track_time = 1000
        self.stay1 = 2000
        self.stay2 = 5000
        self.repeat = 0
        self.track_spd = 400.0
        self.fall_spd = 30.0
        self.ground_y = 704 
        self.slam_DMG = 15

    # ------------------------------------------------------------------
    def update(self, now, player, boss_projs, terrain, sound):
        dt = now - self.last_t
        self.last_t = now

        # phase change
        if self.hp <= self.max_hp // 2 and self.phase == 1:
            self.phase = 2
            self.freq = self.freq2
            self.shot_interval = 2000

        sec = dt / 1000.0
        frame = dt / (1000 / 60)
        if self.rect.colliderect(player.rect) and not player.Invin:
            player.Invin = True
            player.InvinTime = time.time()
            player.HP -= self.slam_DMG
            if player.HP<0:
                player.HP =0
        # ---------- PATROL ----------
        if self.state == "patrol":
            t = now * 0.001
            self.rect.centery = max(50, min(670,
                                   self.center_y + self.amp * math.sin(2 * math.pi * self.freq * t)))
            self.rect.centerx = self.patrol_x

            if now - self.last_shot >= self.shot_interval:
                self._burst(player, boss_projs, sound)
                self.last_shot = now
                self.shots_since_slam += 1
                if self.phase == 2 and self.shots_since_slam >= 2:
                    self._start_slam()
                    self.shots_since_slam = 0

        # ---------- SLAM APPEAR ----------
        elif self.state == "slam_appear":
            self.rect.y = -self.rect.height
            self.rect.centerx = max(120, min(1160, player.rect.centerx))
            self.state_t -= dt
            if self.state_t <= 0:
                self.state = "slam_track"
                self.state_t = self.track_time

        # ---------- SLAM TRACK ----------
        elif self.state == "slam_track":
            target = player.rect.centerx
            dx = target - self.rect.centerx
            move = self.track_spd * sec
            if abs(dx) > move:
                self.rect.centerx += math.copysign(move, dx)
            else:
                self.rect.centerx = target
            self.rect.centerx = max(120, min(1160, self.rect.centerx))
            self.rect.y = -self.rect.height
            self.state_t -= dt
            if self.state_t <= 0:
                self.state = "slam_fall"

        # ---------- SLAM FALL ----------
        elif self.state == "slam_fall":
            self.rect.y += self.fall_spd * frame
            if self.rect.bottom >= self.ground_y:
                self.rect.bottom = self.ground_y
                stay = self.stay1 if self.repeat == 1 else self.stay2
                self.state = "slam_stay"
                slam_sound = pygame.mixer.Sound(join("assets", "sfx", "impact.mp3"))
                slam_sound.set_volume(sound / 100)
                slam_sound.play()
                self.state_t = stay
                self.repeat += 1
            

        # ---------- SLAM STAY ----------
        elif self.state == "slam_stay":
            self.state_t -= dt
            if self.state_t <= 0:
                if self.repeat == 2:
                    self.state = "patrol"
                    self.repeat = 0
                else:
                    self._start_slam()
        

    # ------------------------------------------------------------------
    def _start_slam(self):
        self.state = "slam_appear"
        self.state_t = self.appear_delay
        self.repeat = 1

    def _burst(self, player, projs, sound):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy) or 1
        base = math.atan2(dy, dx)
        for i in range(self.burst):
            ang = base + (i - 1) * 0.15
            vx = math.cos(ang) * self.b_speed   
            vy = math.sin(ang) * self.b_speed
            shoot_sound = pygame.mixer.Sound(join("assets", "sfx", "fireball.mp3"))
            shoot_sound.set_volume(sound/100)  # adjust between 0.0–1.0
            shoot_sound.play()
            projs.append(BossBullet(self.rect.centerx, self.rect.centery, vx, vy, self.b_size))

    # ------------------------------------------------------------------
    def draw_star(self, surf, color, rect):
        x, y, w, h = rect
        cx, cy = x + w / 2, y + h / 2
        outer = min(w, h) / 2 * 0.8
        inner = outer * 0.4
        pts = []
        for i in range(10):
            r = outer if i % 2 == 0 else inner
            a = i / 10 * 2 * math.pi
            pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
        pygame.draw.polygon(surf, color, pts)

    def draw(self, surf, ox, oy, setting):
        draw_x = self.rect.x - ox
        draw_y = self.rect.y - oy
        col = (255, 215, 0) if self.phase == 1 else (255, 0, 0)
        self.draw_star(surf, col, (draw_x, draw_y, self.rect.width, self.rect.height))

        # HP bar
        bw = self.rect.width
        bh = 10
        fill = (self.hp / self.max_hp) * bw
        pygame.draw.rect(surf, (255, 0, 0), (draw_x, draw_y - 20, bw, bh))
        pygame.draw.rect(surf, (0, 255, 0), (draw_x, draw_y - 20, fill, bh))
        pygame.draw.rect(surf, (255, 255, 255), (draw_x, draw_y - 20, bw, bh), 2)
        