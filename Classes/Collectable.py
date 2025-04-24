import pygame
from pygame.math import Vector2
from random import randint

class Collectable(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path=None, color=(255, 255, 0), item_type="health", value=10):
        super().__init__()
        self.pos = Vector2(x, y)
        self.width = width
        self.height = height
        self.item_type = item_type
        self.value = value
        self.collected = False
        self.bounce_height = 5
        self.bounce_speed = 0.05
        self.bounce_offset = 0
        self.bounce_direction = 1
        self.rotation = 0
        self.rotation_speed = 2
        
        # Set up the image
        if image_path:
            try:
                self.original_image = pygame.image.load(image_path).convert_alpha()
                self.original_image = pygame.transform.scale(self.original_image, (width, height))
            except pygame.error:
                # If image loading fails, use a colored rectangle
                self.original_image = pygame.Surface((width, height), pygame.SRCALPHA)
                pygame.draw.rect(self.original_image, color, (0, 0, width, height))
        else:
            # Create a simple rectangle with the specified color
            self.original_image = pygame.Surface((width, height), pygame.SRCALPHA)
            pygame.draw.rect(self.original_image, color, (0, 0, width, height))
        
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (self.pos.x, self.pos.y)
        
        # Sound effect
        try:
            self.collect_sound = pygame.mixer.Sound("./Sounds/collect.mp3")
        except:
            self.collect_sound = None
    
    def update(self, others, screen=None):
        if self.collected:
            return
            
        # Animate the collectable
        self.animate()
        
        # Check for collisions with players or other entities
        hits = []
        for obj in others:
            if hasattr(obj, 'type') and obj.type == "player" and self.rect.colliderect(obj.rect):
                hits.append(obj)
                
        # Apply effects to hit objects
        for hit in hits:
            self.give(hit)
            if self.collect_sound:
                self.collect_sound.play()
            self.collected = True
        
        # Draw if a screen is provided
        if screen and not self.collected:
            self.draw(screen)
    
    def animate(self):
        # Bouncing animation
        self.bounce_offset += self.bounce_speed * self.bounce_direction
        if abs(self.bounce_offset) >= self.bounce_height:
            self.bounce_direction *= -1
        
        # Update position with bounce offset
        self.rect.center = (self.pos.x, self.pos.y + self.bounce_offset)
        
        # Rotation animation
        self.rotation = (self.rotation + self.rotation_speed) % 360
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def draw(self, surface):
        if not self.collected:
            surface.blit(self.image, self.rect)
    
    def give(self, player):
        print(player)
        pass
        
    def kill(self):
        self.collected = True
        super().kill()