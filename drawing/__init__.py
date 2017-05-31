from math import cos, sin, radians


class Point(object):
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

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


class Square(object):
    def __init__(self, origin=None, size=1, angle=0):
        self.origin = origin or Point()
        self.size = size
        self.angle = angle

    def path(self):
        yield self.top_right_point
        yield self.bottom_right_point
        yield self.bottom_left_point
        yield self.top_left_point
        yield self.top_right_point

    @property
    def _unit_point(self):
        return Point(self.size/2, self.size/2).rotate(self.angle)

    @property
    def top_right_point(self):
        return self._unit_point.translate(self.origin)

    @property
    def bottom_right_point(self):
        return self._unit_point.rotate(90).translate(self.origin)

    @property
    def bottom_left_point(self):
        return self._unit_point.rotate(180).translate(self.origin)

    @property
    def top_left_point(self):
        return self._unit_point.rotate(270).translate(self.origin)

