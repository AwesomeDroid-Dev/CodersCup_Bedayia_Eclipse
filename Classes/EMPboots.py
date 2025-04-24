import pygame
from pygame import Rect
from pygame.math import Vector2
from Classes.PlayerTool import PlayerTool
from Classes.Weapon import Weapon

class EMPboots(PlayerTool):
    def __init__(self, player):
        super().__init__(-player.width+9, 50, 35, 24, player)
        self.player = player
        self.active = False
        self.cooldown = 0
        self.emp_wave = None
        self.color = (0, 200, 255)  # Bright blue color for EMP boots
        
        image = pygame.image.load("./Resources/empboots.png").convert_alpha()
        self.image = pygame.transform.scale((image), (self.width, self.height))
        self.rect = self.image.get_rect()

        self.type = "boots"
    
    def draw(self, surface):
        if self.emp_wave is not None:
            self.emp_wave.draw(surface)
        
        if self.player.direction == "right":
            surface.blit(self.image, self.rect)
        else:
            surface.blit(pygame.transform.flip(self.image, True, False), self.rect)
    
    def update(self, others=None):
        self.followPlayer(self.player)
        
        if self.cooldown > 0:
            self.cooldown -= 1
            
        if self.emp_wave is not None:
            self.emp_wave.update(others)
            if not self.emp_wave.active:
                self.emp_wave = None
    
    def activate(self):
        if self.cooldown > 0 or self.emp_wave is not None:
            return
            
        # Create the EMP wave centered on the player
        self.emp_wave = EMPWave(self.player)
        self.cooldown = 60  # 1 second at 60 FPS
    
    def deactivate(self):
        pass  # EMP wave continues until it's complete

class EMPWave(Weapon):
    def __init__(self, player, damage=10, push_force=12):
        # Create a weapon with initial small size
        screen_width, screen_height = 800, 600  # Default screen size, adjust as needed
        max_radius = max(screen_width, screen_height)  # Make sure it covers entire screen
        
        super().__init__(player, 
                       width=10,  # Start small
                       height=10,
                       color=(30, 150, 255),
                       damage=damage)
        
        # Wave parameters
        self.max_radius = max_radius
        self.current_radius = 10  # Start with small radius
        self.growth_rate = 8  # How fast the wave expands
        self.push_force = push_force  # How strong the push effect is
        
        # Wave status
        self.active = True
        self.affected_objects = []  # Track which objects have been affected
        
        # Override rectangle
        self.rect = Rect(int(player.rect.centerx - 5), int(player.rect.centery - 5), 10, 10)
    
    def check_collision(self, others):
        hits = []
        
        # Calculate the ring boundaries
        inner_radius = max(0, self.current_radius - 10)
        outer_radius = self.current_radius
        
        center_x = self.player.rect.centerx
        center_y = self.player.rect.centery
                
        for other in others:
            # Skip the player who created the wave
            if other == self.player:
                continue
                
            # Get other object's center
            other_center_x = other.rect.centerx
            other_center_y = other.rect.centery
            
            # Calculate distance from center
            dx = other_center_x - center_x
            dy = other_center_y - center_y
            distance = (dx**2 + dy**2)**0.5
            # Check if object is touching the wave ring
            if inner_radius <= distance <= outer_radius and other.type == "player":
                if other not in self.affected_objects:
                    self.affected_objects.append(other)
                    hits.append(other)
            
        return hits

    def update(self, others, screen=None):
        if not self.active:
            return

        # Expand the radius
        self.current_radius += self.growth_rate
        
        # Update the circle size
        center_x = self.player.rect.centerx
        center_y = self.player.rect.centery
        self.rect = Rect(
            center_x - self.current_radius, 
            center_y - self.current_radius,
            self.current_radius * 2, 
            self.current_radius * 2
        )
                
        # Check for collisions and apply push effect
        if others:
            hits = self.check_collision(others)
            for hit in hits:
                # Calculate push direction (away from center)
                dx = hit.rect.centerx - center_x
                dy = hit.rect.centery - center_y
                
                # Calculate distance
                distance = max(1, (dx**2 + dy**2)**0.5)  # Avoid division by zero
                
                # Normalize direction
                dx /= distance
                dy /= distance
                
                # Apply push force directly to velocity
                hit.vel.x += dx * self.push_force
                hit.vel.y += dy * self.push_force
                
                # Apply damage
                if hasattr(hit, "change_health"):
                    hit.change_health(-self.damage)
        
        # Deactivate when wave reaches max size
        if self.current_radius >= self.max_radius:
            self.active = False

    def draw(self, surface):
        if not self.active:
            return
                
        # Draw a simple circle outline at the current radius
        pygame.draw.circle(
            surface, 
            self.color, 
            (self.player.rect.centerx, self.player.rect.centery), 
            self.current_radius, 
            3  # Thickness of the circle outline
        )