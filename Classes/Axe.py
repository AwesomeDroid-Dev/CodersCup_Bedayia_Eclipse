from Classes.PlayerTool import PlayerTool
from Classes.Weapon import Weapon
import pygame
import math

class Axe(PlayerTool):
    def __init__(self, xOffset, yOffset, width, height, player):
        super().__init__(xOffset, yOffset, width, height, player)
        self.swing_angle = 0
        self.is_swinging = False
        self.swing_duration = 10  # Frames for full swing
        self.swing_progress = 0
        self.cooldown = 0
        self.shockwave = None
        
        # Load axe image
        try:
            self.base_image = pygame.image.load("./Resources/Axe.png").convert_alpha()
            self.base_image = pygame.transform.scale(self.base_image, (width, height))
        except Exception as e:
            print(f"Error loading axe image: {e}")
            self.base_image = pygame.Surface((width, height), pygame.SRCALPHA)
            pygame.draw.rect(self.base_image, (100, 100, 100), (0, 0, width, height))
        
        self.image = self.base_image
        self.rect = self.image.get_rect()
        self.type = "Axe"

    def rotate_around_pivot(self, image, angle, pivot, original_rect):
        """Rotate image around specified pivot point"""
        # Create rotated image
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rect = rotated_image.get_rect()
        
        # Calculate offset from pivot to rect center
        pivot_offset_x = original_rect.center[0] - pivot[0]
        pivot_offset_y = original_rect.center[1] - pivot[1]
        
        # Calculate new position based on rotation
        rad_angle = math.radians(angle)
        new_x = pivot_offset_x * math.cos(rad_angle) - pivot_offset_y * math.sin(rad_angle)
        new_y = pivot_offset_x * math.sin(rad_angle) + pivot_offset_y * math.cos(rad_angle)
        
        # Position the rotated rect with pivot point at the same position
        rotated_rect.center = (pivot[0] + new_x, pivot[1] + new_y)
        
        return rotated_image, rotated_rect

    def draw(self, screen):
        if self.is_swinging:
            # Calculate rotation progress
            swing_percent = self.swing_progress / self.swing_duration
            angle = -90 * swing_percent  # Negative for clockwise rotation
            
            # Pivot at bottom center (axe handle)
            original_rect = self.base_image.get_rect(topleft=self.rect.topleft)
            pivot = pygame.Vector2(original_rect.centerx, original_rect.bottom)
            
            rotated_image, rotated_rect = self.rotate_around_pivot(
                self.base_image, angle, pivot, original_rect
            )
            
            if self.player.direction == "left":
                rotated_image = pygame.transform.flip(rotated_image, True, False)
                # Adjust position for flipped image
                original_width = rotated_rect.width
                rotated_rect.x = rotated_rect.x + (2 * (pivot.x - rotated_rect.centerx))
            
            screen.blit(rotated_image, rotated_rect)
        else:
            if self.player.direction == "right":
                screen.blit(self.image, self.rect)
            else:
                flipped = pygame.transform.flip(self.image, True, False)
                screen.blit(flipped, self.rect)
        
        if self.shockwave and self.shockwave.active:
            self.shockwave.draw(screen)

    def update(self, others):
        if self.cooldown > 0:
            self.cooldown -= 1
            
        if self.is_swinging:
            self.swing_progress += 1
            if self.swing_progress >= self.swing_duration:
                self.is_swinging = False
                self.swing_progress = 0
                self.cooldown = 30  # Cooldown after swing
                
                # Create shockwave at player's feet
                shockwave_pos = pygame.Vector2(
                    self.player.rect.centerx,
                    self.player.rect.bottom - 10
                )
                
                self.shockwave = Shockwave(
                    self.player, 
                    shockwave_pos,
                    others,
                    radius=150,
                    damage=30
                )
        
        # Update the shockwave if it exists
        if self.shockwave:
            self.shockwave.update()
            
            # Only remove shockwave reference when it's no longer active
            if not self.shockwave.active:
                self.shockwave = None
            
        self.followPlayer(self.player)

    def activate(self):
        if self.cooldown > 0 or self.is_swinging:
            return
        
        self.is_swinging = True
        self.swing_progress = 0


class Shockwave(Weapon):
    def __init__(self, owner, pos, others, radius=20, damage=15):
        super().__init__(owner, radius*2, radius*2, (255, 255, 0, 128), damage)
        self.pos = pygame.Vector2(pos)
        self.radius = radius
        self.active = True
        self.timer = 10
        self.others = others
        # Create a proper rect centered on the position
        self.rect = pygame.Rect(
            pos.x - radius, 
            pos.y - radius, 
            radius*2, 
            radius*2
        )
        # Reset has_hit as it's already defined in the Weapon parent class
        self.has_hit = []

    def update(self):
        if not self.active:
            return
            
        if self.timer <= 0:
            self.active = False
            return
            
        # Update the rect position each frame
        self.rect.x = self.pos.x - self.radius
        self.rect.y = self.pos.y - self.radius
        
        # Use the parent class's collision detection
        hits = self.check_collision(self.others)
        for hit in hits:
            if hasattr(hit, 'change_health') and hit != self.player:  # Don't damage self
                # Calculate damage based on distance
                dist = math.hypot(hit.rect.centerx - self.pos.x, hit.rect.centery - self.pos.y)
                damage_factor = 1 - (dist / self.radius) if dist < self.radius else 0
                actual_damage = int(self.damage * damage_factor)
                if actual_damage > 0:
                    hit.change_health(-actual_damage)
        
        self.timer -= 1

    def draw(self, screen):
        if not self.active:
            return
            
        # Create expanding effect as timer counts down
        current_radius = self.radius * (1 - self.timer / 10)
        alpha = int(200 * (self.timer / 10))
        
        # Create a transparent surface for the shockwave
        surface = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(
            surface, 
            (255, 200, 0, alpha), 
            (self.radius, self.radius), 
            current_radius
        )
        
        # Add a bright inner circle for better visibility
        inner_radius = max(5, current_radius * 0.6)
        pygame.draw.circle(
            surface,
            (255, 255, 100, alpha),
            (self.radius, self.radius),
            inner_radius
        )
        
        # Draw the shockwave
        screen.blit(surface, (self.pos.x - self.radius, self.pos.y - self.radius))