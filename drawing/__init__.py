from math import cos, sin, radians
import drawing.shaders


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

    def __eq__(self, other):
        same_x = self.x == other.x
        same_y = self.y == other.y
        return same_x and same_y


def chain(iterable):
    last = None
    for i in iterable:
        if last is None:
            last = i
            continue
        yield last, i
        last = i


class Line(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def path(self):
        yield self.start
        yield self.end

    def translate(self, vector):
        self.start.translate(vector)
        self.end.translate(vector)
        return self

    def split(self, count=2):
        points = [self.start]
        for i in range(1, count):
            # http://www.dummies.com/education/math/trigonometry/how-to-divide-a-line-segment-into-multiple-parts/
            x = self.start.x + (i/count)*(self.end.x - self.start.x)
            y = self.start.y + (i/count)*(self.end.y - self.start.y)
            points.append(Point(x, y))
        points.append(self.end)
        for p1, p2 in chain(points):
            yield Line(p1, p2)

    def midpoint(self):
        return Point((self.start.x + self.end.x)/2, (self.start.y + self.end.y)/2)

    @property
    def slope(self):
        if not self.delta_y:
            return None
        return self.delta_x / self.delta_y

    @property
    def delta_x(self):
        return self.end.x - self.start.x

    @property
    def delta_y(self):
        return self.end.y - self.start.y


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

    def get_point(self, point_desc):
        point_desc = str(point_desc).lower()
        if point_desc == "tl":
            return self.top_left_point
        if point_desc == "tr":
            return self.top_right_point
        if point_desc == "bl":
            return self.bottom_left_point
        if point_desc == "br":
            return self.bottom_right_point


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

