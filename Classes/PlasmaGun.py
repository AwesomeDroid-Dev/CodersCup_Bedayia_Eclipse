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
        self.explosion = None
        self.color = (255, 100, 100)
        self.type = "PlasmaGun"
    
    def collision(self, others):
        if self.bullet is not None:
            self.bullet.collision(others)
    
    def draw(self, screen):
        if self.bullet is not None:
            self.bullet.draw(screen)
        if self.explosion is not None:
            self.explosion.draw(screen)
        pygame.draw.rect(screen, self.color, self.rect)
    
    def update(self, others):
        if self.cooldown > 0:
            self.cooldown -= 1
        if self.bullet is not None:
            self.bullet.update(others)
        if self.explosion is not None:
            self.explosion.update()
            if not self.explosion.active:
                self.explosion = None
        self.followPlayer(self.player)
    
    def activate(self):
        if self.cooldown > 0:
            return
        self.bullet = PlasmaBullet(self.player, self)
        self.cooldown = 30
        
    def deactivate(self):
        self.bullet = None

class PlasmaBullet(Weapon):
    def __init__(self, player, gun, width=20, height=10, color=(255, 100, 100), damage=10):
        super().__init__(player, damage)
        self.color = color
        self.original_color = color
        self.width = width
        self.height = height
        self.active = True
        self.speed = 10
        self.timer = 300
        self.gun = gun
        self.direction = player.direction
        self.pos = pygame.math.Vector2(player.rect.centerx, player.rect.centery)
    
    def kill(self):
        super().kill()
        self.gun.bullet = None
    
    def update(self, others):
        self.rect = Rect(int(self.pos.x), int(self.pos.y), self.width, self.height)
        if self.timer > 0:
            self.timer -= 1
        else:
            self.kill()
        
        # Update position based on direction
        if self.direction == "right":
            self.pos.x += self.speed
        elif self.direction == "left":
            self.pos.x -= self.speed
        
        # Check for collisions
        hits = self.check_collision(others)
        if hits:
            self.kill()
            # Create charging effect instead of immediate explosion
            self.gun.explosion = PlasmaExplosion(self.player, self.pos, others)

class PlasmaExplosion(Weapon):
    def __init__(self, player, pos, others, radius=40, color=(255, 100, 100), damage=30):
        super().__init__(player, damage)
        self.color = color
        self.original_color = color
        self.radius = radius
        self.active = True
        self.speed = 10
        self.timer = 300
        self.pos = pos
        self.others = others
        self.timer = 20
        self.rect = Rect(int(self.pos.x), int(self.pos.y), self.radius, self.radius)
    
    def charge(self):
        self.timer = 0
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.pos, self.radius)
    
    def kill(self):
        self.active = False
    
    def update(self):
        if self.timer > 0:
            self.timer -= 1
        else:
            self.explode()
            self.kill()
    
    def explode(self):
        hits = self.check_collision(self.others)
        for hit in hits:
            if hit.type == "player":
                hit.change_health(-self.damage)