
from Generators import BezierGenerator, RationalBezierGenerator

class BezierCurve:
    def __init__(self, points, kind):
        self.points = points
        self.kind = kind
        self.generator = self.assignGenerator()

    def assignGenerator(self):
        if self.kind == "bezier":
            return BezierGenerator() 
        elif self.kind == "rational-bezier":
            return RationalBezierGenerator()
        else:
            # default
            pass

    def interpolate(self, ts):
        return self.generator.generate(self.points, ts) 


