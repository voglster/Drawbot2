class WShader(object):
    def __init__(self, bounding_box, squiggle_count, rotation, starting_point="tl"):
        self.bounding_box = bounding_box
        self.squiggle_count = squiggle_count
        self.rotation = rotation
        self.starting_point = starting_point
        pass

    def path(self):
        top_points = self.bounding_box.top_line.split_into_points(self.squiggle_count+1)
        bottom_points = self.bounding_box.bottom_line.split_into_points(self.squiggle_count+2, False)
        while True:
            yield next(top_points)
            yield next(bottom_points)
