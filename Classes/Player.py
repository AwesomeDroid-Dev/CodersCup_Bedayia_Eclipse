import pygame
from pygame.math import Vector2
from Classes.Axe import Axe
from Classes.Jetboots import Jetboots
from Classes.PlayerBar import PlayerBar
from Classes.MovableObject import MovableObject
from Classes.Weapon import Weapon
from Classes.PlasmaGun import PlasmaGun
from Classes.PeletLauncher import PelletLauncher

class Player(MovableObject):
    def __init__(self, x, y, width, height, image, speed):
        super().__init__(x, y, width, height, (0, 0, 0), speed, gravity=0.5)
        self.keys = {
            'up': False,
            'down': False,
            'left': False,
            'right': False,
            'attack': False,
            'boots': False
        }
        self.prev_keys = {
            'up': False,
            'down': False,
            'left': False,
            'right': False,
            'attack': False,
            'boots': False
        }
        self.on_ground = False
        self.jump_strength = 10
        self.pos = Vector2(x, y)

        self.direction = "right"
        self.max_health = 100
        self.health = 100
        self.health_bar = PlayerBar(0, -20, 60, 12, self.max_health, self.health, (0, 255, 0), self)
        self.weapon = None
        self.boots = None
        spritesheet = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(spritesheet.subsurface((21, 0, 12, 21)), (self.width, self.height))
        self.holding_image = pygame.transform.scale(spritesheet.subsurface((0, 0, 12, 21)), (self.width, self.height))
        #spritesheet = pygame.image.load("./Resources/player_spritesheet_2.jpg").convert_alpha()
        #self.image = pygame.transform.scale(spritesheet.subsurface((195, 50, 55, 50)), (self.width, self.height))
        self.rect = self.image.get_rect()
        
        self.type = "player"
        
        #self.weapon = PlasmaGun(10, self)
        #self.weapon = ForceGloves(self)
        #self.weapon = Weapon(self, 10, 5, (255, 0, 0), 10)
        #self.weapon = PelletLauncher(self)
        self.weapon = Axe(10, -10, 50, 50, self)
        self.boots = Jetboots(self)

    def control(self, key, value):
        if key in self.keys:
            self.keys[key] = value

    def update(self, others, screen=None):
        if self.keys['attack'] and self.weapon is not None and self.weapon.cooldown == 0:
            self.attack()

        if self.keys['boots'] and self.boots is not None:
            if self.prev_keys['boots'] == False:
                if self.boots.active == False:
                    self.boots.activate()
                else:
                    self.boots.deactivate()
                self.prev_keys['boots'] = self.keys['boots']
        else:
            self.prev_keys['boots'] = self.keys['boots']
        
        self.vel.x = (self.keys['right'] - self.keys['left']) * self.speed
        
        if self.keys['up'] and self.on_ground:
            self.vel.y = -self.jump_strength
            self.on_ground = False

        self.updateVelocity(others)
        self.applyGravity(others)
        
        # Update stamina (slowly regenerate)
        #if self.stamina < self.max_stamina:
        #    self.stamina = min(self.stamina + 0.1, self.max_stamina)
        #    self.stamina_bar.update(self.stamina)
        
        # Update direction based on movement
        if self.keys['right']:
            self.direction = "right"
        elif self.keys['left']:
            self.direction = "left"
            
        # Draw the player
        if screen is not None:
            self.draw(screen)

        # Check if we're on ground
        self.on_ground = False
        self.move(0, 1)
        for obj in others:
            if self.collide(obj):
                self.on_ground = True
                break
        self.move(0, -1)
        
        if self.weapon is not None:
            self.weapon.update(others)
            if screen:
                self.weapon.draw(screen)
    
        if self.boots is not None:
            self.boots.update()
            if screen:
                self.boots.draw(screen)

    def attack(self):
        self.weapon.activate()
        
        # Use some stamina for attacking
        #self.change_stamina(-10)  # Use 10 stamina points

    def change_health(self, amount):
        self.health += amount
        self.health = max(0, min(self.health, self.max_health))
        self.health_bar.update(self.health)
    
    #def change_stamina(self, amount):
    #    self.stamina += amount
    #    self.stamina = max(0, min(self.stamina, self.max_stamina))
    #    self.stamina_bar.update(self.stamina)
    
    def draw(self, screen):
        self.health_bar.draw(screen)
        image = self.image
        if self.weapon is not None:
            image = self.holding_image
        
        # Draw direction indicator
        #center = self.rect.center
        #if self.direction == "right":
        #    end = (center[0] + 10, center[1])
        #else:
        #    end = (center[0] - 10, center[1])
        
        #pygame.draw.line(surface, (255, 0, 0), center, end, 2)
        if self.direction == "right":
            screen.blit(image, self.rect)
        else:
            screen.blit(pygame.transform.flip(image, True, False), self.rect)