class WShader(object):
    def __init__(self, bounding_box, squiggle_count, rotation, starting_point="tl"):
        self.bounding_box = bounding_box
        self.squiggle_count = squiggle_count
        self.rotation = rotation
        self.starting_point = starting_point
        pass

    def path(self):
        yield self.bounding_box.top_left_point
