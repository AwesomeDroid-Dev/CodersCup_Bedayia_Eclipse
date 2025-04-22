import pygame
from pygame.math import Vector2
from Classes.MovableObject import MovableObject
from Classes.PeletLauncher import PelletExplosion  # Add PelletExplosion import

class Boss(MovableObject):
    def __init__(self, x, y, enemy):
        super().__init__(x, y, 50, 50, (255, 0, 0), 0, 0)
        self.enemy = enemy
        self.pelets = []
        self.explosions = []  # New list to track explosions
        self.type = "boss"
        self.damage_source = self  # For damage attribution

    def update(self, others, screen):
        super().update(others)
        self.timer = getattr(self, 'timer', 0) + 1
        
        # Pellet spawning
        if self.timer >= 20:
            self.shoot()
            self.timer = 0
            
        # Update pellets and handle explosions
        new_pellets = []
        for pellet in self.pelets:
            pellet.update(others)
            pellet.draw(screen)
            
            if pellet.active:
                new_pellets.append(pellet)
            else:
                # Create explosion when pellet becomes inactive
                self.explosions.append(
                    PelletExplosion(self.damage_source, pellet.pos.copy(), others, damage=15)
                )
        self.pelets = new_pellets
        
        # Update explosions
        self.explosions = [exp for exp in self.explosions if exp.active]
        for explosion in self.explosions:
            explosion.update()
            explosion.draw(screen)

    def shoot(self):
        direction_vector = (self.enemy.pos - self.pos).normalize()
        pellet_speed = 8
        direction_vector *= pellet_speed
        # Pass the Boss as the owner instead of player
        new_pellet = Pellet(self.damage_source, self, dir=direction_vector)
        self.pelets.append(new_pellet)

class Pellet(MovableObject):
    def __init__(self, owner, launcher, width=15, height=15, color=(200, 150, 100), damage=8, dir=None):
        super().__init__(launcher.rect.centerx, launcher.rect.centery-12, width, height, color, speed=8, gravity=0.3)
        self.owner = owner  # Changed from 'player' to generic 'owner'
        self.damage = damage
        self.launcher = launcher
        self.active = True
        self.lifetime = 20
        if dir is not None:
            self.vel = dir