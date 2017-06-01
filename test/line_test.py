from nose.tools import *
from drawing import Point, Line


class TestLine(object):
    def test_split_produces_2_lines(self):
        p1 = Point()
        p2 = Point(1, 0)
        l = Line(p1, p2)
        lines = l.split()
        count = sum([1 for _ in lines])
        assert_equals(count, 2)

    def test_split_produces_2_lines_with_equal_slope(self):
        p1 = Point()
        p2 = Point(1, 0)
        l = Line(p1, p2)
        lines = list(l.split())
        assert_almost_equals(lines[0].slope, lines[1].slope)

    def test_midpoint(self):
        p1 = Point()
        p2 = Point(1, 0)
        l = Line(p1, p2)
        midpoint = l.midpoint()
        expected = Point((p1.x + p2.x)/2, (p1.y + p2.y)/2)
        assert_equals(midpoint, expected)

