import pygame
from Classes.Collectable import Collectable
from Classes.Jetboots import Jetboots

class JetbootsItem(Collectable):
    def __init__(self, x, y, width, height, image_path=None, color=(255, 255, 0), item_type="health", value=10):
        super().__init__(x, y, width, height, image_path, color, item_type, value)

    def give(self, player):
        pygame.mixer.Sound.play(self.collect_sound)
        player.boots = Jetboots(player)