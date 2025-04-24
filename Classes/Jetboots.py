import pygame
from Classes.PlayerTool import PlayerTool

class Jetboots(PlayerTool):
    def __init__(self, player):
        super().__init__(-player.width+9, 50, 35, 24, player)
        self.initial_jump_strength = self.player.jump_strength
        self.initial_speed = self.player.speed
        self.active = False
        
        spritesheet = pygame.image.load("./Resources/jetboots_spritesheet.png").convert_alpha()
        self.image = pygame.transform.scale(spritesheet.subsurface((35, 0, 35, 24)), (self.width, self.height))
        self.acive_image = pygame.transform.scale(spritesheet.subsurface((0, 0, 35, 24)), (self.width, self.height))
        self.rect = self.image.get_rect()

        self.type = "boots"
    
    def activate(self):
        self.player.jump_strength = 2
        self.player.speed = 4
        self.active = True
    
    def deactivate(self):
        self.player.on_ground = False
        self.player.jump_strength = self.initial_jump_strength
        self.player.speed = self.initial_speed
        self.active = False
    
    def update(self, others):
        self.followPlayer(self.player)
    
    def draw(self, screen):
        image = self.image
        if self.active and not self.player.on_ground:
            image = self.acive_image
        
        if self.active:
            self.player.on_ground = True
        
        if self.player.direction == "right":
            screen.blit(image, self.rect)
        else:
            screen.blit(pygame.transform.flip(image, True, False), self.rect)