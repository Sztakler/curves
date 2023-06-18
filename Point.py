import pygame

class Point:
    def __init__(self, x, y, color=(255, 255, 255), weight=1.0):
        self.x = x
        self.y = y
        self.color = color
        self.weight = weight

    def getCoordinates(self):
        return [self.x, self.y]
    
    def draw(self, surface, radius, thickness, color):
        pygame.draw.circle(surface, color, self.getCoordinates(), radius, thickness)