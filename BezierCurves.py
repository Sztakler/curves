from Point import Point
from Generators import BezierGenerator, RationalBezierGenerator

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


    def assignGenerator(self):
        if self.kind == "bezier":
            return BezierGenerator() 
        elif self.kind == "rational-bezier":
            return RationalBezierGenerator()
        else:
            return BezierGenerator() 

    def interpolate(self, ts):
        return self.generator.generate(self.points, ts) 


