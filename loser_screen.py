import pygame

def show(screen):
    overlay = pygame.Surface((screen.get_width(), screen.get_height()))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(150)
    screen.blit(overlay, (0, 0))
    
    font = pygame.font.Font("./Resources/PressStart2P-Regular.ttf", 50)
    text = font.render("You lost! You're a loser!", True, (255, 0, 0))
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(text, text_rect)