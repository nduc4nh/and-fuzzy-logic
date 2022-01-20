def trapezoid(a, b, c, d):
    def func(x):
        if x <= a:
            return 0
        elif x <= b:
            return (x - a) / (b - a)
        elif x <= c:
            return 1
        elif x <= d:
            return (d - x) / (d - c)
        else:
            return 0

    return func


def triangular(a, b, c):
    def func(x):
        if x <= a:
            return 0
        elif x <= b:
            return (x - a) / (b - a)
        elif x <= c:
            return (c - x) / (c - b)
        else:
            return 0
    return func

class Shape:
    def __init__(self) -> None:
        self.mf = None
        pass

    def get_area(self):
        pass 

    def get_centroid(self):
        pass

class Trapzoid(Shape):
    def __init__(self, a,b,c,d) -> None:
        super().__init__()
        self.mf = trapezoid(a,b,c,d)
        self.ranges = [a,b,c,d]
        self.a = a
        self.b = b
        self.c = c
        self.d = d
    
    def get_area(self, h = 1):
        return ((self.d - self.a) + (self.c - self.b)) * h / 2

    def get_centroid(self):
        return sum(self.ranges) / 4 
    
    def get_fuzzy_value(self,x):
        return self.mf(x)

    def fit_shape(self,value):
        c = value * (self.b - self.a) + self.a 
        d = self.d - value * (self.d - self.c)
        return Trapzoid(self.a,c,d,self.d)
        
