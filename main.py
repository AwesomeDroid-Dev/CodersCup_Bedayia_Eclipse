import pygame
from menus import create_main_menu

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Menu Test")

main_menu = create_main_menu(screen)

clock = pygame.time.Clock()
running = True

while running:
    screen.fill((0, 0, 0))
    
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    if main_menu.is_enabled():
        main_menu.update(events)
        main_menu.draw(screen)
    
    pygame.display.update()
    clock.tick(60)