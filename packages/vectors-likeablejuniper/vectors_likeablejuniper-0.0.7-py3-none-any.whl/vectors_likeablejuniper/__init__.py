import math
import types

class Vector:
    """Vector class with basic arithmetic operations:
    - Addition/Subtraction
    - Multiplication with real numbers
    - Dotproduct when multiplying with other vectors (or using dotProduct() from this package)
    - Division with real numbers (and vectors, dividing per component)
    - Comparision with other vectors, comparing per component. If you want to compare magnitudes, use abs()
    - Rotation with Vector.rotate()
    """
    def __init__(self, *args):
        self.components: list[float]
        if len(args) == 1 and isinstance(args[0], (list, tuple, types.GeneratorType)): # If a list containing coordinates is submitted, get the coordinates from that list.
            self.components = list(args[0])
        elif len(args) == 1 and isinstance(args[0], Vector):
            self.components = args[0].components
        else:
            self.components = list(float(args[i]) for i in range(len(args)))
        self.dimensions = len(self.components)
    
    def __repr__(self):
        return f"{[component for component in self.components]}"

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return Vector([i+other for i in self.components])
        elif isinstance(other, (list, tuple)):
            return Vector(self.components[i]+otherVal for i, otherVal in enumerate(other))
        elif isinstance(other, Vector):
            if self.dimensions != other.dimensions:
                raise ValueError("Vector dimensions do not match.")
            return Vector([self.components[i]+other.components[i] for i in range(len(self))])
        else:
            raise ValueError("Added object has incompatible type")
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return Vector([i-other for i in self.components])
        elif isinstance(other, Vector):
            if self.dimensions != other.dimensions:
                raise ValueError(f"Vector dimensions do not match. {self.dimensions, other.dimensions}")
            return Vector([self.components[i]-other.components[i] for i in range(len(self))])
        else:
            raise ValueError("Subtracted object has incompatible type")
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector([i*other for i in self.components])
        elif isinstance(other, Vector):
            return dotProduct(self, other)
        else:
            raise ValueError("Multiplied object has incompatible type")
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Vector([self.components[i]/other for i in range(len(self))])
        elif isinstance(other, Vector):
            if self.dimensions != other.dimensions:
                raise ValueError("Vector dimensions do not match.")
            return Vector([self.components[i]/other.components[i] for i in range(len(self))])
        else:
            raise ValueError("Divided object has incompatible type")
    
    def __lt__(self, other) -> bool:
        if isinstance(other, (int, float)):
            return not any(self.components[i] >= other for i in range(len(self)))
        elif isinstance(other, Vector):
            return not any(self.components[i] >= other.components[i] for i in range(len(self)))
        else:
            return False
    
    def __le__(self, other) -> bool:
        if isinstance(other, (int, float)):
            return not any(self.components[i] > other for i in range(len(self)))
        elif isinstance(other, Vector):
            return not any(self.components[i] > other.components[i] for i in range(len(self)))
        else:
            return False
    
    def __gt__(self, other) -> bool:
        if isinstance(other, (int, float)):
            return not any(self.components[i] <= other for i in range(len(self)))
        elif isinstance(other, Vector):
            return not any(self.components[i] <= other.components[i] for i in range(len(self)))
        else:
            return False

    def __ge__(self, other) -> bool:
        if isinstance(other, (int, float)):
            return not any(self.components[i] < other for i in range(len(self)))
        elif isinstance(other, Vector):
            return not any(self.components[i] < other.components[i] for i in range(len(self)))
        else:
            return False
    
    def __eq__(self, other) -> bool:
        if isinstance(other, (int, float)):
            return not any(self.components[i] != other for i in range(len(self)))
        elif isinstance(other, Vector):
            return not any(self.components[i] != other.components[i] for i in range(len(self)))
        else:
            return False
    
    def __abs__(self):
        return math.sqrt(sum(i**2 for i in self.components))
    
    def __setitem__(self, key: int, value: float):
        self.components[key] = value
    
    def __getitem__(self, key: int):
        return self.components[key]

    def __len__(self):
        return self.dimensions
    
    def direction(self):
        if self.dimensions != 2:
            raise ValueError("Can only calculate direction of 2-dimensional Vector, not {}-dimensional.".format(self.dimensions))
        if self[1] >= 0:
            return math.acos(self[0] / abs(self))
        else:
            return math.pi*2 - math.acos(self[0] / abs(self))
    
    def rotatePygame(self, angle=0, rotateTo=0):
        """Rotates the current vector and returns it (note that rotation permanently affects this object)"""
        if not rotateTo:
            rotateTo = self.direction() + angle
        length = abs(self)
        self.components = [math.cos(rotateTo) * length, -1 * math.sin(rotateTo) * length]
        return self

    def rotate(self, angle: float=0, rotateTo: float=0):
        """Rotates the current vector and returns it (note that rotation permanently affects this object). Only supports 2D."""
        if not self.dimensions == 2:
            raise ValueError("Vector must have exactly 2 dimensions to be rotated")
        if not rotateTo:
            rotateTo = self.direction() + angle
        length = abs(self)
        self.components = [math.cos(rotateTo) * length, math.sin(rotateTo) * length]
        return self
    
    def clone(self):
        return Vector(self.components)


def dotProduct(v1 : Vector, v2 : Vector):
    if v1.dimensions != v2.dimensions:
        raise ValueError("Vector dimensions do not match.")
    return sum([v1.components[i]*v2.components[i] for i in range(v1.dimensions)])

def angleBetween(v1: Vector, v2: Vector, format="rad"):
    if v1.dimensions != v2.dimensions:
        raise ValueError("Vector dimensions do not match.")
    return math.acos(dotProduct(v1, v2)/(abs(v1)*abs(v2))) * ((180/math.pi) if format == "deg" else 1)

def customRound(num, roundTo=0.01):
    return (round(num/roundTo))*roundTo
