from PIL import Image, ImageEnhance
import numpy as np
from drawing.PointSetup import Point
from drawing.Square import Square
from drawing.shaders import WShader


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
    return dbic


def setup(dbic):
    class Conf:
        pass

    conf = Conf()
    conf.canvas_size = 300
    conf.pixel_size = 1.0 * conf.canvas_size / dbic.thumbsize
    return conf


def lines(data, conf, shades=10.0):
    shades -= 1
    x, y, pixel, reverse = data
    pixel = 255 - pixel  # invert the color 255 is now black and 0 is white

    pixel = int(pixel * (shades / 255.0))
    pixel = pixel - 2
    if pixel < 0:
        pixel = 0

    if pixel:
        x = x * conf.pixel_size
        y = y * conf.pixel_size

        center = Point(x + conf.pixel_size/2, y + conf.pixel_size/2)
        bounding_box = Square(origin=center, size=conf.pixel_size)

        return WShader(bounding_box=bounding_box, line_count=pixel, reverse=reverse, v_scale=0.8)


def gcode_lines(pixels, conf):
    for i in pixels:
        yield lines(i, conf, 8)




