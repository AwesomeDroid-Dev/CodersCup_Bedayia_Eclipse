import pygame
from pygame.math import Vector2
from Classes.Shield import Shield
from Classes.PlayerBar import PlayerBar
from Classes.MovableObject import MovableObject
from Classes.Weapon import Weapon

class Player(MovableObject):
    def __init__(self, x, y, width, height, color, speed):
        super().__init__(x, y, width, height, color, speed, gravity=0.5)
        self.keys = {
            'up': False,
            'down': False,
            'left': False,
            'right': False
        }
        self.on_ground = False
        self.jump_strength = 10
        self.pos = Vector2(x, y)

        self.direction = "right"
        self.max_health = 100
        self.health = 100
        self.health_bar = PlayerBar(0, -10, self.width, 5, self.max_health, self.health, (0, 255, 0), self)
        self.stamina = 100
        self.max_stamina = 100
        self.stamina_bar = PlayerBar(0, -20, self.width, 5, self.max_stamina, self.stamina, (0, 0, 255), self)
        self.weapon = None  # Initialize weapon as None, we'll create it later
        self.shield = None  # Initialize shield as None, we'll create it later
        self.attack_cooldown = 0
        
        self.type = "player"
        
        # Create the weapon once during initialization
        self.weapon = Weapon(self, width=500, height=10, color=(255, 100, 100), damage=10)
        self.shield = Shield(20, self.height, (0, 0, 255), self)

    def control(self, key, value):
        if key in self.keys:
            self.keys[key] = value

    def update(self, others, screen=None):
        self.vel.x = (self.keys['right'] - self.keys['left']) * self.speed
        
        if self.keys['up'] and self.on_ground:
            self.vel.y = -self.jump_strength
            self.on_ground = False

        self.updateVelocity(others)
        self.applyGravity(others)
        
        # Update stamina (slowly regenerate)
        if self.stamina < self.max_stamina:
            self.stamina = min(self.stamina + 0.1, self.max_stamina)
            self.stamina_bar.update(self.stamina)
        
        # Update direction based on movement
        if self.keys['right']:
            self.direction = "right"
        elif self.keys['left']:
            self.direction = "left"
            
        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
        # Update and draw the weapon if screen is provided
        if self.weapon is not None:
            self.weapon.update(others)
            if screen:
                self.weapon.draw(screen)
        
        if self.shield is not None:
            self.shield.update(others)
            if screen:
                self.shield.draw(screen)

        # Check if we're on ground
        self.on_ground = False
        self.move(0, 1)
        for obj in others:
            if self.collide(obj):
                self.on_ground = True
                break
        self.move(0, -1)

    def attack(self):
        # Activate the weapon if cooldown is complete
        if self.attack_cooldown == 0:
            self.attack_cooldown = 30  # Half second cooldown at 60fps
            self.weapon.activate()
            
            # Use some stamina for attacking
            self.change_stamina(-10)  # Use 10 stamina points

    def change_health(self, amount):
        self.health += amount
        self.health = max(0, min(self.health, self.max_health))
        self.health_bar.update(self.health)
    
    def change_stamina(self, amount):
        self.stamina += amount
        self.stamina = max(0, min(self.stamina, self.max_stamina))
        self.stamina_bar.update(self.stamina)
    
    def draw(self, surface):
        super().draw(surface)
        self.health_bar.draw(surface)
        self.stamina_bar.draw(surface)
        
        # Draw direction indicator
        center = self.rect.center
        if self.direction == "right":
            end = (center[0] + 10, center[1])
        else:
            end = (center[0] - 10, center[1])
        
        pygame.draw.line(surface, (255, 0, 0), center, end, 2)