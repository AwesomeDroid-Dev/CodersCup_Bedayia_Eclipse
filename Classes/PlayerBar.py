import pygame
import math
import random
from Classes.PlayerTool import PlayerTool

class PlayerBar(PlayerTool):
    def __init__(self, x, y, width, height, max_value, value, color, player):
        super().__init__(-width, 10, width, height, player)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_health = max_value
        self.health = max(0, min(value, max_value))
        self.displayed_health = self.health  # For smooth animation
        self.color = color
        self.player = player
        
        # Animation properties
        self.damage_flash_start = 0
        self.damage_flash_duration = 200  # milliseconds
        self.heal_particles = []
        self.damage_particles = []
        self.particle_lifetime = 1000  # milliseconds
        
        # Visual properties
        self.border_radius = 4
        self.border_width = 2
        self.gradient_colors = self._create_gradient(color)
        self.background_color = (40, 40, 40)
        self.border_color = (200, 200, 200)
        
        # Critical health threshold and color
        self.critical_health = 0.2  # 20% of max health
        self.critical_color = (255, 0, 0)
        self.last_critical_flash = 0
        self.critical_flash_rate = 500  # milliseconds
        
        self.rect = pygame.Rect(player.pos.x + x, player.pos.y + y, self.width, self.height)
        self.type = "PlayerBar"
        
        # Health change animation
        self.health_change_time = 0
        self.health_change_duration = 300  # milliseconds
        self.previous_health = self.health
        
        # Create heart icon
        self._create_heart_icon()

    def _create_heart_icon(self):
        size = self.height + 4 
        self.heart_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Draw heart shape
        color = (255, 0, 0)
        center_x = size // 2
        center_y = size // 2
        
        # Draw the two circles for the top of the heart
        radius = size // 4
        pygame.draw.circle(self.heart_surface, color, (center_x - radius + 1, center_y - 1), radius)
        pygame.draw.circle(self.heart_surface, color, (center_x + radius - 1, center_y - 1), radius)
        
        # Draw the triangle for the bottom of the heart
        points = [
            (center_x - size//2 + 2, center_y),
            (center_x, center_y + size//2 - 2),
            (center_x + size//2 - 2, center_y)
        ]
        pygame.draw.polygon(self.heart_surface, color, points)

    def _create_gradient(self, base_color):
        # Create a gradient from darker to lighter version of the base color
        r, g, b = base_color
        gradient = []
        for i in range(3):
            # Darken for bottom
            dark_factor = 0.7 - (i * 0.1)
            # Lighten for top
            light_factor = 1.0 + (i * 0.1)
            
            dark_color = (
                max(0, min(255, int(r * dark_factor))),
                max(0, min(255, int(g * dark_factor))),
                max(0, min(255, int(b * dark_factor)))
            )
            light_color = (
                max(0, min(255, int(r * light_factor))),
                max(0, min(255, int(g * light_factor))),
                max(0, min(255, int(b * light_factor)))
            )
            gradient.append((dark_color, light_color))
        return gradient

    def _create_particles(self, amount, is_heal=True):
        current_time = pygame.time.get_ticks()
        for _ in range(amount):
            particle = {
                'x': self.rect.x + self.width * (self.health / self.max_health),
                'y': self.rect.centery,
                'dx': (random.random() - 0.5) * 3,
                'dy': -random.random() * 2 - 1,
                'size': random.randint(2, 4),
                'creation_time': current_time,
                'color': (100, 255, 100) if is_heal else (255, 100, 100)
            }
            if is_heal:
                self.heal_particles.append(particle)
            else:
                self.damage_particles.append(particle)

    def _update_particles(self, particles, surface):
        current_time = pygame.time.get_ticks()
        remaining_particles = []
        
        for particle in particles:
            age = current_time - particle['creation_time']
            if age < self.particle_lifetime:
                # Update position
                particle['x'] += particle['dx']
                particle['y'] += particle['dy']
                particle['dy'] += 0.1  # Gravity
                
                # Calculate fade based on age
                alpha = 255 * (1 - (age / self.particle_lifetime))
                color = (*particle['color'], int(alpha))
                
                # Draw particle
                pygame.draw.circle(
                    surface,
                    color,
                    (int(particle['x']), int(particle['y'])),
                    particle['size']
                )
                remaining_particles.append(particle)
        
        return remaining_particles

    def draw(self, surface):
        current_time = pygame.time.get_ticks()
        
        # Calculate position relative to the player
        current_x = self.player.pos.x + self.x
        current_y = self.player.pos.y + self.y
        
        # Update rect position
        self.rect.x = current_x
        self.rect.y = current_y
        
        # Draw heart icon
        heart_x = current_x - self.heart_surface.get_width() - 5  # 5 pixels gap
        heart_y = current_y - 2  # Center vertically
        surface.blit(self.heart_surface, (heart_x, heart_y))
        
        # Animate health changes
        if self.displayed_health != self.health:
            progress = min(1, (current_time - self.health_change_time) / self.health_change_duration)
            self.displayed_health = self.previous_health + (self.health - self.previous_health) * progress
            if progress == 1:
                self.displayed_health = self.health
        
        # Draw background with semi-transparency
        bg_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surface, (*self.background_color, 200), bg_surface.get_rect(), border_radius=self.border_radius)
        surface.blit(bg_surface, self.rect)
        
        # Calculate current health width
        health_ratio = self.displayed_health / self.max_health
        current_width = int(self.width * health_ratio)
        
        if current_width > 0:
            health_rect = pygame.Rect(current_x, current_y, current_width, self.height)
            
            # Draw health bar with gradient
            bar_height = self.height // len(self.gradient_colors)
            for i, gradient_pair in enumerate(self.gradient_colors):
                dark_color, light_color = gradient_pair
                section_rect = pygame.Rect(
                    current_x,
                    current_y + (i * bar_height),
                    current_width,
                    bar_height
                )
                
                # Create gradient effect
                for line in range(bar_height):
                    progress = line / bar_height
                    current_color = (
                        int(dark_color[0] + (light_color[0] - dark_color[0]) * progress),
                        int(dark_color[1] + (light_color[1] - dark_color[1]) * progress),
                        int(dark_color[2] + (light_color[2] - dark_color[2]) * progress)
                    )
                    pygame.draw.line(
                        surface,
                        current_color,
                        (section_rect.left, section_rect.top + line),
                        (section_rect.right, section_rect.top + line)
                    )
            
            # Critical health effect
            if self.displayed_health / self.max_health <= self.critical_health:
                if current_time - self.last_critical_flash >= self.critical_flash_rate:
                    self.last_critical_flash = current_time
                    flash_alpha = abs(math.sin(current_time / 200)) * 128
                    flash_surface = pygame.Surface((current_width, self.height), pygame.SRCALPHA)
                    flash_surface.fill((*self.critical_color, int(flash_alpha)))
                    surface.blit(flash_surface, health_rect)
        
        # Draw border
        pygame.draw.rect(surface, self.border_color, self.rect, self.border_width, border_radius=self.border_radius)
        
        # Update and draw particles
        self.heal_particles = self._update_particles(self.heal_particles, surface)
        self.damage_particles = self._update_particles(self.damage_particles, surface)
        
        # Draw health text with outline effect
        font = pygame.font.Font(None, int(self.height * 1.2))  # Increased font size
        health_text = f"{int(self.displayed_health)}/{self.max_health}"
        
        # Function to create outlined text
        def draw_outlined_text(text, font, pos, color, outline_color):
            # Create the outline by drawing the text multiple times with offsets
            outline_positions = [(-2, -2), (-2, 2), (2, -2), (2, 2)]  # Increased outline thickness
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect(center=pos)
            
            # Draw outline
            for dx, dy in outline_positions:
                outline_rect = text_rect.copy()
                outline_rect.x += dx
                outline_rect.y += dy
                outline_text = font.render(text, True, outline_color)
                surface.blit(outline_text, outline_rect)
            
            # Draw main text
            surface.blit(text_surface, text_rect)
        
        # Draw the health text with outline
        text_pos = (self.rect.centerx, self.rect.centery)
        draw_outlined_text(health_text, font, text_pos, (255, 255, 255), (0, 0, 0))

    def update(self, value):
        # Store previous health for animation
        self.previous_health = self.displayed_health
        old_health = self.health
        
        # Update health/value ensuring it stays within bounds
        self.health = max(0, min(value, self.max_health))
        self.health_change_time = pygame.time.get_ticks()
        
        # Create particles based on health change
        if self.health > old_health:
            self._create_particles(int((self.health - old_health) / 5), True)  # Heal particles
        elif self.health < old_health:
            self._create_particles(int((old_health - self.health) / 5), False)  # Damage particles