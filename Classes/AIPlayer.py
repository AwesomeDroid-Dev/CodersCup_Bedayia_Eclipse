import pygame
import random
from pygame.math import Vector2
from Classes.Player import Player

class AIPlayer(Player):
    def __init__(self, x, y, width, height, color, speed, target=None, difficulty="medium"):
        super().__init__(x, y, width, height, color, speed)
        self.target = target  # This is typically the human player
        self.difficulty = difficulty  # "easy", "medium", "hard"
        self.decision_cooldown = 0
        self.decision_interval = self._get_decision_interval()
        self.action_duration = 0
        self.current_action = None
        self.detection_range = self._get_detection_range()
        self.aggression = self._get_aggression()
        self.intelligence = self._get_intelligence()
        self.patrolling = True
        self.patrol_point_a = Vector2(x, y)
        self.patrol_point_b = Vector2(x + random.randint(100, 300), y)
        self.current_patrol_target = self.patrol_point_b
    
    def _get_decision_interval(self):
        # How often the AI makes decisions (ms)
        if self.difficulty == "easy":
            return 60
        elif self.difficulty == "medium":
            return 30
        else:  # hard
            return 15
    
    def _get_detection_range(self):
        # Range at which AI can detect player
        if self.difficulty == "easy":
            return 150
        elif self.difficulty == "medium":
            return 300
        else:  # hard
            return 500
    
    def _get_aggression(self):
        # Likelihood to attack when player is detected
        if self.difficulty == "easy":
            return 0.3
        elif self.difficulty == "medium":
            return 0.6
        else:  # hard
            return 0.9
    
    def _get_intelligence(self):
        # How smart the AI is at predicting player movements
        if self.difficulty == "easy":
            return 0.2
        elif self.difficulty == "medium":
            return 0.5
        else:  # hard
            return 0.8
    
    def set_target(self, target):
        self.target = target
    
    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.decision_interval = self._get_decision_interval()
        self.detection_range = self._get_detection_range()
        self.aggression = self._get_aggression()
        self.intelligence = self._get_intelligence()
    
    def detect_target(self):
        if not self.target:
            return False
        
        distance = Vector2(self.target.pos).distance_to(self.pos)
        return distance <= self.detection_range
    
    def make_decision(self):
        # Reset all keys
        for key in self.keys:
            self.keys[key] = False
        
        # If we detect the target
        if self.detect_target():
            self.patrolling = False
            
            # Calculate direction to target
            direction = Vector2(self.target.pos) - self.pos
            
            # Update facing direction
            if direction.x > 0:
                self.direction = "right"
            else:
                self.direction = "left"
            
            # Move horizontally towards player
            if abs(direction.x) > 20:  # Don't get too close
                self.keys['right'] = direction.x > 0
                self.keys['left'] = direction.x < 0
            
            # Jump if player is above or there's an obstacle
            if (direction.y < -30 or 
                (self.on_ground and random.random() < 0.1 * self.intelligence)):
                self.keys['up'] = True
            
            # Attack based on aggression and if player is within reasonable range
            if (random.random() < self.aggression and 
                abs(direction.x) < 150 and abs(direction.y) < 50):
                self.keys['attack'] = True
            
            # Use jetboots occasionally (if available)
            if self.boots and not self.on_ground and random.random() < 0.3 * self.intelligence:
                self.keys['boots'] = True
        else:
            # Patrol behavior when no target detected
            self.patrolling = True
            self.patrol()
    
    def patrol(self):
        # Simple patrol between two points
        if self.patrolling:
            if Vector2(self.pos).distance_to(self.current_patrol_target) < 20:
                # Switch patrol targets
                if self.current_patrol_target == self.patrol_point_a:
                    self.current_patrol_target = self.patrol_point_b
                else:
                    self.current_patrol_target = self.patrol_point_a
            
            # Move towards current patrol target
            direction = self.current_patrol_target - self.pos
            self.keys['right'] = direction.x > 0
            self.keys['left'] = direction.x < 0
            
            # Jump occasionally or if stuck
            if self.on_ground and random.random() < 0.05:
                self.keys['up'] = True
    
    def update(self, others, screen=None):
        # AI decision making logic
        self.decision_cooldown -= 1
        if self.decision_cooldown <= 0:
            self.make_decision()
            self.decision_cooldown = self.decision_interval
        
        # Call the parent class update method
        super().update(others, screen)
    
    def draw(self, screen):
        super().draw(screen)
        
        # Optional: Visualize AI state for debugging
        if __debug__:
            # Draw detection range circle
            pygame.draw.circle(screen, (255, 0, 0, 64), 
                               (int(self.pos.x + self.width/2), int(self.pos.y + self.height/2)), 
                               self.detection_range, 1)
            
            # Draw patrol points
            if self.patrolling:
                pygame.draw.circle(screen, (0, 255, 0), 
                                  (int(self.patrol_point_a.x), int(self.patrol_point_a.y)), 5)
                pygame.draw.circle(screen, (0, 255, 0), 
                                  (int(self.patrol_point_b.x), int(self.patrol_point_b.y)), 5)
                pygame.draw.line(screen, (0, 255, 0), 
                               (int(self.patrol_point_a.x), int(self.patrol_point_a.y)),
                               (int(self.patrol_point_b.x), int(self.patrol_point_b.y)), 1)