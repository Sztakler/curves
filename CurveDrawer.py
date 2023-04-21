import LinearInterpolation 
from numpy import linspace
import pygame

class CurveDrawer:
    def __init__(self, nodes):
        self.algorithm = LinearInterpolation.LinearInterpolation(nodes)
        self.nodes = list(nodes)
        print(self.nodes)

    def draw(self, surface):
        ts = linspace(0, 800, 1000) 
        line = []
        for t in ts:
          line.append((t, self.algorithm.interpolate(t)))  


        print(line)
        return line
        
    def print(self):
        print(self.nodes)
    
