import pygame
import math
from Classes.PlayerBar import PlayerBar
from Classes.MovableObject import MovableObject
from Classes.PlayerTool import PlayerTool
from Classes.Weapon import Weapon

class Boss(MovableObject):
    def __init__(self, x, y, player):
        super().__init__(x, y, 36, 63, (0, 0, 0), 0, 0.3)  # 12*3, 21*3
        self.player = player
        self.direction = "right"
        self.phase = "nothing" # rise_up, charging_laser, shooting x 3, charging_jetpack
        self.max_health = 500
        self.health = 500
        self.health_bar = PlayerBar(0, -20, 60, 12, self.max_health, self.health, (255, 0, 0), self)
        self.type = "player"
        self.weapon = BossLaserGun(self, 0, 0, 80, 20, self.player)
        self.boss_cycle = 0
        
        self.old_player_pos = self.player.pos.copy()

    def update(self, others, screen):
        self.play_boss_cycle()
        if self.phase == "rise_up":
            self.rise_up()
        elif self.phase == "fall_down":
            self.fall_down()
        elif self.phase == "shooting":
            self.weapon.launch(others, screen, self.old_player_pos)
        
        if self.boss_cycle % 25 == 0:
            self.old_player_pos = self.player.pos.copy()
        
        self.applyGravity(others)
        self.updateVelocity(others)
        self.weapon.update(others, screen)
        self.draw(screen)

    def draw(self, surface):
        self.health_bar.draw(surface)
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
        self.weapon.draw(surface)
    
    def play_boss_cycle(self):
        #print(self.boss_cycle)
        self.boss_cycle += 1
        self.boss_cycle = self.boss_cycle % 1500
        if self.boss_cycle % 100 == 0 and self.boss_cycle <= 500:
            self.phase = "rise_up"
        elif self.boss_cycle % 200 == 0 and self.boss_cycle <= 1000:
            self.phase = "shooting"
        elif self.boss_cycle == 1001:
            self.phase = "fall_down"
        else:
            self.phase = "nothing"
    
    def fall_down(self):
        self.grav = 0.3

    def rise_up(self):
        self.grav = 0
        self.vel = (pygame.Vector2(600, 100) - self.pos) / 100
    
    def change_health(self, amount):
        self.health += amount
        self.health = max(0, min(self.health, self.max_health))
        self.health_bar.update(self.health)

class BossLaserGun(PlayerTool):
    def __init__(self, boss, xOffset, yOffset, width, height, player):
        super().__init__(xOffset, yOffset, width, height, player)
        self.boss = boss
        self.angle = 0
        self.boss_laser = None
        self.type = "boss_laser_gun"

        self.original_image = pygame.image.load("./Resources/boss_laser_gun.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (width, height))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, others, screen):
        self.followPlayer(self.boss)
        self.pointAt(self.player.pos)

        if self.boss_laser and self.boss_laser.active:
            self.boss_laser.update(others, screen)

    def draw(self, surface):
        self.image = pygame.transform.rotozoom(self.original_image, -self.angle, 1)
        self.rect = self.image.get_rect(center=self.pos)
        surface.blit(self.image, self.rect)

        if self.boss_laser and self.boss_laser.active:
            self.boss_laser.draw(surface)

    def pointAt(self, target_pos):
        direction = target_pos - self.pos
        self.angle = math.degrees(math.atan2(direction.y, direction.x))

    def launch(self, others, screen, target_pos):
        muzzle_offset = pygame.Vector2(self.width // 2, 0).rotate(-self.angle)
        launch_pos = self.pos + muzzle_offset
        self.boss_laser = BossLaser(self.player, launch_pos, target_pos)
        

class BossLaser(Weapon):
    def __init__(self, player, start_pos, target_pos, height=10, damage=40):
        direction_vector = target_pos - start_pos
        distance = direction_vector.length() + 100
        super().__init__(player, width=int(distance), height=height, color=(255, 100, 100), damage=damage)

        self.start_pos = pygame.Vector2(start_pos)
        self.direction = direction_vector.normalize()
        self.angle = math.degrees(math.atan2(self.direction.y, self.direction.x))
        self.timer = 100
        self.active = True
        self.type = "boss_laser"
        self.enemy = player
        self.player = self

        self.original_image = pygame.image.load("./Resources/laserbeam.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (int(distance), height))
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.update_rect()

    def update_rect(self):
        # Update the rotated hitbox as a polygon (thin laser beam)
        self.end_pos = self.start_pos + self.direction * self.width
        thickness = self.height // 2

        # Perpendicular vector for beam width
        perp = pygame.Vector2(-self.direction.y, self.direction.x) * thickness

        # Create 4 corners of the laser beam (rotated rectangle)
        self.hitbox = [
            self.start_pos + perp,
            self.start_pos - perp,
            self.end_pos - perp,
            self.end_pos + perp
        ]
        
        self.rect = self.image.get_rect(center=self.start_pos + self.direction * (self.width / 2))

    def update(self, others, screen=None):
        if not self.active:
            return

        self.update_rect()
        hits = self.check_collision(others)
        for hit in hits:
            if hit.type == "player":
                hit.change_health(-self.damage)
                self.active = False
                break

        self.timer -= 1
        if self.timer <= 0:
            self.active = False

        if screen:
            self.draw(screen)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        
        pygame.draw.polygon(surface, (255, 255, 0), self.hitbox, 2)
    
    def check_collision(self, others):
        hits = []
        laser_polygon = pygame.Rect(0, 0, 1, 1)

        for other in others:
            if hasattr(other, "rect") and other.type == "player":
                if self.polygon_collides_rect(self.hitbox, other.rect):
                    hits.append(other)
        return hits

    def polygon_collides_rect(self, polygon, rect):
        # Turn rect into a polygon
        rect_points = [
            pygame.Vector2(rect.topleft),
            pygame.Vector2(rect.topright),
            pygame.Vector2(rect.bottomright),
            pygame.Vector2(rect.bottomleft)
        ]
        return self.polygon_overlap(polygon, rect_points)

    def polygon_overlap(self, poly1, poly2):
        # Separating Axis Theorem for convex polygons
        def get_axes(poly):
            axes = []
            for i in range(len(poly)):
                p1 = poly[i]
                p2 = poly[(i + 1) % len(poly)]
                edge = p2 - p1
                normal = pygame.Vector2(-edge.y, edge.x).normalize()
                axes.append(normal)
            return axes

        def project(poly, axis):
            dots = [p.dot(axis) for p in poly]
            return min(dots), max(dots)

        axes = get_axes(poly1) + get_axes(poly2)
        for axis in axes:
            min1, max1 = project(poly1, axis)
            min2, max2 = project(poly2, axis)
            if max1 < min2 or max2 < min1:
                return False  # gap found
        return True

