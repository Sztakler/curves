class LinearInterpolation:
    def __init__(self, points, nodes):
        self.points = points
        self.nodes = nodes 
        self.weights= []
        self.calculate_weights()
        self.linx = lambda x : x
        self.liny = lambda x : x
        pass

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
        for i in range(0, len(self.nodes)):
            quotient = 1
            for j in range(0, len(self.nodes)):
                if i == j:
                    continue
                quotient *= (self.nodes[i] - self.nodes[j]) 
            self.weights.append(1 / quotient)
       
    def interpolate(self, ts):
        values = []
        
        for t in ts:
            values.append(self.baricentric_formula(t))

        return values
