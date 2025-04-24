import pygame
from Classes.PlayerTool import PlayerTool


class EMPArmor(PlayerTool):
    def __init__(self, player, width=20, height=10, damage=10):
        super().__init__(0, 10, width, height, player)
        self.player = player
        self.active = False
        self.color = (255, 100, 100)
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
    
    def update(self, others, screen=None):
        self.followPlayer(self.player)
        self.draw(screen)
    
    def activate(self):
        self.active = True