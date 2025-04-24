import pygame
from Classes.Axe import Axe
from Classes.Player import Player

class AxeWarrior(Player):
    def __init__(self, x, y, width, height, player, speed=9):
        super().__init__(x, y, width, height, "./Resources/axewarrior_spritesheet.png", speed)
        self.boots = None
        self.player = player
        self.max_reaction = 15
        self.reaction = 15
        spritesheet = pygame.image.load("./Resources/axewarrior_spritesheet.png").convert_alpha()
        self.image = spritesheet.subsurface(pygame.Rect(0, 0, 25, 30))
        self.holding_image = spritesheet.subsurface(pygame.Rect(24, 0, 25, 30))
        self.rect = self.image.get_rect(center=self.pos)
        self.weapon = Axe(-10, 10, 50, 50, self)

        self.type = "AIPlayer"
    
    def update(self, others, screen=None):
        self.reaction -= 1
        if self.reaction == 0:
            if self.pos.distance_to(self.player.pos) < 100:
                self.attack_player(self.player)
            else:
                self.move_towards_player(self.player)
            self.reaction = self.max_reaction
        
        return super().update(others, screen)
    
    def draw(self, screen):
        return super().draw(screen)
    
    def move_towards_player(self, player):
        # Reset all controls
        self.reset_controls()
        
        if player.pos.x < self.pos.x:
            self.control("left", True)
        else:
            self.control("right", True)
    
    def attack_player(self, player):
        # Reset all controls
        self.reset_controls()
        
        self.control("attack", True)
    
    
    def reset_controls(self):
        self.control("right", False)
        self.control("left", False)
        self.control("down", False)
        self.control("up", False)
        self.control("attack", False)
        self.control("boots", False)