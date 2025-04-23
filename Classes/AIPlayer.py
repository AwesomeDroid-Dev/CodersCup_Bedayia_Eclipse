from Classes.Player import Player

class AIPlayer(Player):
    def __init__(self, x, y, width, height, player):
        super().__init__(x, y, width, height, "./Resources/Solid_red.png", speed=9)
        self.boots = None
        self.player = player
        self.max_reaction = 60
        self.reaction = 60

        self.type = "AIPlayer"
    
    def update(self, others, screen=None):
        self.reaction -= 1
        if self.reaction == 0:
            if self.pos.distance_to(self.player.pos) < 100:
                self.attack_player(self.player)
            else:
                self.move_towards_player(self.player)
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
    
    def attack_player(self, player):
        # Reset all controls
        self.reset_controls()
        
        self.control("attack", True)
    
    
    def reset_controls(self):
        self.control("right", False)
        self.control("left", False)
        self.control("down", False)
        self.control("up", False)
        self.control("boots", False)