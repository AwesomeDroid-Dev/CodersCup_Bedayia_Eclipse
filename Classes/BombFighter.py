from Classes.Player import Player
from pygame.math import Vector2

class BombFighter(Player):
    def __init__(self, x, y, width, height, player):
        super().__init__(x, y, width, height, "./Resources/bombfighter.png", speed=9)
        self.boots = None
        self.player = player
        self.max_reaction = 15
        self.reaction = 15
        self.prevPos = Vector2(x, y)
        self.goal = "attack" # "attack" or "run" or "move" or "panick"

        self.type = "AIPlayer"
    
    def update(self, others, screen=None):
        self.reaction -= 1
        if self.reaction == 0:
            self.pick_goal()
            self.prevPos = self.pos
            if self.goal == "run":
                self.move_away_from_player(self.player)
            elif self.goal == "attack":
                self.attack_player(self.player)
            elif self.goal == "move":
                self.move_towards_player(self.player)
            else:
                self.move_to_center()
            self.reaction = self.max_reaction
        
        return super().update(others, screen)
    
    def draw(self, screen):
        return super().draw(screen)
    
    def move_towards_player(self, player):
        # Reset all controls
        self.reset_controls()
        
        if player.pos.x < self.pos.x:
            self.control("left", True)
        else:
            self.control("right", True)
    
    def move_away_from_player(self, player):
        # Reset all controls
        self.reset_controls()
        
        if player.pos.x > self.pos.x:
            self.control("right", True)
        else:
            self.control("left", True)
        self.control("attack", True)
    
    def attack_player(self, player):
        # Reset all controls
        self.reset_controls()
        
        if player.pos.x < self.pos.x:
            self.control("right", True)
        else:
            self.control("left", True)
        self.control("attack", True)
    
    def move_to_center(self):
        # Reset all controls
        self.reset_controls()
        
        if self.pos.x < 400:
            self.control("right", True)
        else:
            self.control("left", True)
    
    
    def reset_controls(self):
        self.control("right", False)
        self.control("left", False)
        self.control("down", False)
        self.control("up", False)
        self.control("attack", False)
        self.control("boots", False)
    
    def pick_goal(self):
        if self.goal == "run" and self.prevPos == self.pos:
            self.goal = "panick"
        if self.pos.distance_to(self.player.pos) < 200:
            self.goal = "run"
        elif self.pos.distance_to(self.player.pos) < 400:
            self.goal = "attack"
        else:
            self.goal = "move"
        pass