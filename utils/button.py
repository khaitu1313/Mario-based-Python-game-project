import pygame

class Button:
    def __init__(self, text, pos, size):
        self.text = text
        self.rect = pygame.Rect(pos, size)
        self.color = (0, 200, 0)

    def draw(self, surface):
        
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 3)
        label = pygame.font.Font(None, int(self.rect.height * 5/6)).render(self.text, True, (255, 255, 255))
        label_rect = label.get_rect(center=self.rect.center)
        surface.blit(label, label_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)