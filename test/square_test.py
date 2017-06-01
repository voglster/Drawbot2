from nose.tools import *
from drawing import Point, Square


class TestSquare(object):
    def test_path(self):
        s = Square()
        c = sum([1 for i in s.path()])
        assert_equals(c, 5)

    def test_path_starts_and_ends_on_sames_point(self):
        s = Square()
        point_list = [p for p in s.path()]
        assert_equals(point_list[0], point_list[-1])

    def test_point_from_string(self):
        s = Square()
        assert_equals(s.top_left_point, s.get_point("tl"))

    def test_points(self):
        s = Square(Point(0, 0), 2)
        assert_equals(Point(1, 1), s.top_right_point)
        assert_equals(Point(1, 1), s.top_right_point)
        assert_equals(Point(1, 1), s.top_right_point)
        assert_equals(Point(1, 1), s.top_right_point)
