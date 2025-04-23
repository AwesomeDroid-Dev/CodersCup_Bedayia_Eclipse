import pygame
import math
from Classes.MovableObject import MovableObject


class Boss(MovableObject):
    def __init__(self, x, y, player):
        super().__init__(x, y, 10, 10, (0, 0, 0), 0, 0)
        self.player = player
    
        self.type = "boss"

        self.rect = pygame.Rect(x, y, self.width, self.height)
    
    def update(self, *args, **kwargs):
        self.rotateAround(0.05)
        self.draw(pygame.display.get_surface())
        return super().update(*args, **kwargs)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
    
    def rotateAround(self, angle, center=(150, 150)):
        # Calculate the offset from the center
        offset_x = self.rect.centerx - center[0]
        offset_y = self.rect.centery - center[1]

        # Calculate the new position based on rotation
        new_x = center[0] + offset_x * math.cos(angle) - offset_y * math.sin(angle)
        new_y = center[1] + offset_x * math.sin(angle) + offset_y * math.cos(angle)

        # Update the position
        self.rect.center = (new_x, new_y)

    

class BossGun(MovableObject):
    def __init__(self, x, y, player):
        super().__init__(x, y, 100, 100, (0, 0, 0), 0, 0)
        self.player = player
    
    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
    
    def update(self, others):
        self.followPlayer(self.player)
        pass
    
    def followPlayer(self, player):
        self.pos = player.pos