from math import cos, sin, radians, sqrt
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

    def distance(self, other):
        delta_x = self.x - other.x
        delta_y = self.y - other.y
        return sqrt(delta_x ** 2 + delta_y ** 2)

    def __eq__(self, other):
        return round(self.x, 7) == round(other.x, 7) and round(self.y, 7) == round(other.y, 7)


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
        points = self.split_into_points(count+1)
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

    def __eq__(self, other):
        first_points_match = self.start == other.start
        second_points_match = self.end == other.end
        return first_points_match and second_points_match

    def split_into_points(self, count_of_points, include_ends=True):
        count = count_of_points - 1
        if include_ends:
            yield self.start
        for i in range(1, count):
            # http://www.dummies.com/education/math/trigonometry/how-to-divide-a-line-segment-into-multiple-parts/
            x = self.start.x + (i/count)*(self.end.x - self.start.x)
            y = self.start.y + (i/count)*(self.end.y - self.start.y)
            yield Point(x, y)
        if include_ends:
            yield self.end


def get_set_dict(dictionary, key, factory):
    if key not in dictionary:
        dictionary[key] = factory()
    return dictionary[key]


class Square(object):
    def __init__(self, origin=None, size=1, angle=0):
        self.origin = origin or Point()
        self.size = size
        self.angle = angle
        self._points = {}
        self._bl = None
        self._tl = None
        self._point_lookup = {
            "tl": self.top_left_point,
            "tr": self.top_right_point,
            "bl": self.bottom_left_point,
            "br": self.bottom_right_point,
        }

    def path(self):
        yield self.top_right_point
        yield self.bottom_right_point
        yield self.bottom_left_point
        yield self.top_left_point
        yield self.top_right_point

    def get_point(self, point_desc):
        point_desc = str(point_desc).lower()
        return self._point_lookup[point_desc]

    def _get_point(self, name, func):
        return get_set_dict(self._points, name, func)

    @property
    def _unit_point(self):
        return self._get_point("unit", lambda: Point(self.size/2, self.size/2).rotate(self.angle))

    @property
    def top_right_point(self):
        return self._get_point("tr", lambda: self._unit_point.copy().translate(self.origin))

    @property
    def bottom_right_point(self):
        return self._get_point("br", lambda: self._unit_point.copy().rotate(90).translate(self.origin))

    @property
    def bottom_left_point(self):
        return self._get_point("bl", lambda: self._unit_point.copy().rotate(180).translate(self.origin))

    @property
    def top_left_point(self):
        return self._get_point("tl", lambda: self._unit_point.copy().rotate(270).translate(self.origin))
    
    @property
    def bottom_line(self):
        self._bl = self._bl or Line(self.bottom_left_point, self.bottom_right_point)
        return self._bl

    @property
    def top_line(self):
        self._tl = self._tl or Line(self.top_left_point, self.top_right_point)
        return self._tl
