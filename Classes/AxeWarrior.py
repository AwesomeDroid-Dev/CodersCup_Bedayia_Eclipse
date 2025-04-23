import pygame
import random
import math
from Classes.AIPlayer import AIPlayer
from Classes.Axe import Axe

class AxeWarrior(AIPlayer):
    def __init__(self, x, y, width, height, player, health=150, speed=3.5):
        super().__init__(x, y, width, height, player, health=health, speed=speed)
        
        # Override some base AI attributes to match axe-fighting style
        self.detection_radius = 350  # Larger detection radius
        self.attack_radius = 120     # Custom attack radius for axe
        self.decision_delay = 20     # Faster decisions
        self.aggression = random.uniform(0.7, 0.9)  # More aggressive
        
        # Axe-specific attributes
        self.charge_timer = 0
        self.charge_duration = 45
        self.is_charging = False
        self.retreat_after_attack = True
        self.shockwave_cooldown = 0
        self.state_memory = []  # Track recent states for pattern prevention
        
        # Customize appearance
        self.color = (180, 60, 60)  # Darker red for axe warrior
        
        # Create and equip the axe as the primary weapon
        self.axe = Axe(10, -10, 50, 50, self)
        self.tools = [self.axe, None, None]  # Add axe as first tool
        self.current_tool = self.axe
        self.preferred_weapon = "Axe"
        
    def think(self, game_objects, player):
        """Enhanced decision-making specifically for axe combat"""
        if self.decision_cooldown > 0:
            self.decision_cooldown -= 1
            return
            
        self.decision_cooldown = self.decision_delay
        
        # Track state memory to prevent repetitive behavior
        if len(self.state_memory) >= 5:
            self.state_memory.pop(0)
        self.state_memory.append(self.state)
        
        # Update shockwave cooldown
        if self.shockwave_cooldown > 0:
            self.shockwave_cooldown -= 1
        
        # Check health status and consider retreating
        health_percentage = self.health / self.max_health
        if health_percentage < 0.25:
            self.state = "retreat"
            self.current_target = None
            return
            
        # Detect player and other entities
        targets = self.detect_targets(game_objects, player)
        
        # State machine logic enhanced for axe combat
        if self.state == "idle":
            # Higher chance to be proactive with axe
            if random.random() < 0.7:
                self.state = "wander"
                self.set_wander_point()
            
            # Check for targets
            if targets and random.random() < self.aggression:
                self.select_target(targets)
                if self.current_target:
                    self.state = "chase"
                    self.chase_timer = self.patience
        
        elif self.state == "wander":
            # Check if we've reached wander point or timeout
            if self.wander_time <= 0 or (self.wander_point and self.distance_to(self.wander_point) < 20):
                if "idle" in self.state_memory[-2:]:  # Avoid repeating idle-wander loop
                    self.state = "search"  # New state to break patterns
                else:
                    self.state = "idle"
                
            # Check for targets while wandering
            if targets and random.random() < self.aggression * 1.5:
                self.select_target(targets)
                if self.current_target:
                    self.state = "chase"
                    self.chase_timer = self.patience
            
            self.wander_time -= 1
            
        elif self.state == "search":
            # More directed exploration to find targets
            if not self.wander_point or random.random() < 0.1:
                self.set_strategic_search_point(game_objects)
            
            # Check distance to search point
            if self.wander_point and self.distance_to(self.wander_point) < 30:
                self.state = "idle"
                
            # Check for targets while searching
            if targets:
                self.select_target(targets)
                if self.current_target:
                    self.state = "chase"
                    self.chase_timer = self.patience
            
        elif self.state == "chase":
            # Lost interest in chasing
            if self.chase_timer <= 0:
                self.state = "idle"
                self.current_target = None
                return
                
            # Target no longer valid
            if not self.is_valid_target(self.current_target):
                if self.last_known_target_pos and random.random() < 0.8:  # Higher chance to investigate
                    # Go to last known position
                    self.move_to_position(self.last_known_target_pos)
                    if self.distance_to(self.last_known_target_pos) < 20:
                        self.state = "search"  # Switch to search instead of idle
                        self.current_target = None
                else:
                    self.state = "search"
                    self.current_target = None
                return
                
            # Update last known position
            self.last_known_target_pos = (self.current_target.rect.x, self.current_target.rect.y)
                
            # Check if within attack range - for axe warriors we want to get close
            target_distance = self.distance_to_entity(self.current_target)
            
            # Start charging attack when in range
            if target_distance < self.attack_radius * 1.5 and not self.is_charging:
                # Chance to use shockwave based on cooldown and distance
                if self.shockwave_cooldown <= 0 and target_distance < self.attack_radius * 0.7:
                    self.state = "prepare_shockwave"
                else:
                    # Regular axe attack
                    self.state = "charge_attack"
                    self.is_charging = True
                    self.charge_timer = self.charge_duration
            else:
                # Continue chase
                self.chase_timer -= 1
                
        elif self.state == "charge_attack":
            # Charging up before a powerful axe attack
            if not self.is_valid_target(self.current_target):
                self.state = "search"
                self.is_charging = False
                return
                
            # Continue approaching during charge
            target_distance = self.distance_to_entity(self.current_target)
            if target_distance > self.attack_radius * 0.6:
                self.move_to_entity(self.current_target, stop_distance=self.attack_radius * 0.5)
            
            # Count down charge timer
            if self.charge_timer > 0:
                self.charge_timer -= 1
                
                # Slow movement during final charge-up
                if self.charge_timer < 10:
                    self.velocity_x *= 0.5
                    self.velocity_y *= 0.5
            else:
                # Charge complete, execute the attack
                self.state = "attack"
                self.is_charging = False
                
        elif self.state == "prepare_shockwave":
            # Special state for preparing shockwave attack
            if not self.is_valid_target(self.current_target):
                self.state = "search"
                return
                
            # Get into perfect position for shockwave
            target_distance = self.distance_to_entity(self.current_target)
            ideal_distance = self.attack_radius * 0.7
            
            if abs(target_distance - ideal_distance) > 20:
                if target_distance > ideal_distance:
                    self.move_to_entity(self.current_target, stop_distance=ideal_distance)
                else:
                    self.move_away_from(self.current_target)
                    self.velocity_x *= 0.5  # Move away more slowly
                    self.velocity_y *= 0.5
            else:
                # In position - execute shockwave attack!
                self.state = "attack"
                self.shockwave_cooldown = 120  # Long cooldown for powerful attack
                    
        elif self.state == "attack":
            # Execute the attack
            if not self.is_valid_target(self.current_target):
                self.state = "search"
                return
                
            # Make sure we're facing the target
            if self.current_target.rect.x > self.rect.x:
                self.direction = "right"
            else:
                self.direction = "left"
                
            # Use the axe
            self.use_axe()
            
            # After attacking, briefly retreat to reposition
            if self.retreat_after_attack and random.random() < 0.7:
                self.state = "reposition"
            else:
                self.state = "chase"  # Go back to chase for another attack
                
        elif self.state == "reposition":
            # Tactical repositioning after attack
            if not self.is_valid_target(self.current_target):
                self.state = "search"
                return
                
            # Calculate a strategic repositioning direction
            target_angle = math.atan2(
                self.current_target.rect.centery - self.rect.centery,
                self.current_target.rect.centerx - self.rect.centerx
            )
            
            # Move to the side of the target
            reposition_angle = target_angle + (math.pi/2 if random.random() < 0.5 else -math.pi/2)
            reposition_distance = random.uniform(100, 150)
            
            reposition_x = self.rect.centerx + math.cos(reposition_angle) * reposition_distance
            reposition_y = self.rect.centery + math.sin(reposition_angle) * reposition_distance
            
            self.move_to_position((reposition_x, reposition_y))
            
            # If we've moved some distance or random chance, go back to chase
            if (self.distance_to((reposition_x, reposition_y)) < 30 or 
                random.random() < 0.1):
                self.state = "chase"
                    
        elif self.state == "retreat":
            # Run away from danger
            if player and self.is_valid_target(player):
                self.move_away_from(player)
            
            # Chance to stop retreating if health is better
            if health_percentage > 0.4 and random.random() < 0.05:
                self.state = "search"
    
    def set_strategic_search_point(self, game_objects):
        """Choose a strategic location to search for targets"""
        # Prioritize central areas or places where targets might be
        potential_points = []
        
        # Center of the screen is often a good place to search
        screen_width, screen_height = pygame.display.get_surface().get_size()
        center_point = (screen_width / 2, screen_height / 2)
        potential_points.append((center_point, 0.5))  # (point, weight)
        
        # Add the last known target position if we have one
        if self.last_known_target_pos:
            potential_points.append((self.last_known_target_pos, 0.8))
            
        # Add some random points
        for _ in range(3):
            random_x = random.randint(100, screen_width - 100)
            random_y = random.randint(100, screen_height - 100)
            potential_points.append(((random_x, random_y), 0.3))
            
        # Select a point based on weights
        weights = [p[1] for p in potential_points]
        total_weight = sum(weights)
        normalized_weights = [w / total_weight for w in weights]
        
        chosen_index = random.choices(range(len(potential_points)), normalized_weights)[0]
        self.wander_point = potential_points[chosen_index][0]
        self.wander_time = random.randint(90, 150)  # Longer search time
    
    def use_axe(self):
        """Specialized method for using the axe effectively"""
        # Make sure we have the axe equipped
        if self.current_tool != self.axe:
            for i, tool in enumerate(self.tools):
                if tool and tool.type == "Axe":
                    self.change_tool(i)
                    break
        
        # Use the axe
        if hasattr(self.current_tool, 'activate'):
            self.current_tool.activate()
    
    def update(self, game_objects=None, player=None):
        """Enhanced update function for axe warrior"""
        # Call the parent update method
        super().update(game_objects, player)
        
        # Visual effect for charging
        if self.is_charging:
            # You could add visual effects here in a real game
            pass
            
    def draw(self, screen):
        """Draw the axe warrior with additional visual indicators"""
        # Call parent draw method first
        super().draw(screen)
        
        # Add charging effect visualization if needed
        if self.is_charging and hasattr(self, 'debug_mode') and self.debug_mode:
            charge_percent = 1 - (self.charge_timer / self.charge_duration)
            
            # Draw charge meter above character
            charge_width = self.width * charge_percent
            charge_rect = pygame.Rect(
                self.rect.x, 
                self.rect.y - 15, 
                charge_width, 
                5
            )
            pygame.draw.rect(screen, (255, 165, 0), charge_rect)  # Orange charge bar