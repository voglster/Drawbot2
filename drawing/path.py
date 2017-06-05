class Path(object):

    def __init__(self):
        self.data = []

    def add_point(self, point):
        self.data.append(point.copy())

    def path(self):
        for p in self.data:
            yield p

