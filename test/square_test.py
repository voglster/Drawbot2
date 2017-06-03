from nose.tools import *
from drawing import Point, Line
from drawing.Square import Square


class TestSquare(object):
    def test_path(self):
        s = Square()
        c = sum([1 for i in s.path()])
        assert_equals(c, 5)

    def test_path_starts_and_ends_on_sames_point(self):
        s = Square()
        point_list = [p for p in s.path()]
        assert_is(point_list[0], point_list[-1])

    def test_point_from_string(self):
        s = Square()
        assert_equals(s.top_left_point, s.get_point("tl"))

    def test_points(self):
        s = Square(Point(0, 0), 2)
        top_right_distance = Point(1, 1).distance(s.top_right_point)
        assert_almost_equals(top_right_distance, 0)
        top_left_distance = Point(-1, 1).distance(s.top_left_point)
        assert_almost_equals(top_left_distance, 0)
        bottom_right_distance = Point(1, -1).distance(s.bottom_right_point)
        assert_almost_equals(bottom_right_distance, 0)
        bottom_left_distance = Point(-1, -1).distance(s.bottom_left_point)
        assert_almost_equals(bottom_left_distance, 0)

    def test_bottom_line(self):
        s = Square(Point(0, 0), 2)
        expected = Line(Point(-1, -1), Point(1, -1))
        assert_equal(s.bottom_line, expected)

    def test_top_line(self):
        s = Square(Point(0, 0), 2)
        expected = Line(Point(-1, 1), Point(1, 1))
        assert_equal(s.top_line, expected)

