class Circle:

    def __init__(self, point, x, y, radius):
        self.point = point
        self.x = x
        self.y = y
        self.radius = radius

    def contains(self):
        distance = ((self.x - self.point.x)**2 + (self.y - self.point.y) **2)**(1/2)
        if distance < self.radius:
            return True
        return False


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


point_1 = Point(15, 5)
circle_1 = Circle(point_1, 5, 10, 10)
print(circle_1.contains())