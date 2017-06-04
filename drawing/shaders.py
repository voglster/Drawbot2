from drawing.PointSetup import Point


class WShader(object):
    def __init__(self, bounding_box, line_count, reverse=False, v_scale=1):
        self.bounding_box = bounding_box
        self.line_count = line_count
        self.reverse = reverse
        self.v_scale = v_scale

    def path(self):
        if self.line_count == 0:
            yield None
        else:
            ends_on_top = self.line_count % 2 == 0
            if ends_on_top:
                top_points = [p.copy() for p in self.bounding_box.top_line.as_points(self.line_count)]
                bottom_points = [p.copy() for p in self.bounding_box.bottom_line.as_points(self.line_count + 1)][1:-1]
            else:
                top_points = [p.copy() for p in self.bounding_box.top_line.as_points(self.line_count + 1)][:-1]
                bottom_points = [p.copy() for p in self.bounding_box.bottom_line.as_points(self.line_count + 1)][1:]

            change = ((self.bounding_box.size * self.v_scale) - self.bounding_box.size) / 2

            if change:
                for p in top_points:
                    p.translate(Point(0, change))
                for p in bottom_points:
                    p.translate(Point(0, change * -1))

            q = []
            while top_points:
                q.append(top_points.pop(0))
                if bottom_points:
                    q.append(bottom_points.pop(0))
            if self.reverse:
                q.reverse()
            for p in q:
                yield p
