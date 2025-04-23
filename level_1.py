import pygame
from Classes.AIPlayer import AIPlayer
from Classes.Axe import Axe
from Classes.AxeWarrior import AxeWarrior
from Classes.BombFighter import BombFighter
from Classes.Boss import Boss
from Classes.Object import Object
from Classes.PeletLauncher import PelletLauncher
from Classes.Player import Player
import loser_screen

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

def init_game():
    return init_wave_2()

def init_wave_1():
    ground = Object(0, 550, 1200, 50, (255, 255, 255))
    wall1 = Object(0, 0, 50, 600, (255, 255, 255))
    wall2 = Object(1150, 0, 50, 600, (255, 255, 255))
    player = Player(600, 100, 12*3, 21*3, "./Resources/player_spritesheet.png", speed=10)
    player.weapon = Axe(10, -10, 50, 50, player)
    player2 = AxeWarrior(100, 100, 12*3, 21*3, player)
    return [ground, wall1, wall2, player, player2]

def init_wave_2():
    ground = Object(0, 550, 1200, 50, (255, 255, 255))
    wall1 = Object(0, 0, 50, 600, (255, 255, 255))
    wall2 = Object(1150, 0, 50, 600, (255, 255, 255))
    player = Player(600, 100, 12*3, 21*3, "./Resources/player_spritesheet.png", speed=10)
    player2 = BombFighter(100, 100, 12*3, 21*3, player)
    player2.weapon = PelletLauncher(player2)
    return [ground, wall1, wall2, player, player2]

def init_wave_3():
    ground = Object(0, 550, 1200, 50, (255, 255, 255))
    wall1 = Object(0, 0, 50, 600, (255, 255, 255))
    wall2 = Object(1150, 0, 50, 600, (255, 255, 255))
    player = Player(600, 100, 12*3, 21*3, "./Resources/player_spritesheet.png", speed=10)
    player2 = AIPlayer(100, 100, 12*3, 21*3, player)
    return [ground, wall1, wall2, player, player2]

def init_wave_4():
    ground = Object(0, 550, 1200, 50, (255, 255, 255))
    wall1 = Object(0, 0, 50, 600, (255, 255, 255))
    wall2 = Object(1150, 0, 50, 600, (255, 255, 255))
    player = Player(600, 100, 12*3, 21*3, "./Resources/player_spritesheet.png", speed=10)
    player2 = AIPlayer(100, 100, 12*3, 21*3, player)
    return [ground, wall1, wall2, player, player2]

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Two Player Battle Game")
    clock = pygame.time.Clock()
    
    objects = init_game()
    player = objects[3]  # Player is the 4th object
    player2 = objects[4]  # AI Player is the 5th object
    
    running = True
    game_over = False
    next_round = False
    
    while running:
        screen.fill((0, 0, 0))
        
        events = pygame.event.get()
        keysDown = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        
        if not game_over and not next_round:
            # Player 1 controls
            player.control('left', keysDown[pygame.K_LEFT])
            player.control('right', keysDown[pygame.K_RIGHT])
            player.control('up', keysDown[pygame.K_UP])
            player.control('down', keysDown[pygame.K_DOWN])
            player.control('attack', keysDown[pygame.K_SLASH])
            player.control('boots', keysDown[pygame.K_PERIOD])
            player.update([obj for obj in objects if obj != player], screen)
            
            # Player 2 controls
            player2.update([obj for obj in objects if obj != player2], screen)
            
            # Draw all objects
            for obj in objects:
                obj.draw(screen)
                
            # Check for game over
            if player.health <= 0:
                game_over = True
            if player2.health <= 0:
                next_round = True
                global timer
                timer = pygame.time.get_ticks()
                
        
        if next_round:
            timeSince = pygame.time.get_ticks() - timer
            font = pygame.font.Font("./Resources/PressStart2P-Regular.ttf", 50)
            text = font.render(f"Next Round in {3 - int(timeSince / 1000)} seconds", True, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
            if timeSince / 1000 >= 3:
                next_round = False
                objects = init_game()
                player = objects[3]
                player2 = objects[4]
                game_over = False
        
        if game_over:
            action = loser_screen.show(screen)
            if action == "restart":
                # Reset the game completely
                objects = init_game()
                player = objects[3]
                player2 = objects[4]
                game_over = False
            elif action == "quit":
                running = False
        
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()