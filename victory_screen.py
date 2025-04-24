import pygame
import math
import os
import random  # Added for proper random number generation

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.alpha = 0  # For fade in animation
        
        # Load sound effect if available
        try:
            self.hover_sound = pygame.mixer.Sound("./Resources/hover.wav")
            self.click_sound = pygame.mixer.Sound("./Resources/click.wav")
        except:
            self.hover_sound = None
            self.click_sound = None
        
        self._was_hovered = False  # Track previous hover state

    def draw(self, screen, font):
        current_color = self.hover_color if self.is_hovered else self.color
        # Apply alpha for fade in
        button_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(button_surface, (*current_color, self.alpha), button_surface.get_rect(), border_radius=12)
        
        text_surface = font.render(self.text, True, (255, 255, 255, self.alpha))
        text_rect = text_surface.get_rect(center=self.rect.center)
        
        screen.blit(button_surface, self.rect)
        screen.blit(text_surface, text_rect)
        
        # Play hover sound when first hovering
        if self.hover_sound and self.is_hovered and not self._was_hovered:
            self.hover_sound.play()
        self._was_hovered = self.is_hovered

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                if self.click_sound:
                    self.click_sound.play()
                return True
        return False

class ScoreDisplay:
    def __init__(self, x, y, width, height, scores=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.scores = scores if scores else {"Current": 0}
        self.alpha = 0  # For fade in animation
        
    def draw(self, screen, font):
        # Draw background panel with alpha
        panel_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surface, (30, 30, 30, self.alpha), panel_surface.get_rect(), border_radius=12)
        screen.blit(panel_surface, self.rect)
        
        # Draw header
        header = font.render("SCORES", True, (255, 215, 0, self.alpha))
        header_rect = header.get_rect(midtop=(self.rect.centerx, self.rect.y + 20))
        screen.blit(header, header_rect)
        
        # Draw scores
        y_offset = header_rect.bottom + 20
        for label, score in self.scores.items():
            score_text = font.render(f"{label}: {score}", True, (255, 255, 255, self.alpha))
            score_rect = score_text.get_rect(midtop=(self.rect.centerx, y_offset))
            screen.blit(score_text, score_rect)
            y_offset += 30

class VictoryScreen:
    def __init__(self, screen, score=0, high_scores=None):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.animation_start = pygame.time.get_ticks()
        self.fade_in_duration = 1000  # 1 second fade in
        self.title_float_duration = 3000  # 3 second float cycle
        self.particles = []  # For celebration particles
        
        # Prepare scores
        self.current_score = score
        self.high_scores = high_scores if high_scores else {"High Score": 1000}
        
        # Create combined scores dict
        scores_dict = {"Current Score": score}
        scores_dict.update(self.high_scores)
        
        # Create score display
        score_panel_width, score_panel_height = 300, 200
        self.score_display = ScoreDisplay(
            self.width//2 - score_panel_width//2,
            self.height * 0.4,
            score_panel_width,
            score_panel_height,
            scores_dict
        )
        
        # Create buttons
        button_width, button_height = 200, 50
        button_y = self.height * 0.75
        spacing = 30
        
        self.home_button = Button(
            self.width//2 - button_width - spacing,
            button_y,
            button_width,
            button_height,
            "Go to Home",
            (0, 100, 0),
            (0, 150, 0)
        )
        
        self.play_again_button = Button(
            self.width//2 + spacing,
            button_y,
            button_width,
            button_height,
            "Play Again",
            (0, 100, 100),
            (0, 150, 150)
        )
        
        # Load fonts
        self.title_font = pygame.font.Font("./Resources/PressStart2P-Regular.ttf", 50)
        self.button_font = pygame.font.Font("./Resources/PressStart2P-Regular.ttf", 20)
        self.score_font = pygame.font.Font("./Resources/PressStart2P-Regular.ttf", 18)
        
        # Initialize celebratory particles
        self._create_particles()
        
        # Try to load victory sound
        try:
            self.victory_sound = pygame.mixer.Sound("./Resources/victory.wav")
            self.victory_sound.play()
        except:
            self.victory_sound = None
    
    def _create_particles(self, count=50):
        """Create celebratory particles"""
        for _ in range(count):
            x = self.width / 2
            y = self.height / 3
            
            # Random velocities (fixed Vector2 issue)
            vel_x = (random.random() * 2 - 1) * 5  # Random x velocity between -5 and 5
            vel_y = (random.random() * -1 - 0.5) * 8  # Random y velocity (upward)
            
            # Random colors
            color = (
                random.randint(150, 255),  # Random R
                random.randint(150, 255),  # Random G
                random.randint(200, 255)   # Random B (biased toward brighter)
            )
            
            size = random.random() * 10 + 5  # Size between 5 and 15
            lifetime = random.random() * 2 + 1  # 1-3 seconds
            
            self.particles.append({
                "pos": pygame.math.Vector2(x, y),
                "vel": pygame.math.Vector2(vel_x, vel_y),
                "color": color,
                "size": size,
                "lifetime": lifetime,
                "born": pygame.time.get_ticks() / 1000.0
            })

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            if self.home_button.handle_event(event):
                return "home"
            if self.play_again_button.handle_event(event):
                return "restart"
            
            # Handle ESC key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "quit"
        return None

    def update_animations(self):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.animation_start
        
        # Fade in animation (0 to 255 over fade_in_duration)
        alpha = min(255, (elapsed / self.fade_in_duration) * 255)
        self.home_button.alpha = alpha
        self.play_again_button.alpha = alpha
        self.score_display.alpha = alpha
        
        # Floating title animation
        float_progress = (elapsed % self.title_float_duration) / self.title_float_duration
        self.title_offset = math.sin(float_progress * 2 * math.pi) * 15
        
        # Update particles
        current_time_sec = current_time / 1000.0
        for particle in self.particles[:]:
            # Apply gravity
            particle["vel"].y += 0.1
            # Move particle
            particle["pos"] += particle["vel"]
            # Check if particle is dead
            age = current_time_sec - particle["born"]
            if age > particle["lifetime"] or particle["pos"].y > self.height:
                self.particles.remove(particle)
        
        # Add new particles occasionally
        if elapsed % 500 < 20:  # Every ~0.5 seconds
            self._create_particles(count=5)
            
        return alpha

    def draw(self):
        # Create overlay with fade
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        alpha = self.update_animations()
        overlay.fill((0, 20, 40, min(200, int(alpha))))
        self.screen.blit(overlay, (0, 0))
        
        # Draw particles
        for particle in self.particles:
            age_ratio = 1 - (pygame.time.get_ticks() / 1000.0 - particle["born"]) / particle["lifetime"]
            size = particle["size"] * age_ratio
            particle_color = (*particle["color"], int(255 * age_ratio))
            pygame.draw.circle(
                self.screen,
                particle_color,
                (int(particle["pos"].x), int(particle["pos"].y)),
                int(size)
            )
        
        # Draw floating title with golden color
        title_text = self.title_font.render("VICTORY!", True, (255, 215, 0))
        title_rect = title_text.get_rect(center=(self.width // 2, self.height // 5 + self.title_offset))
        self.screen.blit(title_text, title_rect)
        
        # Draw celebratory message
        subtitle_text = self.button_font.render("Congratulations!", True, (200, 255, 200))
        subtitle_rect = subtitle_text.get_rect(center=(self.width // 2, title_rect.bottom + 20))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Draw score display
        self.score_display.draw(self.screen, self.score_font)
        
        # Draw buttons
        self.home_button.draw(self.screen, self.button_font)
        self.play_again_button.draw(self.screen, self.button_font)

def show(screen, score=0, high_scores=None):
    victory_screen = VictoryScreen(screen, score, high_scores)
    clock = pygame.time.Clock()
    
    while True:
        action = victory_screen.handle_events()
        if action in ["home", "restart", "quit"]:
            return action
            
        victory_screen.draw()
        pygame.display.flip()
        clock.tick(60)