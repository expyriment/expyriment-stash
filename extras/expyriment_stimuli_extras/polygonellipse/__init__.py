#!/usr/bin/env python

"""
An ellipse stimulus.

This module contains a class implementing an ellipse stimulus.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


from abc import ABC


class PolygonEllipse(ABC):
    """A class implementing an ellipse stimulus."""

    _default_number_of_vertices = 36

    def __init__(self, size, position=None, line_width=0, colour=None,
                 resolution_factor=1, anti_aliasing=5):
        """Create an ellipse.

        Parameters
        ----------
        size : (int,int)
            size of the ellipse (x,y)
        position : (int, int, int), optional
            position of the stimulus
        colour  : (int, int, int), optional
            colour of the stimulus
        line_width : int, optional
            if line width is 0, the shape is filled (default=0)
        resolution_factor : int, optional
            The resolution_factor increases the resolution of the eclipse.
            The default factor is 1 resulting in 36 points describing the
            ellipse (default=1)
        anti_aliasing : int, optional
            anti aliasing parameter (default=5)

        """

        from ._polygonellipse import PolygonEllipse
        self.__class__ = PolygonEllipse
        PolygonEllipse.__init__(self, size, position, line_width, colour,
                                resolution_factor, anti_aliasing)
