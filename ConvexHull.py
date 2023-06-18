import pygame
from functools import reduce
from utils import HULLMETHOD

class ConvexHull:
    def __init__(self, points, color=(255, 255, 255), method=HULLMETHOD.GRAHAM_SCAN):
      self.method = method
      self.color = color
      self.hull = self.generateConvexHull(points)
      self.isRendered = False

    def update(self, points):
       self.hull = self.generateConvexHull(points)

    def draw(self, surface):
      if len(self.hull) > 2 and self.isRendered:
            pygame.draw.aalines(surface, self.color, closed=True, points=self.hull)
        
    def toggleRendering(self):
       self.isRendered = not self.isRendered

    def GrahamScan(self, points):
      '''
      Returns points on convex hull in CCW order according to Graham's scan algorithm. 
      By Tom Switzer <thomas.switzer@gmail.com>.
      '''
      points = [[point.x, point.y] for point in points]
      TURN_LEFT, TURN_RIGHT, TURN_NONE = (1, -1, 0)

      def cmp(a, b):
          return (a > b) - (a < b)

      def turn(p, q, r):
          return cmp((q[0] - p[0])*(r[1] - p[1]) - (r[0] - p[0])*(q[1] - p[1]), 0)

      def _keep_left(hull, r):
          while len(hull) > 1 and turn(hull[-2], hull[-1], r) != TURN_LEFT:
              hull.pop()
          if not len(hull) or hull[-1] != r:
              hull.append(r)
          return hull

      points = sorted(points)
      l = reduce(_keep_left, points, [])
      u = reduce(_keep_left, reversed(points), [])
      return l.extend(u[i] for i in range(1, len(u) - 1)) or l     

    def generateConvexHull(self, points):
      if self.method == HULLMETHOD.GRAHAM_SCAN:
        return self.GrahamScan(points)
      if self.method == HULLMETHOD.QUICK_HULL:
        raise NotImplementedError

    def changeColor(self, color):
       self.color = color