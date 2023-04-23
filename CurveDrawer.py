import LinearInterpolation 

class CurveDrawer:
    def __init__(self, points, nodes):
        self.points = points
        self.nodes = nodes

    def draw(self, ts):
        xs = [point[0] for point in self.points]
        ys = [point[1] for point in self.points]
    
        interpolated_xs = LinearInterpolation.LinearInterpolation(xs, self.nodes).interpolate(ts)
        interpolated_ys = LinearInterpolation.LinearInterpolation(ys, self.nodes).interpolate(ts)
        
    

        interpolated_curve = list(zip(interpolated_xs, interpolated_ys))
        return interpolated_curve
        
    def print(self):
        print(self.points)
    
