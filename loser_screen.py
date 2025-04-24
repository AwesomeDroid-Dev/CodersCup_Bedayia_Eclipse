import pygame
import math
import os

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

class GameOverScreen:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.animation_start = pygame.time.get_ticks()
        self.fade_in_duration = 1000  # 1 second fade in
        self.title_bounce_duration = 2000  # 2 second bounce cycle
        
        # Create buttons
        button_width, button_height = 200, 50
        button_y = self.height * 0.6
        spacing = 30
        
        self.restart_button = Button(
            self.width//2 - button_width - spacing,
            button_y,
            button_width,
            button_height,
            "Play Again",
            (45, 45, 45),
            (75, 75, 75)
        )
        
        self.quit_button = Button(
            self.width//2 + spacing,
            button_y,
            button_width,
            button_height,
            "Quit Game",
            (45, 45, 45),
            (75, 75, 75)
        )
        
        # Load font
        self.title_font = pygame.font.Font("./Resources/PressStart2P-Regular.ttf", 50)
        self.button_font = pygame.font.Font("./Resources/PressStart2P-Regular.ttf", 20)
        
        # Try to load game over sound
        try:
            self.game_over_sound = pygame.mixer.Sound("./Resources/game_over.wav")
            self.game_over_sound.play()
        except:
            self.game_over_sound = None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if self.restart_button.handle_event(event):
                return "restart"
            if self.quit_button.handle_event(event):
                return "quit"
            
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
        self.restart_button.alpha = alpha
        self.quit_button.alpha = alpha
        
        # Bouncing title animation
        bounce_progress = (elapsed % self.title_bounce_duration) / self.title_bounce_duration
        self.title_offset = math.sin(bounce_progress * 2 * math.pi) * 10
        
        return alpha

    def draw(self):
        # Create overlay with fade
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        alpha = self.update_animations()
        overlay.fill((0, 0, 0, min(150, alpha)))
        self.screen.blit(overlay, (0, 0))
        
        # Draw bouncing title
        title_text = self.title_font.render("GAME OVER!", True, (255, 0, 0))
        title_rect = title_text.get_rect(center=(self.width // 2, self.height // 3 + self.title_offset))
        self.screen.blit(title_text, title_rect)
        
        # Draw subtitle
        subtitle_text = self.button_font.render("Press ESC to quit or choose an option", True, (200, 200, 200))
        subtitle_rect = subtitle_text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Draw buttons
        self.restart_button.draw(self.screen, self.button_font)
        self.quit_button.draw(self.screen, self.button_font)

def show(screen):
    game_over = GameOverScreen(screen)
    clock = pygame.time.Clock()
    
    while True:  # Changed from game_over.running
        action = game_over.handle_events()
        if action in ["restart", "quit"]:
            return action
            
        game_over.draw()
        pygame.display.flip()
        clock.tick(60)