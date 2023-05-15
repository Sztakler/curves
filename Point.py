import pygame

class Point:
    def __init__(self, x, y, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.color = color

    def getCoordinates(self):
        return [self.x, self.y]
    
    def draw(self, surface, thickness, color):
        pygame.draw.circle(surface, color, self.getCoordinates(), thickness)
