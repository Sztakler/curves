class NaturalCubicSplines:
    def __init__(self, points):
        self.points = points

    def h_k(self, x, k):
        return x[k] - x[k-1]

    def lambda_k(self, x,k):
        h_k_value = self.h_k(x,k)
        return h_k_value / ( h_k_value + self.h_k(x, k+1) )   
    
    def diff_quot(self, x, y):
        n = len(x) - 1
        result = y
        for i in range(1, n+1):
            for j in range(n, i-1, -1):
                result[j] = (result[j] - result[j - 1]) / ( x[j] - x[j-i] )
        return result
    
    def d_k(self, x,y,k):
        return 6 * self.diff_quot( x[k - 1 : k + 2], y[k - 1 : k + 2])[-1]
    
    def get_auxilary_pqu(self,n,x,y):
        p = n * [0]
        q = n * [0]
        u = n * [0]
        for k in range(1,n):
            lambda_k_value = self.lambda_k(x,k)
            p[k] = lambda_k_value * q[k-1] + 2 
            q[k] = (lambda_k_value - 1) / p[k] 
            u[k] = ( self.d_k(x,y,k) - lambda_k_value * u[k-1] ) / p[k] 
        return (p,q,u)
        
    def nifs3(self, x,y): #ta funkcja, zwraca funkcję, do której później podawane są argumenty
            n = len(x) - 1
            p, q, u = self.get_auxilary_pqu(n,x,y)
            
            m_k = (n + 1) * [0]
            m_k[n - 1] = u[n - 1]
            for k in range(n - 2, 0, -1):
                m_k[k] = u[k] + q[k] * m_k[k + 1]
        
            def s(t): #funkcja, która będzie zwracana
                def get_section_nr(t): #odszukujemy przedział, na którym chcemy uzyc funkcji interpolacyjnej
                    for i in range(0, n):
                        if(t >= x[i] and t <= x[i+1]):
                            return i + 1;
                    return 1;
                k = get_section_nr(t) #szukamy w jakim przedziale jestesmy
                hk = self.h_k(x,k)
                return ( 1/ hk * ( #zwracamy wartość nifs3 od danego x dla odpowiedniego przedziału
                        1/6 * m_k[k-1] * (x[k] - t)**3 +
                        1/6 * m_k[k] * (t - x[k - 1])**3 +
                        ( y[k-1] - 1/6 * m_k[k-1] * hk**2) * (x[k] - t) +
                        ( y[k] - 1/6 * m_k[k] * hk**2) * (t - x[k-1])
                    )
                )
            return s; #zwracamy funkcję
        
    def map_list(self, f, x): #funkcja, która nakłada działanie jakiejś funkcji na zbiór i zwraca wynik w postaci listy
        return list(map(f,x)) 

    def interpolate(self, ts): 
        xk = []
        yk = []

        for point in self.points: #z punktów z zadania wyciagamy iksy i igreki
              xk.append(point.x)
              yk.append(point.y)

        l = len(xk)
        tk = [k / (l-1) for k in range(0, l)] 

        s_x = self.nifs3(tk, xk) #generujemy nifs3 za pomocą podanych w tresci zadania punktów
        s_y = self.nifs3(tk, yk) #dodatkowa opcja, dla funkcji parametrycznych

        x = self.map_list(s_x, ts)
        y = self.map_list(s_y, ts)

        points = list(zip(x, y))
        return points

