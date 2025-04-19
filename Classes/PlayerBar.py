import pygame
from Classes.PlayerTool import PlayerTool

class PlayerBar(PlayerTool):
    def __init__(self, x, y, width, height, max_value, value, color, player):
        super().__init__(-width, 10, width, height, player)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_health = max_value
        self.health = max(0, min(value, max_value))
        self.color = color
        self.player = player

        self.rect = pygame.Rect(player.pos.x + x, player.pos.y + y, self.width, self.height)
        self.type = "PlayerBar"

    def draw(self, surface):
        # Calculate position relative to the player
        current_x = self.player.pos.x + self.x
        current_y = self.player.pos.y + self.y
        
        # Update rect position
        self.rect.x = current_x
        self.rect.y = current_y
        
        # Draw red background (empty health)
        pygame.draw.rect(surface, (255, 0, 0), self.rect)

        # Calculate current health width
        health_ratio = self.health / self.max_health
        current_width = int(self.width * health_ratio)

        # Draw filled portion with color
        if current_width > 0:
            filled_rect = pygame.Rect(current_x, current_y, current_width, self.height)
            pygame.draw.rect(surface, self.color, filled_rect)

    def update(self, value):
        # Update health/value ensuring it stays within bounds
        self.health = max(0, min(value, self.max_health))