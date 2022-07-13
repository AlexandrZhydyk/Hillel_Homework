class Circle:

    X = 10
    Y = 10
    radius = 10

    def __init__(self, point):
        self.point = point

    def contains(self):
        distance = ((self.X - self.point.x)**2 + (self.Y - self.point.y) **2)**(1/2)
        if distance < self.radius:
            return True
        else:
            return False


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


point_1 = Point(15, 5)
circle_1 = Circle(point_1)
print(circle_1.contains())