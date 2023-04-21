class LinearInterpolation:
    def __init__(self, nodes: list):
        self.nodes = nodes
        self.weights= []
        self.calculate_weights()
        pass

    def calculate_weights(self):
        ts = [node[0] for node in self.nodes]
        for i in range(0, len(ts)):
            quotient = 1
            for j in range(0, len(ts)):
                if i == j:
                    continue
                quotient *= 1 / (ts[i] - ts[j]) 
            print("quotient", quotient)
            self.weights.append(quotient)
    
    def baricentric_formula(self, t):
        ts = [node[0] for node in self.nodes]
        ys = [node[1] for node in self.nodes]
    
        def sum_of_weighted_points():
            result = 0
            for i in range(len(self.nodes)):
               result += (self.weights[i]) / (t - ts[i]) * ys[i]
            return result
        
        def sum_of_weights():
            result = 0
            for i in range(len(self.nodes)):
                result += (self.weights[i]) / (t - ts[i])
            return result


        if t in ts:
            index = self.nodes.index(t) 
            return ys[index]
        else:
            return sum_of_weighted_points() / sum_of_weights()

    def interpolate(self, t):
        return self.baricentric_formula(t)
