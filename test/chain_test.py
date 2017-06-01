from nose.tools import *
from drawing import chain


def test_chain_groups_2_items():
    l = [1, 2]
    val = list(chain(l))
    assert_equals(len(val), 1)


def test_chain_groups_1_items():
    l = [1]
    val = list(chain(l))
    assert_equals(len(val), 0)


def test_chain_groups_3_items():
    l = [1, 2, 3]
    val = list(chain(l))
    assert_equals(len(val), 2)


def test_chain_connections():
    l = [1, 2, 3]
    val = chain(l)
    first = next(val)
    second = next(val)
    assert_equals(first[1], second[0])

