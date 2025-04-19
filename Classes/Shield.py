import pygame
from Classes.PlayerModifier import PlayerModifier

class Shield(PlayerModifier):
    def __init__(self, width, height, color, player):
        super().__init__(5, 0, width, height, player)
        self.width = width
        self.height = height
        self.color = color
        self.active = False
            
        self.followPlayer(player)
    
    def check_collision(self, others):
        for other in others:
            if other.type == "player" and other != self.player:
                if other.weapon != None:
                    if self.rect.colliderect(other.weapon.rect):
                            other.weapon.blocked = True
    
    def draw(self, surface):
        if self.active:
            pygame.draw.rect(surface, self.color, self.rect)
    
    def update(self, others):
        self.followPlayer(self.player)
        if self.active:
            self.check_collision(others)
    
    def activate(self):
        self.active = True
    
    def deactivate(self):
        self.active = False