import pygame
from Classes.AIPlayer import AIPlayer
from Classes.AxeWarrior import AxeWarrior
from Classes.Boss import Boss
from Classes.Object import Object
from Classes.Player import Player

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Two Player Battle Game")

clock = pygame.time.Clock()
running = True


ground = Object(0, 550, 1200, 50, (255, 255, 255))
wall1 = Object(0, 0, 50, 600, (255, 255, 255))
wall2 = Object(1150, 0, 50, 600, (255, 255, 255))
player = Player(600, 100, 12*3, 21*3, "./Resources/player_spritesheet.png", speed=10)
#boss = Boss(100, 100, player)
player2 = AIPlayer(100, 100, 12*3, 21*3, player)
#player2 = Player(100, 100, 12*3, 21*3, (0, 255, 0), speed=10)
#player2 = AxeWarrior(100, 100, 12*3, 21*3, (0, 255, 0), player, speed=10)

objects = [ground, wall1, wall2, player, player2]

while running:
    screen.fill((0, 0, 0))
    
    events = pygame.event.get()
    keysDown = pygame.key.get_pressed()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    
    
    # Player 1 controls
    player.control('left', keysDown[pygame.K_LEFT])
    player.control('right', keysDown[pygame.K_RIGHT])
    player.control('up', keysDown[pygame.K_UP])
    player.control('down', keysDown[pygame.K_DOWN])
    player.control('attack', keysDown[pygame.K_SLASH])
    player.control('boots', keysDown[pygame.K_PERIOD])
    player.update([obj for obj in objects if obj != player], screen)
    #boss.update([obj for obj in objects if obj != boss], screen)
    
    # Player 2 controls
    #player2.control('left', keysDown[pygame.K_a])
    #player2.control('right', keysDown[pygame.K_d])
    #player2.control('up', keysDown[pygame.K_w])
    #player2.control('down', keysDown[pygame.K_s])
    player2.update([obj for obj in objects if obj != player2], screen)
    
    # Draw objects
    ground.draw(screen)
    wall1.draw(screen)
    wall2.draw(screen)
        
    pygame.display.update()
    clock.tick(60)

pygame.quit()