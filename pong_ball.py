import pyxel
import random
import numpy as np
import math

class PongBall():
    def __init__(self, color):
        self.color = color
        self.radius = 3
        self.width = self.radius
        self.height = self.radius
        self.base_speed = 2

        self.reset()
        
    def get_random_dir(self):
        return random.choice(np.arange(-1.0, 1.1, 0.3))
    
    def update(self):
        self.add_normalized_speed()
        self.check_out_of_bounds()
        
    def draw(self):
        pyxel.circ(self.x, self.y, self.radius, self.color)
        
    def reset(self):
        self.x = pyxel.width * 0.5
        self.y = pyxel.height * 0.5
        self.base_speed = 2
        self.x_speed = random.choice([-1, 1])
        self.y_speed = self.get_random_dir()
        
    def add_normalized_speed(self): 
        vector_length = math.sqrt(self.x_speed**2 + self.y_speed**2)
        if vector_length > 0:
            self.x += (self.x_speed / vector_length) * self.base_speed
            self.y += (self.y_speed / vector_length) * self.base_speed
            
    def check_out_of_bounds(self):
        padding = 1
        if self.y + self.radius > pyxel.height:
            self.y_speed *= -padding
            self.y = pyxel.height - self.radius - padding
            self.base_speed +=0.3
        elif self.y - self.radius < 0:
            self.y_speed *= -padding
            self.y = self.radius + padding
            self.base_speed +=0.3
    
    def collide(self, other):
        self.base_speed +=0.3
        padding = 1
        self.x_speed *= -padding
        self.y_speed = self.get_random_dir()
        if self.x > pyxel.width * 0.5:
            self.x = other.x - padding
        else:
            self.x = other.x + other.width + padding