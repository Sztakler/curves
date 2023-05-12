from math import comb, pow

class BezierCurve:
    def __init__(self, points):
        self.points = points

    def binomial_coefficient(self, n, k):
        return comb(n, k)

    def bernstein_polynomial(self, n, i, t):
        return self.binomial_coefficient(n, i) * pow((1 - t), (n - i)) * pow(t, i)

    def bezier(self, t):
        x = 0
        y = 0
        n = len(self.points)
        for i in range(n):
            x += self.bernstein_polynomial(n-1, i, t) * self.points[i].x         
            y += self.bernstein_polynomial(n-1, i, t) * self.points[i].y         

        return [x, y]
       
    def interpolate(self, ts):
        curve = []

        for t in ts:
            curve.append(self.bezier(t))

        return curve


