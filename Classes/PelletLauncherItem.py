import pygame
from Classes.Collectable import Collectable
from Classes.PeletLauncher import PelletLauncher

class PelletLauncherItem(Collectable):
    def __init__(self, x, y, width, height, image_path="./Resources/pelletlauncher.png", color=(255, 255, 0), item_type="health", value=10):
        super().__init__(x, y, width, height, image_path, color, item_type, value)

    def give(self, player):
        pygame.mixer.Sound.play(self.collect_sound)
        player.boots = PelletLauncher(player)