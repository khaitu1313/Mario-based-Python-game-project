import pygame

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        # Create a surface for the portal
        self.image = pygame.Surface((width, height))
        self.image.fill((128, 128, 128))  # gray color (R,G,B)
        
        # Optional: add a border to make it stand out
        pygame.draw.rect(self.image, (200, 200, 200), self.image.get_rect(), 3)

        # Set up rectangle for positioning
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def draw(self, surface, camera_x=0, camera_y=0):
        """Draw portal relative to camera offset."""
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
