from nose.tools import *
from drawing.PointSetup import Point
from drawing.Line import Line


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
        distance = midpoint.distance(expected)
        assert_equals(distance, 0)

    def test_split_1_produces_same_line(self):
        p1 = Point()
        p2 = Point(1, 0)
        l = Line(p1, p2)
        lines = list(l.split(1))
        count = sum([1 for _ in lines])
        assert_equals(count, 1)
        assert_equals(l, lines[0])

    def test_as_points_into_3(self):
        p1 = Point()
        p2 = Point(1, 0)
        l = Line(p1, p2)
        points = list(l.as_points(3))
        assert_equals(len(points), 3)
        assert_equals(points[1], Point(0.5, 0))
        assert_equals(points[0], p1)
        assert_equals(points[2], p2)

    def test_as_points_into_2(self):
        p1 = Point()
        p2 = Point(1, 0)
        l = Line(p1, p2)
        points = list(l.as_points(2))
        assert_equals(len(points), 2)
        assert_equals(points[0], p1)
        assert_equals(points[1], p2)

    def test_as_points_into_1(self):
        p1 = Point()
        p2 = Point(1, 0)
        l = Line(p1, p2)
        points = list(l.as_points(1))
        assert_equals(len(points), 1)
        assert_equals(points[0], l.midpoint())




