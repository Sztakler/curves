from numpy import linspace
from math import isnan

class BSpline:
    def __init__(self, points, degree):
        self.points = points
        self.degree = degree
        knots = list(linspace(0, 1, len(self.points) + degree))
        self.knots = [knots[0]] * degree + knots + [knots[-1]] * degree

    def getIntervalIndex(self, x):
        for i in range(0, len(self.knots) - 1):
            if (x >= self.knots[i] and x <= self.knots[i+1]):
                return i
        return None

    def deBoor(self, points, x):
        interval_index = self.getIntervalIndex(x)
        if interval_index is None:
            return points[0]

        d = []
        for j in range(0, self.degree + 1):
            index = j + interval_index - self.degree
            if index < 0 and index < len(points):
                d.append(points[0])
            elif index >= len(points):
                d.append(points[-1])
            else:
                d.append(points[index])

        for r in range(1, self.degree + 1):
            for j in range(self.degree, r - 1, -1):
                alpha = (x - self.knots[j + interval_index - self.degree]) / (
                    self.knots[j + 1 + interval_index - r] - self.knots[j + interval_index - self.degree])
                d[j] = (1.0 - alpha) * d[j - 1] + alpha * d[j]

        if isnan(d[self.degree]):
            return points[0]
        return d[self.degree]

    def calculatePointDeBoorCox(self, xs, ys, t):
        return (self.deBoor(xs, t), self.deBoor(ys, t))

    def interpolate(self, ts):
        curve = []
        xs = [point.x for point in self.points]
        ys = [point.y for point in self.points]

        for t in ts:
            curve.append(self.calculatePointDeBoorCox(xs, ys, t))
        return curve
