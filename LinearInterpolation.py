class LinearInterpolation:
    def __init__(self, points, nodes):
        self.points = points
        self.nodes = nodes 
        self.weights= []
        self.calculate_weights()

    def baricentric_formula(self, t):
        def sum_of_weights(t):
            result = 0
            for i in range(len(self.weights)):
                result += self.weights[i] / (t - self.nodes[i])
            return result

        def sum_of_weighted_points(t):
            result = 0
            for i in range(len(self.weights)):
                result += self.weights[i] / (t - self.nodes[i]) * self.points[i]
            return result

        def is_node(t, epsilon):
            i = 0
            while i < len(self.nodes):
                node = self.nodes[i]
                if abs(node - t) <= epsilon:
                    return (True, self.points[i])
                i += 1
            return (False, None)

        t_is_node, value = is_node(t, 0.001)
        if t_is_node:
            return value 
        else:
            return sum_of_weighted_points(t) / sum_of_weights(t) 

    def calculate_weights(self):
        self.weights = []
        for i in range(0, len(self.nodes)):
            quotient = 1
            for j in range(0, len(self.nodes)):
                if i == j:
                    continue
                quotient *= (self.nodes[i] - self.nodes[j]) 
            self.weights.append(1 / quotient)
       
    def interpolate(self, ts):
        def calculate_values(points):
            values = []
            self.points = points
            self.calculate_weights()

            for t in ts:
                values.append(self.baricentric_formula(t))

            return values

        xs = [point.x for point in self.points]
        ys = [point.y for point in self.points]
   

        interpolated_xs = calculate_values(xs)
        interpolated_ys = calculate_values(ys)

        interpolated_curve = list(zip(interpolated_xs, interpolated_ys))
        return interpolated_curve
