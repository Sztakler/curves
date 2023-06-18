from Point import Point
from Generators import BezierGenerator, RationalBezierGenerator

import numpy as np

class BezierCurve:
    def __init__(self, points, kind):
        self.points = points
        self.kind = kind
        self.generator = self.assignGenerator()

    def split(self):
        xs = [point.x for point in self.points]
        ys = [point.y for point in self.points]

        curves = [[], []]
        
        curve1_x, curve2_x = self.generator.split(xs, 0.5)
        curve1_y, curve2_y = self.generator.split(ys, 0.5)

        curves[0] = [Point(element[0], element[1]) for element in list(zip(curve1_x, curve1_y))]
        curves[1] = [Point(element[0], element[1]) for element in list(zip(curve2_x, curve2_y))]

        return curves

    def raiseDegree(self):
        points_copy = self.points[:] 
        k = len(points_copy)
        new_points = [points_copy[0]]

        for i in range(1, k):
            current = points_copy[i]
            previous = points_copy[i - 1]
            new_points.append(Point(x=((k - i) / k * current.x + (i / k) * previous.x),
                    y=((k - i) / k * current.y + (i / k) * previous.y)))

        new_points.append(points_copy[k - 1])
        self.points = new_points[:]

        return self.points

    def lowerDegree(self):
        points_copy = self.points[:]
        k = len(points_copy)
        data = []
        n = k - 1

        if k <= 3:
            return None
        
        for i in range(k):
            data.append( [0] * (k-1) )
            if i == 0:
                data[i][0] = 1
            elif i == n:
                data[i][i-1] = 1
            else:
                data[i][i-1] = i / k
                data[i][i] = 1 - data[i][i - 1]

        M = np.array(data)
        Mt = M.transpose()
        Mc = np.matmul(Mt, M)
        Mi = np.linalg.inv(Mc)

        V = np.matmul(Mi, Mt)
        x = np.array([point.x for point in points_copy])
        nx = np.matmul(V, x).tolist()
        y = np.array([point.y for point in points_copy])
        ny = np.matmul(V, y).tolist()
        
        new_points = []
        for x, y in zip(nx, ny):
            new_points.append(Point(x, y))

        return new_points
        
    def join(self, other):
        if other is None:
            print("Other curve was not selected")
            return None

        # Class C0
        #self.points[-1] = other.points[0]

        # Class C1
        n = len(self.points)
        m = len(other.points)

        new_x = (n / m) * (self.points[-1].x - self.points[-2].x) + other.points[0].x
        new_y = (n / m) * (self.points[-1].y - self.points[-2].y) + other.points[0].y

        other.points[1] = Point(new_x, new_y)
        
        new_points = self.points[:-1] + other.points[:]
        
        return new_points

    def assignGenerator(self):
        if self.kind == "bezier":
            return BezierGenerator() 
        elif self.kind == "rational-bezier":
            return RationalBezierGenerator()
        else:
            return BezierGenerator() 

    def interpolate(self, ts):
        return self.generator.generate(self.points, ts) 


