#!/usr/bin/env python

"""
A Line stimulus.

This module contains a class implementing a line stimulus.

"""
from __future__ import absolute_import, print_function, division
from builtins import *


__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


from abc import ABC


class PolygonLine(ABC):
    """A class implementing a line stimulus."""

    def __init__(self, start_position, end_position, line_width, colour=None,
                 anti_aliasing=0):
        """Create a line between two points.

        Parameters
        ----------
        start_position : (int, int)
            start point of the line (x,y)
        end_position : (int, int)
            end point of the line (x,y)
        line_width : int, optional
            width of the plotted line
        colour : (int, int, int), optional
            line colour
        anti_aliasing : int
            anti aliasing parameter (good anti_aliasing with 10) (default=0)

        """

        from ._polygonline import PolygonLine
        self.__class__ = PolygonLine
        PolygonLine.__init__(self, start_position, end_position, line_width,
                             colour, anti_aliasing)
