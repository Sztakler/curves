from ctypes.wintypes import RGB
from math import *
from CurveDrawer import CurveDrawer
from Point import Point
from ConvexHull import ConvexHull
from utils import HULLMETHOD

class Curve:
    def __init__(self, points, color=(255, 255, 255), interpolationMethod="bezier", nodesMethod=None, tsLen=1000, convexHullMethod=HULLMETHOD.GRAHAM_SCAN, pointThickness=3, lineThickness=1):
        self.points = points
        self.curveDrawer = CurveDrawer(user_points=self.points, interpolation_method=interpolationMethod, nodes_method=nodesMethod, ts_len=tsLen)
        self.color = color
        self.baseColor = color
        self.pointThickness = pointThickness
        self.lineThickness = lineThickness
        self.isSelected = False
        self.convexHull = ConvexHull(self.points, self.getColorInverse(self.color), convexHullMethod)

    def draw(self, surface, draw_points=False):
        for point in self.points:
            point.draw(surface=surface, radius=self.pointThickness, thickness=self.pointThickness, color=self.color)   

        if len(self.points) > 1:
            self.curveDrawer.draw(surface, self.color, self.lineThickness)

        self.convexHull.draw(surface)

    def append(self, point):
        self.points.append(point)
        self.update(self.points)

    def remove(self, point):
        if point in self.points:
            self.points.remove(point)

    def update(self, points=None):
        if points == None:
            points = self.points
        self.points = points
        self.curveDrawer.update(points)
        self.convexHull.update(points)

    def clear(self):
        self.points = []

    def split(self, t):
        return self.curveDrawer.split()

    def raiseDegree(self):
        return self.curveDrawer.raiseDegree()

    def lowerDegree(self):
        return self.curveDrawer.lowerDegree()

    def join(self, other):
        return self.curveDrawer.join(other)

    def select(self, colorOverride):
        self.color = colorOverride
        self.isSelected = True

    def deselect(self):
        self.color = self.baseColor
        self.isSelected = False

    def changeSelectedPointWeight(self, weightDelta, pointIndex):
        if pointIndex == None or self.points[pointIndex].weight + weightDelta < 0:
            return

        self.points[pointIndex].weight += weightDelta
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

    def modifyLineThickness(self, value):
        self.lineThickness += value

    def modifyPointThickness(self, value):
        self.pointThickness += value

    def changeColor(self, color):
        self.color = color[:]
        self.baseColor = color[:]
        self.convexHull.changeColor(self.getColorInverse(self.color))

    def getColorInverse(self, color):
        return (255 - color[0], 255 - color[1], 255 - color[2], color[3])