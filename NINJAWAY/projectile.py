import pygame

class Projectile:
    def __init__(self, x, y, width, height, speed, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color

    def update(self):
        self.x += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def on_hit(self, target):
        pass