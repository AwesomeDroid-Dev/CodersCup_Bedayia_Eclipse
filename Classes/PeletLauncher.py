import pygame
from pygame import Rect
from Classes.PlayerTool import PlayerTool
from Classes.Weapon import Weapon
from Classes.MovableObject import MovableObject

class PelletLauncher(PlayerTool):
    def __init__(self, player):
        super().__init__(-player.width/2+12, 0, 12*3, 21*3, player)
        self.cooldown = 0
        self.pellet = None
        self.explosion = None
        
        # Try to load the image, with fallback to a basic rectangle
        try:
            spritesheet = pygame.image.load("./Resources/plasmagun_spritesheet.png").convert_alpha()
            self.image = pygame.transform.scale(spritesheet.subsurface((8, 0, 12, 21)), (self.width, self.height))
            self.active_image = pygame.transform.scale(spritesheet.subsurface((29, 0, 12, 21)), (self.width, self.height))
        except:
            # Create a simple rectangle if image loading fails
            self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (100, 100, 200), (0, 0, self.width, self.height))
            self.active_image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.rect(self.active_image, (150, 150, 250), (0, 0, self.width, self.height))
            
        self.rect = self.image.get_rect()
        self.type = "PelletLauncher"
    
    def collision(self, others):
        if self.pellet is not None:
            self.pellet.collision(others)
    
    def draw(self, screen):
        image = self.image
        
        if self.pellet is not None:
            self.pellet.draw(screen)
        if self.explosion is not None:
            self.explosion.draw(screen)
            
        if self.cooldown > 0:
            image = self.active_image
        
        if self.player.direction == "right":
            screen.blit(image, self.rect)
        else:
            screen.blit(pygame.transform.flip(image, True, False), self.rect)
    
    def update(self, others):
        if self.cooldown > 0:
            self.cooldown -= 1
        if self.pellet is not None:
            self.pellet.update(others)
            # Check if the pellet has reached its timer limit
            if not self.pellet.active:
                # Create an explosion at the pellet's current position
                self.explosion = PelletExplosion(self.player, self.pellet.pos.copy(), others)
                self.pellet = None
                
        if self.explosion is not None:
            self.explosion.update()
            if not self.explosion.active:
                self.explosion = None
                
        self.followPlayer(self.player)
    
    def activate(self):
        if self.cooldown > 0 or self.pellet is not None:
            return
            
        self.player.change_fuel(-5)  # Use less fuel than plasma gun
        self.pellet = Pellet(self.player, self)
        self.cooldown = 60  # Slightly faster cooldown than plasma gun
        
    def deactivate(self):
        if self.pellet is not None:
            # Force the pellet to explode immediately
            self.explosion = PelletExplosion(self.player, self.pellet.pos.copy(), [])
            self.pellet = None


class Pellet(MovableObject):
    def __init__(self, owner, launcher, width=15, height=15, color=(200, 150, 100), damage=8, dir=None):
        super().__init__(
            launcher.rect.centerx, 
            launcher.rect.centery-12, 
            width, height, color, speed=8, gravity=0.3
        )
        self.owner = owner  # Changed from 'player' to generic 'owner'
        self.damage = damage
        self.launcher = launcher
        self.active = True
        self.lifetime = 20
        if dir is not None:
            self.vel = dir
        
        # Try to load the image, with fallback to a basic circle
        try:
            image = pygame.image.load('./Resources/plasma_bullet.png').convert_alpha()
            self.image = pygame.transform.scale(image, (self.width, self.height))
        except:
            # Create a simple circle if image loading fails
            self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.circle(self.image, color, (width//2, height//2), width//2)
        
        if dir is None:
            self.direction = owner.direction
            self.rect = self.image.get_rect()
            
            # Initial velocity based on player direction
            initial_speed = 15
            if self.direction == "right":
                self.vel.x = initial_speed
            else:
                self.vel.x = -initial_speed
        
            
    def kill(self):
        self.active = False
    
    def collision(self, others):
        for other in others:
            if other != self.owner and self.rect.colliderect(other.rect):  # Use 'owner' instead of 'player'
                if other.type == "player":
                    other.change_health(-self.damage)
                self.kill()
                return True
        return False
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def update(self, others):
        if not self.active:
            return
            
        # Update lifetime
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()
            return
        
        # Handle physics
        self.updateVelocity([obj for obj in others if obj != self.owner and obj != self])
        self.applyGravity([obj for obj in others if obj != self.owner and obj != self])
        
        # Check for collisions
        if self.collision(others):
            return


class PelletExplosion(Weapon):
    def __init__(self, owner, pos, others, radius=60, color=(200, 150, 50), damage=15):
        super().__init__(owner, width=radius*2, height=radius*2, color=color, damage=damage)
        self.radius = radius
        self.active = True
        self.pos = pos
        self.pos.x -= self.radius  # Center the explosion
        self.pos.y -= self.radius
        self.others = others
        self.timer = 15  # Shorter duration than plasma explosion
        self.expansion_phase = 5  # Ticks for expansion
        self.current_size = 0.1  # Start small
        self.rect = Rect(int(self.pos.x), int(self.pos.y), self.radius*2, self.radius*2)
    
    def draw(self, surface):
        if not self.active:
            return
            
        # Calculate current size based on expansion phase
        if self.expansion_phase > 0:
            size_factor = 1 - (self.expansion_phase / 5)
            current_radius = int(self.radius * size_factor)
        else:
            current_radius = self.radius * (self.timer / 10)  # Fade out
        
        # Create gradient explosion
        surf = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        
        # Outer explosion ring
        alpha = min(255, int(255 * (self.timer / 15)))
        outer_color = (*self.color, alpha)
        pygame.draw.circle(surf, outer_color, (self.radius, self.radius), current_radius)
        
        # Inner brighter core
        inner_radius = max(3, int(current_radius * 0.6))
        inner_color = (255, 200, 100, alpha)
        pygame.draw.circle(surf, inner_color, (self.radius, self.radius), inner_radius)
        
        surface.blit(surf, (self.pos.x, self.pos.y))
    
    def update(self):
        if not self.active:
            return
            
        if self.expansion_phase > 0:
            self.expansion_phase -= 1
            hits = self.check_collision(self.others)
            for hit in hits:
                # Changed check to exclude the explosion owner
                if hit.type == "player" and hit != self.owner:
                    hit.change_health(-self.damage)
        else:
            self.timer -= 1
            if self.timer <= 0:
                self.active = False