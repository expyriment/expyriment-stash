#!/usr/bin/env python

"""
A Rectangle stimulus.

This module contains a class implementing a rectangle stimulus.

"""
from __future__ import absolute_import, print_function, division
from builtins import *

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


class PolygonRectangle:
    """A class implementing a rectangle stimulus."""

    def __init__(self, size, position=None, colour=None, anti_aliasing=0):
        """Create a filled rectangle.

        Parameters
        ----------
        size : (int, int)
            size (width, height) of the Rectangle
        position : (int, int), optional
            position of the stimulus
        colour   : (int, int, int), optional
            colour of the rectangle
        anti_aliasing : int, optional
            anti aliasing parameter (default=0)

        """

        from ._polygonrectangle import PolygonRectangle
        self.__class__ = PolygonRectangle
        PolygonRectangle.__init__(self, size, position, colour, anti_aliasing)
