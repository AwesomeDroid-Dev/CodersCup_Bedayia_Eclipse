from pygame import Vector2
from Classes.Object import Object

class MovableObject(Object):
    def __init__(self, x, y, width, height, color, speed, gravity):
        super().__init__(x, y, width, height, color)
        self.speed = speed
        self.grav = gravity
        self.vel = Vector2(0, 0)
        self.step = 1
        
        self.type = "movable"

    def moveCollide(self, dx, dy, others):
        steps_x = int(abs(dx) / self.step)
        step_x = self.step if dx > 0 else -self.step
        for _ in range(steps_x):
            self.move(step_x, 0)
            for obj in others:
                if self.collide(obj):
                    self.move(-step_x, 0)
                    self.vel.x = 0
                    break

        steps_y = int(abs(dy) / self.step)
        step_y = self.step if dy > 0 else -self.step
        for _ in range(steps_y):
            self.move(0, step_y)
            for obj in others:
                if self.collide(obj):
                    self.move(0, -step_y)
                    self.vel.y = 0
                    break

    def applyGravity(self, others):
        self.vel.y += self.grav
        self.moveCollide(0, self.vel.y, others)

    def updateVelocity(self, others):
        self.moveCollide(self.vel.x, self.vel.y, others)