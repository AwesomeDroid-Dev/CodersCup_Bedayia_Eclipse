import pygame
from pygame import Rect, Vector2

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, width=20, height=10, color=(255, 100, 100), damage=10):
        super().__init__()
        self.player = player  # Keep reference to the owner
        self.color = color
        self.original_color = color  # Store original color for reset after flash effect
        self.width = width
        self.height = height
        self.damage = damage
        self.active = False
        
        # Initialize position based on player's position and direction
        if player.direction == "right":
            self.pos = Vector2(player.pos.x + player.width, player.pos.y + player.height // 2 - height // 2)
        else:
            self.pos = Vector2(player.pos.x - width, player.pos.y + player.height // 2 - height // 2)
            
        self.rect = Rect(self.pos.x, self.pos.y, self.width, self.height)
        self.timer = 0  # Weapon exists for 10 frames when active
        self.has_hit = []  # Track which objects this weapon has already hit
        
    def folow_player(self, player):
        if player.direction == "right":
            self.pos = Vector2(player.pos.x + player.width, player.pos.y + player.height // 2 - self.height // 2)
        else:
            self.pos = Vector2(player.pos.x - self.width, player.pos.y + player.height // 2 - self.height // 2)
            
        self.rect = Rect(self.pos.x, self.pos.y, self.width, self.height)
        