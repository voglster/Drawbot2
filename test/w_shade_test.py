from nose.tools import *
from drawing import Point
from drawing.Square import Square
from drawing.shaders import WShader


class TestWShader(object):
    def test_wshader_starts_and_ends_on_same_y(self):
        s = Square()
        shader = WShader(bounding_box=s, squiggle_count=1, rotation=0)
        point_list = [p for p in shader.path()]
        first_point = point_list[0]
        last_point = point_list[-1]
        assert_almost_equal(first_point.y, last_point.y)
        assert_equal(len(point_list), 3)

    def test_wshader_lvl_2(self):
        s = Square()
        shader = WShader(bounding_box=s, squiggle_count=2, rotation=0)
        point_list = [p for p in shader.path()]
        assert_equal(len(point_list), 5)

    def test_wshader_lvl_3(self):
        s = Square()
        shader = WShader(bounding_box=s, squiggle_count=3, rotation=0)
        point_list = [p for p in shader.path()]
        assert_equal(len(point_list), 7)


