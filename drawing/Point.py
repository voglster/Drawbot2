from math import radians, cos, sin, sqrt


class Point(object):
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    def rotate(self, angle, center=None):
        # rotate clockwise cause thats how i think
        angle_rad = radians(angle) * -1
        if not center:
            center = Point()
        center.invert()
        self.translate(center)
        x = self.x
        y = self.y
        self.x = x * cos(angle_rad) - y * sin(angle_rad)
        self.y = y * cos(angle_rad) + x * sin(angle_rad)
        center.invert()
        self.translate(center)
        return self

    def translate(self, vector):
        self.x += vector.x
        self.y += vector.y
        return self

    def invert(self):
        self.x *= -1
        self.y *= -1
        return self

    def copy(self):
        return Point(self.x, self.y)

    def distance(self, other):
        delta_x = self.x - other.x
        delta_y = self.y - other.y
        return sqrt(delta_x ** 2 + delta_y ** 2)

    def __eq__(self, other):
        return round(self.x, 7) == round(other.x, 7) and round(self.y, 7) == round(other.y, 7)