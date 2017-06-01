from PIL import Image, ImageEnhance
import numpy as np
from drawing import Point, Line


class DBImageConverter(object):
    def __init__(self, file):
        self.thumbsize = 180
        self.raw_image = Image.open(file)
        self.raw_image.thumbnail((self.thumbsize, self.thumbsize))
        self.raw_image = self.raw_image.convert("L")
        enhancer = ImageEnhance.Contrast(self.raw_image)
        self.raw_image = enhancer.enhance(2)
        self.shader()

    def as_array(self):
        return np.asarray(self.raw_image.getdata(), dtype=np.float64).reshape(
            (self.raw_image.size[1], self.raw_image.size[0]))

    def shader(self, shades=10):
        shades -= 1
        ary = self.as_array()
        for x, row in enumerate(ary):
            for y, pixel in enumerate(row):
                ary[x, y] = int(int(pixel * (shades / 255.0)) * (255.0 / shades))
        self.raw_image = Image.fromarray(np.uint8(ary))

    @property
    def pixels(self):
        reverse = False
        for y, row in enumerate(self.as_array()):
            for x, pixel in (reversed([q for q in enumerate(row)]) if reverse else enumerate(row)):
                yield (x - (self.thumbsize / 2), y, pixel, reverse)
            reverse = not reverse

    def show(self):
        self.raw_image.show()


def getImage(path):
    dbic = DBImageConverter(path)
    dbic.show()
    #input("Waiting ctrl-c to abort")
    return dbic


def setup(dbic):
    class Conf:
        pass

    conf = Conf()
    conf.canvas_size = 200
    conf.pixel_size = 1.0 * conf.canvas_size / dbic.thumbsize
    conf.vert_line_size = conf.pixel_size * 0.9
    conf.vert_offset = (conf.pixel_size - conf.vert_line_size) / 2.0
    return conf


def lines(data, conf, shades=10.0):
    shades -= 1
    x, y, pixel, reverse = data
    pixel = 255 - pixel  # invert the color 255 is now black and 0 is white

    pixel = int(pixel * (shades / 255.0))

    x = x * conf.pixel_size
    y = y * conf.pixel_size
    if pixel:
        increment = conf.pixel_size / pixel

        lst = [i for i in range(0, pixel)]
        if reverse:
            lst = reversed(lst)
        swap = False
        start_point = None

        for idx in lst:
            start_point = start_point or Point(str(round(x + (idx * increment), 4)), str(round(y + conf.vert_offset, 4)))
            end_point = Point(str(round(x + (idx * increment), 4)), str(round(y + conf.vert_offset + conf.vert_line_size, 4)))
            if swap:
                yield Line(start_point, end_point)
                start_point = end_point
            else:
                yield Line(end_point, start_point)




def gcode_lines(pixels, conf):
    for i in pixels:
        for g in lines(i, conf):
            yield g




