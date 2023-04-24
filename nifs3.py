import matplotlib.pyplot as pyplot
import numpy

#przepisana metoda, której uczyli na wykładzie z analizy numerycznej na UWr

def h_k(x, k):
    return x[k] - x[k-1]

def lambda_k(x,k):
    h_k_value = h_k(x,k)
    return h_k_value / ( h_k_value + h_k(x, k+1) )   

def diff_quot(x, y):
    n = len(x) - 1
    result = y
    for i in range(1, n+1):
        for j in range(n, i-1, -1):
            result[j] = (result[j] - result[j - 1]) / ( x[j] - x[j-i] )
    return result

def d_k(x,y,k):
    return 6 * diff_quot( x[k - 1 : k + 2], y[k - 1 : k + 2])[-1]

def get_auxilary_pqu(n,x,y):
    p = n * [0]
    q = n * [0]
    u = n * [0]
    for k in range(1,n):
        lambda_k_value = lambda_k(x,k)
        p[k] = lambda_k_value * q[k-1] + 2 
        q[k] = (lambda_k_value - 1) / p[k] 
        u[k] = ( d_k(x,y,k) - lambda_k_value * u[k-1] ) / p[k] 
    return (p,q,u)

def nifs3(x,y): #ta funkcja, zwraca funkcję, do której później podawane są argumenty
    n = len(x) - 1
    p, q, u = get_auxilary_pqu(n,x,y)
    
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
        hk = h_k(x,k)
        return ( 1/ hk * ( #zwracamy wartość nifs3 od danego x dla odpowiedniego przedziału
                1/6 * m_k[k-1] * (x[k] - t)**3 +
                1/6 * m_k[k] * (t - x[k - 1])**3 +
                ( y[k-1] - 1/6 * m_k[k-1] * hk**2) * (x[k] - t) +
                ( y[k] - 1/6 * m_k[k] * hk**2) * (t - x[k-1])
            )
        )
    return s; #zwracamy funkcję

def map_list(f, x): #funkcja, która nakłada działanie jakiejś funkcji na zbiór i zwraca wynik w postaci listy
    return list(map(f,x))

points = [[0, 1.000], #punkty z zadania
[2, 0.830],
[4, 0.685],
[6, 0.559],
[8, 0.439],
[10, 0.344],
[12, 0.254],
[14, 0.184],
[16, 0.127],
[18, 0.077],
[20, 0.045],
[22, 0.025],
[24, 0.010],
[26, 0.005],
[28, 0.0025],
[30, 0.00125]]

xk = []
yk = []

for point in points: #z punktów z zadania wyciagamy iksy i igreki
      xk.append(point[0])
      yk.append(point[1])

l = len(xk)
tk = [k / (l-1) for k in range(0, l)] 

s_x = nifs3(tk, xk) #generujemy nifs3 za pomocą podanych w tresci zadania punktów
s_y = nifs3(tk, yk) #dodatkowa opcja, dla funkcji parametrycznych

m = 10000
u_k = [k/m for k in range(0, m + 1)] #generujemy 10001 punktów, w których obliczymy wartość nifs3, której wzór
                                     #wyznaczylismy w poprzednich linijkach

x = map_list(s_x, u_k) #mapujemy działanie funkcji na argumenty
y = map_list(s_y, u_k)

pyplot.plot(x,y) #rysujemy wykres nifs3
pyplot.scatter(xk, yk) #nanosimy punkty podne w zadaniu (funkcja powinna przez nie przechodzic)
pyplot.show()