class LinearInterpolation:
    def __init__(self, nodes, ts):
        self.nodes = nodes
        self.ts = ts
        self.weights= []
        self.calculate_weights()
        self.linx = lambda x : x
        self.liny = lambda x : x
        pass

    def calculate_weights(self):
        for i in range(0, len(self.ts)):
            quotient = 1
            for j in range(0, len(self.ts)):
                if i == j:
                    continue
                quotient *= (self.ts[i] - self.ts[j]) 
            self.weights.append(1 / quotient)
   

    def baricentric_formula(self, t, axis):
        points = []
        if axis == "x":
            print("x")
            points = [node[0] for node in self.nodes]
        else:
            points = [node[1] for node in self.nodes]
            print("y")

        def sum_of_weighted_points():
            result = 0
            for i in range(len(self.nodes)):
               result += (self.weights[i]) / (t - self.ts[i]) * points[i]
            return result
        
        def sum_of_weights():
            result = 0
            for i in range(len(self.nodes)):
                result += (self.weights[i]) / (t - self.ts[i])
            return result


        if t in self.ts:
            index = self.nodes.index(t) 
            return points[index]
        else:
            return sum_of_weighted_points() / sum_of_weights()
    
    def interpolate(self, ts):
        curve = []
        xs = [node[0] for node in self.nodes]
        ys = [node[1] for node in self.nodes]
     
        

    def interpolate(self, t, axis):
        return self.baricentric_formula(t, axis)
