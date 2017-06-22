#!/usr/bin/env python

"""
A dot stimulus.

This module contains a class implementing a dot stimulus.

"""
from __future__ import absolute_import, print_function, division
from builtins import *


__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


class PolygonDot:
    """A class implementing a dot as a child of PolygonEllipse."""

    def __init__(self, radius, position=None, colour=None,
                 resolution_factor=1, anti_aliasing=10):
        """Create a dot.

        Parameters
        ----------
        radius : int
            radius of the dot
        position : int, optional
            position of the stimulus
        colour : (int, int, int), optional
            colour of the dot
        resolution_factor : int, optional
            The resolution_factor increases the resolution of the eclipse.
            The default factor is 1 resulting in 36 points describing the
            ellipse (default=1).
        anti_aliasing : int, optional
            anti aliasing parameter (default=10)

        """

        from ._polygondot import PolygonDot
        self.__class__ = PolygonDot
        PolygonDot.__init__(self, radius, position, colour, resolution_factor,
                            anti_aliasing)
