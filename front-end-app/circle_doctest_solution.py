import math


class Circle:
    def __init__(self, radius):
        """
        >>> c1 = Circle(2.5)
        >>> c1.radius
        2.5
        """
        self.radius = radius

    def area(self):
        """
        >>> c1 = Circle(2.5)
        >>> c1.area()
        19.63
        """
        return round(math.pi * (self.radius ** 2), 2)

    def circumference(self):
        """
        >>> c1 = Circle(2.5)
        >>> c1.circumference()
        15.71
        """
        return round(2 * math.pi * self.radius, 2)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
