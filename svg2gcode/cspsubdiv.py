#!/usr/bin/env python  
from svg2gcode.bezmisc import *
from svg2gcode.ffgeom import *


def maxdist(a, b, c, d):
    p0x, p0y = a
    p1x, p1y = b
    p2x, p2y = c
    p3x, p3y = d
    p0 = Point(p0x, p0y)
    p1 = Point(p1x, p1y)
    p2 = Point(p2x, p2y)
    p3 = Point(p3x, p3y)

    s1 = Segment(p0, p3)
    return max(s1.distanceToPoint(p1), s1.distanceToPoint(p2))


def cspsubdiv(csp, flat):
    for sp in csp:
        subdiv(sp, flat)


def subdiv(sp, flat, i=1):
    p0 = sp[i - 1][1]
    p1 = sp[i - 1][2]
    p2 = sp[i][0]
    p3 = sp[i][1]

    m = maxdist(p0, p1, p2, p3)
    if m <= flat:
        try:
            subdiv(sp, flat, i + 1)
        except IndexError:
            pass
    else:
        one, two = beziersplitatt(p0, p1, p2, p3, 0.5)
        sp[i - 1][2] = one[1]
        sp[i][0] = two[2]
        p = [one[2], one[3], two[1]]
        sp[i:1] = [p]
        subdiv(sp, flat, i)
