from nose.tools import *

from drawing.PointSetup import Point
from drawing.Square import Square
from drawing.shaders import WShader


class TestWShader(object):

    def test_wshader_0_line(self):
        s = Square()
        shader = WShader(bounding_box=s, line_count=0)
        point_list = [p for p in shader.path()]
        assert_equal(len(point_list), 0)

    def test_wshader_1_line_has_2_points_on_path(self):
        s = Square()
        shader = WShader(bounding_box=s, line_count=1)
        point_list = [p for p in shader.path()]
        assert_equal(len(point_list), 2)

    def test_wshader_1_line_points_at_both_ends(self):
        s = Square()
        shader = WShader(bounding_box=s, line_count=1)
        point_list = [p for p in shader.path()]
        assert_equal(s.top_left_point, point_list[0])
        assert_equal(s.bottom_right_point, point_list[1])

    def test_wshader_2_line_points_at_both_ends(self):
        s = Square()
        shader = WShader(bounding_box=s, line_count=2)
        point_list = [p for p in shader.path()]
        assert_equal(s.top_left_point, point_list[0])
        assert_equal(s.bottom_line.midpoint(), point_list[1])
        assert_equal(s.top_right_point, point_list[2])

    def test_wshader_reversed(self):
        s = Square()
        shader = WShader(bounding_box=s, line_count=1, reverse=True)
        point_list = [p for p in shader.path()]
        assert_equal(s.bottom_right_point, point_list[0])
        assert_equal(s.top_left_point, point_list[1])

    def test_wshader_v_scale(self):
        s = Square()
        shader = WShader(bounding_box=s, line_count=1, v_scale=2)
        point_list = [p for p in shader.path()]
        assert_equal(Point(-0.5, 1), point_list[0])

