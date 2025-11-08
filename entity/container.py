import pygame
from entity.obj import Object
from entity.star import Star

class Container(Object):
    def __init__(self, x, y, volume=100):
        super().__init__(x, y, 48, 48, "Container")

        # Load terrain image once
        terrain_image = pygame.image.load("assets/img/block/Terrain.png").convert_alpha()

        # --- SELECT BLOCK TILE AREA ---
        # Example: top-left block (0,0) with size 48x48
        self.block_img = terrain_image.subsurface(pygame.Rect(0, 0, 48, 48))

        # Create a "used"/dim version
        self.used_block_img = self.block_img.copy()
        dark_surface = pygame.Surface((48, 48))
        dark_surface.fill((60, 60, 60))
        self.used_block_img.blit(dark_surface, (0, 0), special_flags=pygame.BLEND_RGB_MULT)

        # States
        self.used = False
        self.star_spawned = False
        self.star = None
        self.volume = volume
        self.visible = True   # <--- NEW FLAG: for hiding after bounce

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

            # Spawn star slightly above
            self.star = Star(self.rect.centerx - 16, self.rect.y - 60, self.volume)
            self.star_spawned = True
            print("⭐ Star released!")

    def update(self, player):
        """Update bounce animation and hide after finished."""
        if not self.visible:
            return  # stop updating if already gone

        # Bounce animation
        if self.bouncing:
            self.rect.y += self.bounce_speed
            self.bounce_offset += abs(self.bounce_speed)

            # Reverse direction at max height
            if self.bounce_offset >= self.bounce_height:
                self.bounce_speed *= -1

            # Stop when back to original position
            if self.bounce_speed > 0 and self.rect.y >= self.original_y:
                self.rect.y = self.original_y
                self.bouncing = False
                self.bounce_speed = -4
                self.bounce_offset = 0

                # After the bounce finishes → make the container disappear
                if self.used and self.star_spawned:
                    self.visible = False  # <--- now hidden
                    print("🟫 Container disappeared after releasing star")

        # Update star
        if self.star_spawned and self.star:
            self.star.update(player)

    def draw(self, screen, camera_x, camera_y):
        """Draw container and star."""
        if self.visible:  # <--- skip drawing when hidden
            img = self.used_block_img if self.used else self.block_img
            screen.blit(
                img,
                (self.rect.x - camera_x, self.rect.y - camera_y)
            )

        # Always draw star (even if container hidden)
        if self.star_spawned and self.star:
            self.star.draw(screen, camera_x, camera_y)
