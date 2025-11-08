import pygame
import sys
import os
from os import listdir
from os.path import isfile, join

from entity.obj import Object
from entity.player import Player


def load_sprite_sheets(path, width, height):
    sprite_sheet = pygame.image.load(path).convert_alpha()
    frames = []
    for i in range(sprite_sheet.get_width() // width):
        frame_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        rect = pygame.Rect(i * width, 0, width, height)
        frame_surface.blit(sprite_sheet, (0, 0), rect)
        # Scale 3x for better visibility
        frame_surface = pygame.transform.scale(frame_surface, (width * 3, height * 3))
        frames.append(frame_surface)
    return frames[:-2]


class Coin(Object):
    def __init__(self, x, y, volume):
        super().__init__(x, y, 48, 48, "Coin")
        
        self.frames = load_sprite_sheets("assets/img/coin/Coin.png", 16, 16)
        print("Loaded coin frames:", len(self.frames))
        
        self.frame_index = 0
        self.animation_speed = 0.08
        self.image = self.frames[0]

        self.collected = False
        self.sound = pygame.mixer.Sound("assets/sfx/coin.wav")
        self.sound.set_volume(volume / 100)

    def update(self, player):
        """Animate and detect collection."""
        if not self.collected:
            # Spin animation
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.frames):
                self.frame_index = 0
            self.image = self.frames[int(self.frame_index)]
            
            # Collision detection
            if self.rect.colliderect(player.rect):
                self.collected = True
                if self.sound:
                    self.sound.play()
                player.coins += 1

    def draw(self, screen, camera_x, camera_y):
        if not self.collected:
            screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
            pygame.draw.rect(screen, (255, 0, 0), 
                         pygame.Rect(self.rect.x - camera_x, self.rect.y - camera_y, 
                                     self.rect.width, self.rect.height), 2)
            
    def adj_vol(self, new_vol):
        if(new_vol == 0):
            self.sound = None
        else:
            self.sound.set_volume(new_vol / 100)