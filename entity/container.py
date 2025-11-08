import pygame
from entity.obj import Object
from entity.star import Star

class Container(Object):
    def __init__(self, x, y, volume=100):
        super().__init__(x, y, 48, 48, "Container")

        terrain_image = pygame.image.load("assets/img/block/Terrain.png").convert_alpha()
        self.block_img = terrain_image.subsurface(pygame.Rect(0, 0, 48, 48))

        self.used = False
        self.visible = True
        self.star_spawned = False
        self.star = None
        self.volume = volume

        # Bounce animation
        self.bounce_offset = 0
        self.bouncing = False
        self.bounce_speed = -4
        self.bounce_height = 10
        self.original_y = y

    def hit_from_below(self, player):
        """Triggered when the player jumps and hits the container from below."""
        if not self.used:
            self.used = True
            self.bouncing = True

            # Spawn star just above the container
            star_x = self.rect.centerx - 8   # center horizontally
            star_y = self.rect.top - 16      # slightly above container
            self.star = Star(star_x, star_y)
            self.star_spawned = True
            print("⭐ Star released!")

    def update(self, player):
        """Update bounce and star movement."""
        if self.bouncing:
            self.rect.y += self.bounce_speed

            # Move upward until reaching max bounce height
            if self.bounce_speed < 0:
                if self.rect.y <= self.original_y - self.bounce_height:
                    self.rect.y = self.original_y - self.bounce_height
                    self.bounce_speed = abs(self.bounce_speed)  # reverse direction

            # Move downward until reaching original position
            else:
                if self.rect.y >= self.original_y:
                    self.rect.y = self.original_y
                    self.bouncing = False
                    self.bounce_speed = -4      # reset for next time
                    self.bounce_offset = 0
                    self.visible = False        # optional: hide after bounce

        if self.star_spawned and self.star:
            self.star.update(self, player)

    def draw(self, screen, camera_x, camera_y):
        """Draw the container and its star."""
        if self.visible:
            screen.blit(
                self.block_img,
                (self.rect.x - camera_x, self.rect.y - camera_y)
            )

        if self.star_spawned and self.star:
            self.star.draw(screen, camera_x, camera_y)
