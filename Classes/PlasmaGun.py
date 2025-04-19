import pygame
from pygame import Rect
from Classes.PlayerTool import PlayerTool
from Classes.Weapon import Weapon

class PlasmaGun(PlayerTool):
    def __init__(self, power, player):
        super().__init__(10, 0, 10, 10, player)
        self.power = power
        self.cooldown = 0
        self.bullet = None
        self.color = (255, 100, 100)

        self.type = "PlasmaGun"
    
    def collision(self, others):
        if self.bullet is not None:
            self.bullet.collision(others)
    
    def draw(self, screen):
        if self.bullet is not None:
            self.bullet.draw(screen)
        pygame.draw.rect(screen, self.color, self.rect)
    
    def update(self, others):
        if self.cooldown > 0:
            self.cooldown -= 1
        if self.bullet is not None:
            self.bullet.update(others)
        self.followPlayer(self.player)
    
    def activate(self):
        if self.cooldown > 0:
            return
        self.bullet = PlasmaRay(self.player, self)
        
    def deactivate(self):
        self.bullet = None
    
class PlasmaRay(Weapon):
    def __init__(self, player, gun, width=20, height=10, color=(255, 100, 100), damage=10):
        super().__init__(player)
        self.player = player  # Keep reference to the owner
        self.color = color
        self.original_color = color  # Store original color for reset after flash effect
        self.width = width
        self.height = height
        self.damage = damage
        self.active = True
        self.speed = 10
        self.timer = 300
        self.gun = gun
        self.direction = player.direction
    
    def kill(self):
        super().kill()
        self.gun.bullet = None
    
    def update(self, others):
        self.rect = Rect(self.pos.x, self.pos.y, self.width, self.height)
        if self.timer > 0:
            self.timer -= 1
        else:
            self.kill()
        
        if self.direction == "right":
            self.pos.x += self.speed
        elif self.direction == "left":
            self.pos.x -= self.speed
        
        hits = self.check_collision(others)
        
        for hit in hits:
            self.kill()
            if hit.type == "player":
                hit.change_health(-self.damage)