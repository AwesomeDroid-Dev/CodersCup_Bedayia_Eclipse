import pygame
from Classes.PlayerModifier import PlayerModifier

class Shield(PlayerModifier):
    def __init__(self, x, y, width, height, color, player):
        super().__init__(10, player.height /2, width, height, player)
        self.width = width
        self.height = height
        self.color = color
        self.active = False
            
        self.followPlayer(player)
    
    def check_collision(self, others):
        for other in others:
            if other.type == "player":
                if self.rect.colliderect(other.rect):
                    if other.weapon != None:
                        other.weapon.blocked = True
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
    
    def update(self):
        self.followPlayer(self.player)
        self.draw(self.player.screen)
        if self.active:
            self.check_collision(self.player.others)
    
    def activate(self):
        self.active = True