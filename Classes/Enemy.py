import pygame
import random
from Classes.Player import Player

class Enemy(Player):
    def __init__(self, x, y, width, height, color, speed, level=1):
        super().__init__(x, y, width, height, color, speed)
        
        # Override player attributes with enemy-specific values
        self.level = level
        self.max_health = 50 + level * 20
        self.health = self.max_health
        self.strength = 5 + level * 2
        self.health_bar.update(self.health)  # Update the health bar with new max health
        self.health_bar.color = (255, 0, 0)  # Red health bar for enemies
        
        # AI behavior settings
        self.attack_range = 70
        self.detection_range = 300
        self.attack_cooldown = 0
        self.attack_cooldown_max = int(60 * (1.0 - min(level * 0.05, 0.7)))  # Decreases with level
        self.jump_probability = min(0.01 + level * 0.005, 0.05)
        
        # Default direction for enemies is left (facing player)
        self.direction = "left"
        
        # Load enemy sprite instead of player sprite
        spritesheet = pygame.image.load("./Resources/player_spritesheet_2.png").convert_alpha()
        self.image = pygame.transform.scale(spritesheet.subsurface((0, 0, 12, 21)), (self.width, self.height))
        self.holding_image = pygame.transform.scale(spritesheet.subsurface((21, 0, 12, 21)), (self.width, self.height))
        self.rect = self.image.get_rect()
        
        self.type = "enemy"

    def update(self, others, screen=None):
        # Find player in the list of objects
        player = None
        for obj in others:
            if obj.type == "player":
                player = obj
                break
        
        # AI decision making if player exists
        if player:
            self.ai_update(player)
        
        # Call the parent update method (Player update)
        super().update(others, screen)

    def ai_update(self, player):
        # Reset keys
        for key in self.keys:
            self.keys[key] = False
            
        # Calculate distance to player
        distance_x = player.pos.x - self.pos.x
        distance = abs(distance_x)
        
        # If player is in detection range
        if distance < self.detection_range:
            # Move towards player
            if distance_x > self.attack_range:
                self.keys['right'] = True
                self.direction = "right"
            elif distance_x < -self.attack_range:
                self.keys['left'] = True
                self.direction = "left"
            
            # Random jumping
            if self.on_ground and random.random() < self.jump_probability:
                self.keys['up'] = True
                
            # Attack if in range and cooldown is done
            if self.weapon and self.attack_cooldown <= 0 and distance < self.attack_range:
                self.weapon.activate()
                self.attack_cooldown = self.attack_cooldown_max
                
        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def draw(self, screen):
        # Draw health bar (inherited from Player)
        super().draw(screen)
        
        # Additionally draw level indicator
        level_text = pygame.font.SysFont('Arial', 16).render(f"Lvl {self.level}", True, (255, 255, 255))
        level_rect = level_text.get_rect()
        level_rect.centerx = self.rect.centerx
        level_rect.bottom = self.rect.top - 15
        screen.blit(level_text, level_rect)