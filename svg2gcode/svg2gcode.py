#!/usr/bin/env python

import sys
import xml.etree.ElementTree as ET
import svg2gcode.shapes as shapes_pkg
from drawing.PointSetup import Point
from drawing.path import Path
from svg2gcode.shapes import point_generator
from svg2gcode.config import *


def generate_paths(file_as_string):
    svg_shapes = {'rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path'}

    tree = ET.ElementTree(ET.fromstring(file_as_string))
    root = tree.getroot()

    width = root.get('width')
    height = root.get('height')
    if width is None or height is None:
        view_box = root.get('viewBox')
        if view_box:
            _, _, width, height = view_box.split()

    if width is None or height is None:
        print("Unable to get width and height for the svg")
        sys.exit(1)

    numeric = '0123456789-.'
    for i, c in enumerate(width):
        if c not in numeric:
            break
    width = width[:i]
    for i, c in enumerate(height):
        if c not in numeric:
            break
    height = height[:i]

    width = float(width)
    height = float(height)

    scale_x = bed_max_x / max(width, height)
    scale_y = bed_max_y / max(width, height)

    for elem in root.iter():
        try:
            _, tag_suffix = elem.tag.split('}')
        except ValueError:
            continue

        if tag_suffix in svg_shapes:
            shape_class = getattr(shapes_pkg, tag_suffix)
            shape_obj = shape_class(elem)
            d = shape_obj.d_path()
            m = shape_obj.transformation_matrix()

            if d:
                path = Path()
                p = point_generator(d, m, smoothness)
                for x, y in p:
                    #x = scale_x * x
                    #y = scale_y * y
                    if 0 < x < bed_max_x and 0 < y < bed_max_y:
                        path.add_point(Point(x, y))
                yield path
