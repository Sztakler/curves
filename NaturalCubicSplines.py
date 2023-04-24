class NaturalCubicSplines:
    def __init__(self, points):
        self.points = points
        self.splines = self.calculate_splines()

    def calculate_splines(self):
        n = len(self.points)
        x = [point[0] for point in self.points]
        y = [point[1] for point in self.points]

        a = []
        for i in range(0, n):
            a.append(y[i])

        b = [1] * (n - 1)
        d = [1] * (n - 1)
        h = [1] * (n - 1)

        for i in range(0, n - 1):
            h[i] = y[i+1] - y[i]

        alpha = [1] * (n - 1)
        for i in range(1, n - 1):
            alpha[i] = (3 / h[i] * (a[i+1] - a[i])) - (3 / h[i-1] * (a[i] - a[i-1]))
    
        c = [1] * n
        l = [1] * n 
        u = [1] * n 
        z = [1] * n

        l[0] = 1
        u[0] = 0
        z[0] = 0

        for i in range(1, n - 1):
            l[i] = 2 * (x[i+1] - x[i-1]) - h[i-1]*u[i-1]
            u[i] = h[i] / l[i]
            z[i] = (alpha[i] - h[i-1] * z[i-1]) / l[i]

        l[n-1] = 1
        z[n-1] = 0
        c[n-1] = 0

        for j in range(n-2, -1, -1):
            c[j] = z[j] - u[j]*c[j+1]
            b[j] = ((a[j+1] - a[j]) / h[j]) - (h[j] * (c[j+1] + 2*c[j]) / 3)
            d[j] = (c[j+1] - c[j]) / (3 * h[j])
            print(a[j])

        splines = []
        for i in range(0, n - 1):
            S = []
            S.append(a[i])
            S.append(b[i])
            S.append(c[i])
            S.append(d[i])
            S.append(x[i])
            splines.append(S)

        return splines
        
    def interpolate(self):
        pass

    def make_ranges(self):
        ranges = []
        xs = [point[0] for point in self.points]
        for i in range(len(xs) - 1):
            ranges.append([xs[i], xs[i+1]])
            print(ranges[-1])
        return ranges

cubicSpline = NaturalCubicSplines([(-2, 4), (-1, 1), (0, 0), (1, 1), (2, 4)])
ranges = cubicSpline.make_ranges()

for i in range(len(ranges)):
    print(cubicSpline.splines[i])
