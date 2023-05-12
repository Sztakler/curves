from ctypes.wintypes import RGB
from functools import reduce
from math import *
import sys

import numpy
import pygame
import pygame_gui

import CurveDrawer
from CurveDrawer import CurveDrawer
from Point import Point
from ConvexHull import ConvexHull
from utils import HULLMETHOD

class Curve:
    def __init__(self, points, color=(255, 255, 255), interpolationMethod="bezier", nodesMethod=None, tsLen=1000, convexHullMethod=HULLMETHOD.GRAHAM_SCAN):
        self.points = points
        self.curveDrawer = CurveDrawer(user_points=self.points, interpolation_method=interpolationMethod, nodes_method=nodesMethod, ts_len=tsLen)
        self.color = color
        self.convexHull = ConvexHull(self.points, (255, 0, 255), convexHullMethod)

    def draw(self, surface, draw_points=False):
        for point in self.points:
            point.draw(surface=surface, thickness=3.0)

        if len(self.points) > 1:
            self.curveDrawer.draw(surface, self.color)

        self.convexHull.draw(surface)
    
    def update(self, points):
        self.points = points
        self.curveDrawer.update(points)
        self.convexHull.update(points)

    def move_points(self, direction):
        if len(self.points) < 1:
            return

        if direction == "left":
            for point in self.points:
                point.x -= 10
        if direction == "right":
            for point in self.points:
                point.x += 10
        if direction == "up":
            for point in self.points:
                point.y -= 10
        if direction == "down":
            for point in self.points:
                point.y += 10
        self.update()
