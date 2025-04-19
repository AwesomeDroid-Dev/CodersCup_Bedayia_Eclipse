import pygame
from pygame import Rect
from Classes.PlayerTool import PlayerTool

class Weapon(PlayerTool):
    def __init__(self, player, width=20, height=10, color=(255, 100, 100), damage=10):
        super().__init__(0, 10, width, height, player)
        self.player = player  # Keep reference to the owner
        self.color = color
        self.original_color = color  # Store original color for reset after flash effect
        self.width = width
        self.height = height
        self.damage = damage
        self.active = False
        self.cooldown = 0
        
        self.rect = Rect(self.pos.x, self.pos.y, self.width, self.height)
        self.timer = 0  # Weapon exists for 10 frames when active
        self.has_hit = []  # Track which objects this weapon has already hit
        
    def check_collision(self, others):
        hits = []
        for other in others:
            # Don't hit the weapon's owner or objects already hit
            if other != self.player and other not in self.has_hit:
                if self.rect.colliderect(other.rect):
                    self.has_hit.append(other)
                    hits.append(other)
        return hits

    def update(self, others):
        self.followPlayer(self.player)
        if self.cooldown > 0:
            self.cooldown -= 1
        # Only check collisions if the weapon is active
        if self.active:
            hits = self.check_collision(others)
            for hit in hits:
                if hit.type == "player":
                    hit.change_health(-self.damage)
                    # Make the weapon flash on hit
                    self.color = (255, 0, 0)
            
            # Count down the timer
            if self.timer > 0:
                self.timer -= 1
            else:
                self.active = False
                self.color = self.original_color  # Reset color after deactivation

    def draw(self, surface):
        self.rect = Rect(self.pos.x, self.pos.y, self.width, self.height)
        if self.active:
            pygame.draw.rect(surface, self.color, self.rect)
    
    def activate(self):
        if self.cooldown > 0:
            return
        self.active = True
        self.cooldown = 30
        self.timer = 10
        self.has_hit = []  # Reset the hit list
        self.color = self.original_color  # Reset color when activating