from math import comb, pow

def binomial_coefficient(n, k):
    return comb(n, k)

def bernstein_polynomial(n, i, t):
    return binomial_coefficient(n, i) * pow((1 - t), (n - i)) * pow(t, i)

def deCasteljau(t, coefficients):
    betas = [coefficient for coefficient in coefficients]
    n = len(betas)
    for i in range(1, n):
        for j in range(n - i):
            betas[j] = betas[j] * (1 - t) + betas[j+1] * t
    return betas[0]

class Generator:
    def __init__(self):
        pass

    def generate(self, points, ts):
        pass
    
    def split(self, coefficients, t):
        betas = [coefficient for coefficient in coefficients]
        newCurvesCoefficients = [[betas[0]], [betas[-1]]]
        n = len(betas)
        for i in range(1, n):
            for j in range(n - i):
                betas[j] = betas[j] * (1 - t) + betas[j+1] * t
            newCurvesCoefficients[0].append(betas[0])
            newCurvesCoefficients[1].append(betas[j])
        return newCurvesCoefficients

class BezierGenerator(Generator):
    def generate(self, points, ts):
        curve = []
        for t in ts:
            curve.append(self.calculatePointDeCasteljau(points, t))
        return curve
    
    def calculatePoint(self, points, t):
        x = 0
        y = 0
        n = len(points)
        for i in range(n):
            x += bernstein_polynomial(n-1, i, t) * points[i].x         
            y += bernstein_polynomial(n-1, i, t) * points[i].y         
        return [x, y]

    def calculatePointDeCasteljau(self, points, t):
        xs = [point.x for point in points]
        ys = [point.y for point in points]
        x = deCasteljau(t, xs)
        y = deCasteljau(t, ys)
        return [x, y]

class RationalBezierGenerator(Generator):
    def generate(self, points, ts):
        curve = []
        for t in ts:
            curve.append(self.calculatePoint(points, t))
        return curve

    def calculatePoint(self, points, t):
        bernsteinWeightedSum = self.getBernsteinWeightedSum(points, t)
        bezierPoint = [0, 0]
        n = len(points)
        for i in range(n):
            bezierPoint[0] += bernstein_polynomial(n-1, i, t) * points[i].x * points[i].weight
            bezierPoint[1] += bernstein_polynomial(n-1, i, t) * points[i].y * points[i].weight

        bezierPoint[0] /= bernsteinWeightedSum
        bezierPoint[1] /= bernsteinWeightedSum

        return bezierPoint

    def getBernsteinWeightedSum(self, points, t):
        bernsteinWeightedSum = 0
        n = len(points)
        for i in range(n):
            bernsteinWeightedSum += bernstein_polynomial(n-1, i, t) * points[i].weight
        return bernsteinWeightedSum
