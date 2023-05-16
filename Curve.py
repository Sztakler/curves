from ctypes.wintypes import RGB
from functools import reduce
from math import *
from CurveDrawer import CurveDrawer
from Point import Point
from ConvexHull import ConvexHull
from utils import HULLMETHOD

class Curve:
    def __init__(self, points, color=(255, 255, 255), interpolationMethod="bezier", nodesMethod=None, tsLen=1000, convexHullMethod=HULLMETHOD.GRAHAM_SCAN):
        self.points = points
        self.curveDrawer = CurveDrawer(user_points=self.points, interpolation_method=interpolationMethod, nodes_method=nodesMethod, ts_len=tsLen)
        self.color = color
        self.baseColor = color
        self.isSelected = False
        self.convexHull = ConvexHull(self.points, (255, 0, 255), convexHullMethod)

    def draw(self, surface, draw_points=False):
        for point in self.points:
            point.draw(surface=surface, thickness=3.0, color=self.color)

        if len(self.points) > 1:
            self.curveDrawer.draw(surface, self.color)

        self.convexHull.draw(surface)

    def update(self, points):
        self.points = points
        self.curveDrawer.update(points)
        self.convexHull.update(points)

    def select(self, colorOverride):
        self.color = colorOverride
        self.isSelected = True

    def deselect(self):
        self.color = self.baseColor
        self.isSelected = False

    def changeSelectedPointWeight(self, weightDelta, pointIndex):
        if pointIndex == None:
            return

        self.points[pointIndex].weight += weightDelta
        print(self.points[pointIndex].weight)
        self.update(self.points)

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

    def move_curve(self, offset):
        for point in self.points:
            point.x += offset[0]
            point.y += offset[1]

    def check_if_lies_on(self, point, epsilon=10):
        def distance_squared(p1, p2):
            return (p2[0] - p1[0])**2 + (p2[1] - p1[1])**2

        # https://stackoverflow.com/questions/11907947/how-to-check-if-a-point-lies-on-a-line-between-2-other-points
        curve = self.curveDrawer.interpolated_curve
        for i in range(len(curve)-1):
            node0 = curve[i]
            node1 = curve[i+1]

            if (distance_squared(node0, point) + distance_squared(point, node1) - distance_squared(node0, node1) < epsilon):
                return True
        return False
