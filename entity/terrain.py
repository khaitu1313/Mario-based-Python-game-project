import pygame
import sys
import os
from os.path import join
from entity.obj import Object
def get_block(size):
    path = join("assets", "img", "block", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)
class Terrain(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size, "terrain")
        self.image.blit(get_block(size), (0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        
        
        