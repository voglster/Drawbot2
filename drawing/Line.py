from drawing.util import chain
from drawing.PointSetup import Point


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
        points = self.as_points(count + 1)
        for p1, p2 in chain(points):
            yield Line(p1, p2)

    def midpoint(self):
        return Point((self.start.x + self.end.x) / 2, (self.start.y + self.end.y) / 2)

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

    def as_points(self, count_of_points):
        if count_of_points == 1:
            yield self.midpoint()
        else:
            count = count_of_points - 1
            yield self.start
            for i in range(1, count):
                # http://www.dummies.com/education/math/trigonometry/how-to-divide-a-line-segment-into-multiple-parts/
                x = self.start.x + (i/count)*(self.end.x - self.start.x)
                y = self.start.y + (i/count)*(self.end.y - self.start.y)
                yield Point(x, y)
            yield self.end
