import pygame
from pygame import Rect, Vector2

class PlayerModifier:
    def __init__(self, player, name="Generic Modifier", description="", color=(150, 150, 150)):
        # Reference to the player this modifier is attached to
        self.player = player
        
        # Basic properties all modifiers should have
        self.name = name
        self.description = description
        self.color = color
        self.active = False
        
        # Visual representation (optional)
        self.visible = False  # Whether this modifier has a visual representation
        self.width = 0
        self.height = 0
        self.pos = Vector2(0, 0)
        self.rect = None
        
        # Stats modifications
        self.stat_modifiers = {
            "speed": 0,
            "jump_strength": 0,
            "damage": 0,
            "defense": 0,
            "health": 0,
            "max_health": 0
        }
        
        # Cooldown tracking
        self.cooldown = 0
        self.max_cooldown = 0
        
    def activate(self):
        if self.cooldown <= 0:
            self.active = True
            self.cooldown = self.max_cooldown
            return True
        return False
        
    def deactivate(self):
        self.active = False
        
    def update(self, others=None):
        # Update cooldown
        if self.cooldown > 0:
            self.cooldown -= 1
            
        # Update position if this modifier has a visual representation
        if self.visible and self.rect:
            self.update_position()
    
    def update_position(self):
        # Default implementation - override in subclasses for specific positioning
        self.pos = Vector2(self.player.pos.x, self.player.pos.y)
        self.rect.topleft = (self.pos.x, self.pos.y)
        
    def draw(self, surface):
        if self.visible and self.active and self.rect:
            pygame.draw.rect(surface, self.color, self.rect)
            
    def apply_modifiers(self):
        """Apply stat modifiers to the player"""
        for stat, value in self.stat_modifiers.items():
            if hasattr(self.player, stat):
                original_value = getattr(self.player, stat)
                setattr(self.player, stat, original_value + value)
                
    def remove_modifiers(self):
        """Remove stat modifiers from the player"""
        for stat, value in self.stat_modifiers.items():
            if hasattr(self.player, stat):
                original_value = getattr(self.player, stat)
                setattr(self.player, stat, original_value - value)
                
    def on_equip(self):
        """Called when the modifier is equipped by a player"""
        self.apply_modifiers()
        
    def on_unequip(self):
        """Called when the modifier is unequipped by a player"""
        self.remove_modifiers()
        self.deactivate()
        
    def on_collision(self, other):
        """
        Handle collision with another object
        
        Args:
            other: The object this modifier collided with
            
        Returns:
            bool: True if the collision was handled, False otherwise
        """
        return False