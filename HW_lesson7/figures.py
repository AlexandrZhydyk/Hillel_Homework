import math


class Shape:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def square(self):
        return 0


class Circle(Shape):

    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius

    def square(self):
        return math.pi * self.radius ** 2


class Rectangle(Shape):

    def __init__(self, x, y, height, width):
        super().__init__(x, y)
        self.height = height
        self.width = width

    def square(self):
        return self.width * self.height


class Parallelogram(Rectangle):

    def __init__(self, x, y, height, width, angle):
        super().__init__(x, y, height, width)
        self.angle = angle
        self.figure_name = self.__class__.__name__

    def print_angle(self):
        print(self.angle)

    def __str__(self):
        result = super().__str__()
        return result + f'\n{self.figure_name}: {self.width}, {self.height}, {self.angle}'

    def square(self):
        return super().square() * math.sin(self.angle)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

class Triangle(Parallelogram):
    def __init__(self, x, y, height, width, angle):
        super().__init__(x, y, height, width, angle)

    def print_angle(self):
        print(self.angle)

    def square(self):
        return super().square() * (1/2)

    def __str__(self):
        return super().__str__()

    def __eq__(self):
        return super.__eq__(self)


class Scene:
    def __init__(self):
        self._figures = []

    def add_figure(self, figure):
        self._figures.append(figure)

    def total_square(self):
        return round(sum(f.square() for f in self._figures), 2)

    def __str__(self):
        pass


r = Rectangle(0, 0, 10, 20)
r1 = Rectangle(10, 0, -10, 20)
r2 = Rectangle(0, 20, 100, 20)

c = Circle(10, 0, 10)
c1 = Circle(100, 100, 5)

p = Parallelogram(1, 2, 20, 30, 45)
print(p.x)
p1 = Parallelogram(1, 2, 20, 30, 45)
print(p1)

tr = Triangle(1, 2, 20, 30, 45)

scene = Scene()
scene.add_figure(r)
scene.add_figure(r1)
scene.add_figure(r2)
scene.add_figure(c)
scene.add_figure(c1)
scene.add_figure(tr)

print(tr)
print(scene.total_square())
