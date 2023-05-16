import pygame
import LinearInterpolation 
import NaturalCubicSplines
import BezierCurves
from numpy import linspace

class CurveDrawer:
    def __init__(self, user_points, interpolation_method, nodes_method=None, ts_len=1000):
        self.points = user_points
        self.nodes = []
        self.nodes_method = nodes_method
        self.interpolation_method = interpolation_method
        self.algorithm = self.select_algorithm(interpolation_method)
        self.interpolated_curve = []
        self.ts = []
        self.ts_len = ts_len
        
        if len(self.points) > 2:
            if self.nodes_method != None:
                self.nodes = self.nodes_method(self.points)
                self.ts = list(linspace(self.nodes[0], self.nodes[-1], self.ts_len))
            else:
                self.ts = list(linspace(0, 1, self.ts_len))
            self.generate_interpolated_curve()


    def select_algorithm(self, method):
        if method == "lagrange":
            return LinearInterpolation.LinearInterpolation(self.points, self.nodes)
        elif method == "spline":
            return NaturalCubicSplines.NaturalCubicSplines(self.points)
        elif method == "bezier":
            return BezierCurves.BezierCurve(self.points, "bezier")
        elif method == "rational-bezier":
            return BezierCurves.BezierCurve(self.points, "rational-bezier")
        else:
            return NaturalCubicSplines.NaturalCubicSplines(self.points)
    

    def generate_interpolated_curve(self):
        if len(self.points) < 2:
            return

        self.interpolated_curve = self.algorithm.interpolate(self.ts)


    def update(self, new_user_points):
        self.points = new_user_points
        if self.nodes_method != None:
            self.nodes = self.nodes_method(self.points)
            if len(self.nodes) < 1:
                self.ts = list(linspace(0, 0, self.ts_len))
            else:
                self.ts = list(linspace(self.nodes[0], self.nodes[-1], self.ts_len))
        else:
            self.ts = list(linspace(0, 1, self.ts_len))
        
        self.algorithm = self.select_algorithm(self.interpolation_method)
        self.generate_interpolated_curve()


    def draw(self, surface, color):
        if len(self.points) < 2:
            return

        pygame.draw.aalines(surface, color, closed=False, points=self.interpolated_curve);
        

    def print(self):
        print(self.points)
    
