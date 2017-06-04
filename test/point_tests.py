from nose.tools import *
from drawing.PointSetup import Point


class TestPoint(object):
    def test_rotation_about_origin(self):
        p = Point(0, 1)
        p.rotate(90)
        assert_almost_equals(p.x, 1)
        assert_almost_equals(p.y, 0)

    def test_translate(self):
        p = Point(0, 0)
        vec = Point(1, 1)
        p.translate(vec)
        assert_almost_equals(p.x, 1)
        assert_almost_equals(p.y, 1)

    def test_invert(self):
        p = Point(1, 1)
        p.invert()
        assert_almost_equals(p.x, -1)
        assert_almost_equals(p.y, -1)

    def test_copy(self):
        p = Point(1, 1)
        p_copy = p.copy()
        assert_almost_equals(p.x, p_copy.x)
        assert_almost_equals(p.y, p_copy.y)

    def test_rotate_about_other_point(self):
        p = Point(0, 0)
        other_point = Point(0, -1)
        p.rotate(90, other_point)
        assert_almost_equals(p.x, 1)
        assert_almost_equals(p.y, -1)

    def test_distance(self):
        p1 = Point(0, 0)
        p2 = Point(0, 0)
        distance = p1.distance(p2)

        assert_equals(distance, 0)

