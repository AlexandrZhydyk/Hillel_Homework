class Circle:

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def __contains__(self, item):
        distance = ((self.x - item.x)**2 + (self.y - item.y) ** 2)**(1/2)
        if distance < self.radius:
            return True
        return False


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


point_1 = Point(15, 5)
circle_1 = Circle(10, 10, 10)
print(point_1 in circle_1)
