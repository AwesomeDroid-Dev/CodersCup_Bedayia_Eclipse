import sys
import pygame
from Classes.AIPlayer import AIPlayer
from Classes.Axe import Axe
from Classes.AxeWarrior import AxeWarrior
from Classes.BombFighter import BombFighter
from Classes.Boss import Boss
from Classes.Jetboots import Jetboots
from Classes.JetbootsBoss import JetbootsBoss
from Classes.Object import Object
from Classes.PeletLauncher import PelletLauncher
from Classes.Player import Player
import loser_screen
import victory_screen

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

global current_round
current_round = 1

round_scores = [
    100,
    100,
    100
]

def init_game():
    if current_round == 1:
        return init_wave_1()
    elif current_round == 2:
        return init_wave_2()
    elif current_round == 3:
        return init_wave_3()
    else:
        return False

def init_wave_1():
    font = pygame.font.Font(None, 36)
    text = font.render("Wave 1", 1, (255, 255, 255))
    textpos = text.get_rect(centerx=SCREEN_WIDTH / 2, centery=SCREEN_HEIGHT / 2)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill((0, 0, 0))
    screen.blit(text, textpos)
    pygame.display.flip()
    pygame.time.wait(1000)
    
    ground = Object(0, 550, 1200, 50, (255, 255, 255), invisible=True)
    wall1 = Object(0, 0, 1, 600, (255, 255, 255), invisible=True)
    wall2 = Object(1199, 0, 1, 600, (255, 255, 255), invisible=True)
    player = Player(600, 100, 20*3, 21*3, "./Resources/player_spritesheet.png", speed=10)
    player.weapon = PelletLauncher(player)
    player.boots = Jetboots(player)
    player2 = AxeWarrior(100, 100, 20*3, 25*3, player, speed=5)
    return [ground, wall1, wall2, player, player2]

def init_wave_2():
    font = pygame.font.Font(None, 36)
    text = font.render("Wave 2", 1, (255, 255, 255))
    textpos = text.get_rect(centerx=SCREEN_WIDTH / 2, centery=SCREEN_HEIGHT / 2)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill((0, 0, 0))
    screen.blit(text, textpos)
    pygame.display.flip()
    pygame.time.wait(1000)
    
    ground = Object(0, 550, 1200, 50, (255, 255, 255), invisible=True)
    wall1 = Object(0, 0, 1, 600, (255, 255, 255), invisible=True)
    wall2 = Object(1199, 0, 1, 600, (255, 255, 255), invisible=True)
    player = Player(600, 100, 20*3, 21*3, "./Resources/player_spritesheet.png", speed=10)
    player.weapon = PelletLauncher(player)
    player.boots = Jetboots(player)
    player2 = BombFighter(100, 100, 12*3, 21*3, player)
    player2.weapon = PelletLauncher(player2)
    return [ground, wall1, wall2, player, player2]

def init_wave_3():
    font = pygame.font.Font(None, 36)
    text = font.render("BOSS BATTLE", 1, (255, 255, 255))
    textpos = text.get_rect(centerx=SCREEN_WIDTH / 2, centery=SCREEN_HEIGHT / 2)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill((0, 0, 0))
    screen.blit(text, textpos)
    pygame.display.flip()
    pygame.time.wait(1000)
    
    ground = Object(0, 550, 1200, 50, (255, 255, 255), invisible=True)
    wall1 = Object(0, 0, 1, 600, (255, 255, 255), invisible=True)
    wall2 = Object(1199, 0, 1, 600, (255, 255, 255), invisible=True)
    player = Player(600, 100, 20*3, 21*3, "./Resources/player_spritesheet.png", speed=10)
    player.weapon = PelletLauncher(player)
    player.boots = Jetboots(player)
    player2 = Boss(100, 100, player)
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
    enemy_defeated = False
    dropped_item = None  # To track if an item has been dropped
    
    while running:
        screen.fill((0, 0, 0))
        bg = pygame.image.load("Resources/bg_round_1.png").convert_alpha()
        bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(bg, (0, 0))
        
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
            
            # Player 2 controls if still alive
            if player2.health > 0:
                player2.update([obj for obj in objects if obj != player2], screen)
            # If enemy is defeated but item hasn't been dropped yet
            elif not enemy_defeated:
                enemy_defeated = True
                global current_round
                player2.type = "defeated"

                next_round = True
                current_round += 1
                global timer
                timer = pygame.time.get_ticks()
        
            
            # Update and check dropped item if it exists
            if dropped_item and dropped_item in objects:
                dropped_item.update(objects, screen)
                
                # Check if the item has been collected
                if hasattr(dropped_item, "collected") and dropped_item.collected:
                    # Remove item from objects list
                    objects.remove(dropped_item)
                    dropped_item = None
                    # Prepare for next round
                    next_round = True
                    current_round += 1
                    timer = pygame.time.get_ticks()
            
            # Draw all objects
            for obj in objects:
                obj.draw(screen)
                
            # Check for game over
            if player.health <= 0:
                game_over = True
        
        if next_round:
            timeSince = pygame.time.get_ticks() - timer
            font = pygame.font.Font("./Resources/PressStart2P-Regular.ttf", 50)
            text = font.render(f"Next Round in {3 - int(timeSince / 1000)} seconds", True, (255, 255, 255))
            round_scores[current_round - 2] = player.health
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
            if timeSince / 1000 >= 3:
                next_round = False
                enemy_defeated = False
                dropped_item = None
                objects = init_game()
                if objects:
                    player = objects[3]
                    player2 = objects[4]
                    game_over = False
                else:
                    # Example usage
                    action = victory_screen.show(screen, round_scores[0]+round_scores[1]+round_scores[2], {"Round 1": round_scores[0], "Round 2": round_scores[1], "Round 3": round_scores[2]})
                    if action == "home":
                        # Go to home screen
                        running = False
                    elif action == "restart":
                        running = False
                    elif action == "quit":
                        pygame.quit()
                        sys.exit()
        
        if game_over:
            action = loser_screen.show(screen)
            if action == "restart":
                # Reset the game completely
                objects = init_game()
                if objects:
                    player = objects[3]
                    player2 = objects[4]
                    game_over = False
                    enemy_defeated = False
                    dropped_item = None
                else:
                    running = False
            elif action == "quit":
                running = False
        
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()