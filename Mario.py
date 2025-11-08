import pygame
import random
import sys
import time
import os   # to check if image exists
from Loops.menu import menu
from Loops.game import game
from Loops.about import about

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 1400, 800


pygame.display.set_caption("MAWIO")

running = True
state = "menu"
sound_volume = 50
level = 1
coin = 0

while running:
    print(f"Current State: {state}")
    
    if state == "menu":
        state, WIDTH, HEIGHT, sound_volume, coin  = menu(WIDTH, HEIGHT, sound_volume, coin)
    elif state == "about":
        state, WIDTH, HEIGHT, sound_volume = about(WIDTH, HEIGHT,sound_volume)
    elif state == "game":
        state, WIDTH, HEIGHT, sound_volume, level, coin = game(WIDTH, HEIGHT,sound_volume, level, coin)
    else:
        running = False
    
    
    

