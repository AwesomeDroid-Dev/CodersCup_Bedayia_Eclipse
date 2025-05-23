import pygame
from pygame.math import Vector2

class PlayerTool(pygame.sprite.Sprite):
    def __init__(self, xOffset, yOffset, width, height, player):
        super().__init__()
        self.width = width
        self.height = height
        self.offset = Vector2(xOffset, yOffset)
        self.pos = Vector2(0, 0)
        self.rect = pygame.Rect(player.pos.x+self.offset.x, player.pos.y+self.offset.y, self.width, self.height)
        self.player = player

        self.followPlayer(player)

    def followPlayer(self, player):
        if player.direction == "right":
            self.pos.x = player.pos.x + player.width + self.offset.x
        else:
            self.pos.x = player.pos.x - self.width - self.offset.x

        self.pos.y = player.pos.y + self.offset.y
        self.rect.topleft = (self.pos.x, self.pos.y)