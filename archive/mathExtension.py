import math

pi = math.pi

def sin(x):
    return math.sin(x)

def cos(x):
    return math.cos(x)

class vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return vec2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return vec2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return vec2(self.x * scalar, self.y * scalar)
        else:
            raise ValueError("vec2 multiplication: unknown instance")

    __rmul__ = __mul__
    
    @property
    def normalize(self):
        l = math.sqrt(self.x**2 + self.y**2)
        return vec2(self.x / l, self.y / l)
    
    @property
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    def __repr__(self) -> str:
        return f"[{self.x}, {self.y}]"
    

class vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return vec2(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return vec2(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return vec2(self.x * scalar, self.y * scalar, self.z * scalar)
        else:
            raise ValueError("vec3 multiplication: unknown instance")

    __rmul__ = __mul__
    
    @property
    def normalize(self):
        l = math.sqrt(self.x**2 + self.y**2 + self.z**2)
        return vec2(self.x / l, self.y / l, self.z / l)
    
    @property
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def __repr__(self) -> str:
        return f"[{self.x}, {self.y}, {self.z}]"

