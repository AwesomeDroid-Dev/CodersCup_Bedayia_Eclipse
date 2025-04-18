import pygame

class PlayerBar(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, max_value, value, color=(0, 255, 0)):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_health = max_value
        self.health = max(0, min(value, max_value))
        self.color = color

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.type = "PlayerBar"

    def draw(self, surface):
        self.rect.x = self.x
        self.rect.y = self.y
        
        # draw red background
        pygame.draw.rect(surface, (255, 0, 0), self.rect)

        # current health width
        health_ratio = self.health / self.max_health
        current_width = int(self.width * health_ratio)

        # draw green bar
        if current_width > 0:
            green_rect = pygame.Rect(self.x, self.y, current_width, self.height)
            pygame.draw.rect(surface, self.color, green_rect)

    def update(self, health):
        self.health = max(0, min(health, self.max_health))