import LinearInterpolation 
from numpy import linspace
import pygame

class CurveDrawer:
    def __init__(self, nodes):
        self.algorithm = LinearInterpolation.LinearInterpolation(nodes)
        self.nodes = list(nodes)
        # print(self.nodes)

    def draw(self, surface):
        ts = linspace(0, 800, 1000) 
        line = []
        for t in ts:
          line.append((self.algorithm.interpolate(t, 'x'), self.algorithm.interpolate(t, 'y')))  
        interpolated_curve = self.algorithm.interpolate(ts)

        # print(line)
        return line
        
    def print(self):
        print(self.nodes)
    
