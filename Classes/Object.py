import pygame
from pygame import Rect, Vector2

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, invisible=False):
        super().__init__()
        self.pos = Vector2(x, y)
        self.width = width
        self.height = height
        self.color = color
        self.dir = 90
        self.invisible = invisible
        self.rect = Rect(self.pos.x, self.pos.y, self.width, self.height)
        
        self.type = "object"

    def draw(self, surface):
        if self.invisible:
            return
        pygame.draw.rect(surface, self.color, self.rect)

    def move(self, dx, dy):
        self.pos.x += dx
        self.pos.y += dy
        self.rect.topleft = (self.pos.x, self.pos.y)

    def collide(self, other):
        return self.rect.colliderect(other.rect)