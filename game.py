import pygame
from Classes.Object import Object
from Classes.Player import Player

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Two Player Battle Game")

clock = pygame.time.Clock()
running = True

ground = Object(0, 500, 800, 100, (255, 255, 255))
wall1 = Object(0, 0, 50, 600, (255, 255, 255))
wall2 = Object(750, 0, 50, 600, (255, 255, 255))
player = Player(600, 100, 12*3, 21*3, (0, 0, 255), speed=10)
player2 = Player(100, 100, 12*3, 21*3, (0, 255, 0), speed=10)

objects = [ground, wall1, wall2, player, player2]

while running:
    screen.fill((0, 0, 0))
    
    events = pygame.event.get()
    keysDown = pygame.key.get_pressed()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    
    # Check for weapon attacks
    for event in events:
        if event.type == pygame.KEYDOWN:
            # Player 1 attack with SLASH key
            if event.key == pygame.K_SLASH:
                player.attack()
            
            # Player 2 attack with E key
            if event.key == pygame.K_e:
                player2.attack()
            
            # Player 1 fly with . key
            if event.key == pygame.K_PERIOD:
                player.boots.activate()
            
            # Player 2 fly with q key
            if event.key == pygame.K_q:
                player2.boots.deactivate()
    
    # Player 1 controls
    player.control('left', keysDown[pygame.K_LEFT])
    player.control('right', keysDown[pygame.K_RIGHT])
    player.control('up', keysDown[pygame.K_UP])
    player.control('down', keysDown[pygame.K_DOWN])
    player.update([obj for obj in objects if obj != player], screen)
    
    # Player 2 controls
    player2.control('left', keysDown[pygame.K_a])
    player2.control('right', keysDown[pygame.K_d])
    player2.control('up', keysDown[pygame.K_w])
    player2.control('down', keysDown[pygame.K_s])
    player2.update([obj for obj in objects if obj != player2], screen)
    
    # Draw objects
    ground.draw(screen)
    wall1.draw(screen)
    wall2.draw(screen)
    #player.draw(screen)
    #player2.draw(screen)
        
    pygame.display.update()
    clock.tick(60)

pygame.quit()