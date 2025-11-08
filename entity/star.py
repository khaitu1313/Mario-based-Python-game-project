import pygame
from entity.obj import Object
import time

def load_sprite_sheets(path, width, height):
    """Load sprite sheet frames from a single row."""
    sprite_sheet = pygame.image.load(path).convert_alpha()
    frames = []
    for i in range(sprite_sheet.get_width() // width):
        frame_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        rect = pygame.Rect(i * width, 0, width, height)
        frame_surface.blit(sprite_sheet, (0, 0), rect)
        frame_surface = pygame.transform.scale(frame_surface, (width * 2, height * 2))
        frames.append(frame_surface)
    return frames


class Star(Object):
    def __init__(self, x, y, volume=100):
        width, height = 32, 32
        super().__init__(x, y, width * 2, height * 2, "Star")

        # Load correct frames (13 frames, 32x32 each)
        self.frames = load_sprite_sheets("assets/img/star/Star.png", width, height)
        self.frame_index = 0
        self.animation_speed = 0.12
        self.image = self.frames[0]

        # Movement physics
        self.vy = -3
        self.gravity = 0.2
        self.on_ground = False

        # Collection state
        self.collected = False

        # Sound
        self.sound = pygame.mixer.Sound("assets/sfx/coin.wav")
        self.sound.set_volume(volume / 100)

    def update(self, container, player=None):
        """Animate, move, and handle player collection."""
        if self.collected:
            return  # already taken, skip

        # --- Animate ---
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

        # --- Movement ---
        if not self.on_ground:
            self.vy += self.gravity
            self.rect.y += self.vy

            # Stop when landing on container top
            if self.rect.colliderect(container.rect) and self.vy > 0:
                self.rect.bottom = container.rect.top
                self.vy = 0
                self.on_ground = True

        # --- Check player collision ---
        if player and self.rect.colliderect(player.rect):
            self.collected = True
            if self.sound:
                self.sound.play()

            # Give player power-up: 2× attack speed
            if hasattr(player, "atk_speed"):
                player.atk_speed *= 2
                player.boost_start = time.time()
                if player.HP < 100:
                    player.HP += 10
            print("Player attack speed doubled!")

    def draw(self, screen, camera_x, camera_y):
        if not self.collected:
            screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
