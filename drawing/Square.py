from drawing.PointSetup import Point
from drawing.Line import Line
from drawing.util import get_set_dict


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
        self.mirror_x = False
        self.mirror_y = False

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
        return self._get_point("unit", lambda: Point(self.size / 2, self.size / 2).rotate(self.angle))

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

    def mirror(self, param):
        if str(param).lower() == "x":
            self.mirror_x = not self.mirror_x
        if str(param).lower() == "y":
            self.mirror_y = not self.mirror_y
