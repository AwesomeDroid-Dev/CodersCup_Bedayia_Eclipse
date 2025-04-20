import pygame
from Classes.PlayerTool import PlayerTool

class Jetboots(PlayerTool):
    def __init__(self, player):
        super().__init__(-player.width+9, 13.5, 12*3, 21*3, player)
        self.initial_jump_strength = self.player.jump_strength
        self.active = False
        
        spritesheet = pygame.image.load("./Resources/jetboots_spritesheet.png").convert_alpha()
        self.image = pygame.transform.scale(spritesheet.subsurface((0, 0, 12, 21)), (self.width, self.height))
        self.rect = self.image.get_rect()

        self.type = "jetboots"
    
    def activate(self):
        self.player.jump_strength = 2
        self.active = True
    
    def deactivate(self):
        self.player.jump_strength = self.initial_jump_strength
        self.active = False
    
    def update(self):
        self.followPlayer(self.player)
    
    def draw(self, screen):
        if self.active:
            self.player.on_ground = True
        
        if self.player.direction == "right":
            screen.blit(self.image, self.rect)
        else:
            screen.blit(pygame.transform.flip(self.image, True, False), self.rect)