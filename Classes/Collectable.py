import pygame
from pygame import Vector2, Rect


class Collectable(pygame.sprite.Sprite):
    def __init__(self, x, y, height, width, sprite):
        self.pos = Vector2(x, y)
        self.height = height
        self.width = width
        
        self.image = sprite
        self.rect = self.image.get_rect()
    
    def update(self, others, screen):
        hits = self.check_collisions(others)
        for hit in hits:
            self.give(hit)
            self.kill()
        self.draw(screen)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    def give(self, player):
        pass
    
    def check_collisions(self, others):
        has_hit = []
        for other in others:
            if self.rect.colliderect(other.rect):
                has_hit.append(other)
        return has_hit