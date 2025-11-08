import pygame
from entity.obj import Object
from entity.player import Player

def load_sprite_sheets(path, width, height):
    sprite_sheet = pygame.image.load(path).convert_alpha()
    frames = []
    for i in range(sprite_sheet.get_width() // width):
        frame_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        rect = pygame.Rect(i * width, 0, width, height)
        frame_surface.blit(sprite_sheet, (0, 0), rect)
        frame_surface = pygame.transform.scale(frame_surface, (width * 3, height * 3))
        frames.append(frame_surface)
    return frames


class Star(Object):
    def __init__(self, x, y, volume):
        super().__init__(x, y, 48, 48, "Star")

        # Load animation
        self.frames = load_sprite_sheets("assets/img/star/Star.png", 16, 16)
        print("Loaded star frames:", len(self.frames))
        self.frame_index = 0
        self.animation_speed = 0.08
        self.image = self.frames[0]

        # Physics
        self.vx = 2       # small horizontal move
        self.vy = -3      # initial pop-up
        self.gravity = 0.3

        # States
        self.collected = False
        self.sound = None
        if pygame.mixer.get_init():
            try:
                self.sound = pygame.mixer.Sound("assets/sfx/star.wav")
                self.sound.set_volume(volume / 100)
            except Exception:
                print("Star sound not found, skipping audio.")

    def update(self, player, blocks=None):
        """Update star physics and handle collisions."""
        if self.collected:
            return

        if blocks is None:
            blocks = []  # fallback if not passed

        # Apply gravity
        self.vy += self.gravity
        self.rect.y += self.vy

        # --- Vertical collision ---
        for block in blocks:
            if self.rect.colliderect(block.rect):
                if self.vy > 0:  # falling down
                    self.rect.bottom = block.rect.top
                    self.vy = 0
                elif self.vy < 0:  # hitting ceiling
                    self.rect.top = block.rect.bottom
                    self.vy = 0

        # --- Horizontal movement ---
        self.rect.x += self.vx
        for block in blocks:
            if self.rect.colliderect(block.rect):
                # Stop horizontal movement if hit wall
                if self.vx > 0:
                    self.rect.right = block.rect.left
                elif self.vx < 0:
                    self.rect.left = block.rect.right
                self.vx = 0  # stop moving horizontally

        # --- Animation ---
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

        # --- Collision with player ---
        if self.rect.colliderect(player.rect):
            self.collected = True
            if self.sound:
                self.sound.play()
            if hasattr(player, "atk_speed"):
                player.atk_speed *= 2
            print("⭐ Star collected!")

    def draw(self, screen, camera_x, camera_y):
        """Draw star if not collected."""
        if not self.collected:
            screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

    def adj_vol(self, new_vol):
        if not self.sound:
            return
        if new_vol == 0:
            self.sound = None
        else:
            self.sound.set_volume(new_vol / 100)
