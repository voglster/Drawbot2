from nose.tools import *
from drawing import Point, Square


class TestSquare(object):
    def test_path(self):
        s = Square()
        c = sum([1 for i in s.path()])
        assert_equals(c, 5)
