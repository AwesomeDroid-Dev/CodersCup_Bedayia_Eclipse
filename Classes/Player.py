import pygame
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

        self.max_health = 100
        self.health = 100
        self.health_bar = PlayerBar(self.pos.x, self.pos.y - 10, self.width, 5, self.max_health, self.health)
        self.direction = "right"
        self.weapon = None  # Initialize weapon as None, we'll create it later
        self.attack_cooldown = 0
        
        self.type = "player"
        
        # Create the weapon once during initialization
        self.weapon = Weapon(self, width=20, height=10, color=(255, 100, 100), damage=10)

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
        
        self.health_bar.x = self.pos.x
        self.health_bar.y = self.pos.y - 10
        
        # Update and draw the weapon if screen is provided
        if self.weapon is not None:
            # Update weapon position based on player's current position and direction
            if self.direction == "right":
                self.weapon.pos.x = self.pos.x + self.width
            else:
                self.weapon.pos.x = self.pos.x - self.weapon.width
                
            self.weapon.pos.y = self.pos.y + self.height // 2 - self.weapon.height // 2
            self.weapon.rect.topleft = (self.weapon.pos.x, self.weapon.pos.y)
            
            self.weapon.update(others)
            if screen and self.weapon.active:
                self.weapon.draw(screen)

        self.on_ground = False
        self.move(0, 1)
        for obj in others:
            if self.collide(obj):
                self.on_ground = True
                break
        self.move(0, -1)
        
        if self.keys['right']:
            self.direction = "right"
        elif self.keys['left']:
            self.direction = "left"
            
        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def attack(self):
        # Activate the weapon if cooldown is complete
        if self.attack_cooldown == 0:
            self.attack_cooldown = 30  # Half second cooldown at 60fps
            self.weapon.activate()

    def change_health(self, amount):
        self.health += amount
        self.health = max(0, min(self.health, self.max_health))
        self.health_bar.update(self.health)
    
    def draw(self, surface):
        super().draw(surface)
        self.health_bar.draw(surface)
        
        center = self.rect.center
        if self.direction == "right":
            end = (center[0] + 10, center[1])
        else:
            end = (center[0] - 10, center[1])
        
        pygame.draw.line(surface, (255, 0, 0), center, end, 2)