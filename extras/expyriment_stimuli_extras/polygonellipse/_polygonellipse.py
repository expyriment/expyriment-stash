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


import math as _math

from expyriment.misc import geometry as _geometry
from expyriment.stimuli._shape import Shape


class PolygonEllipse(Shape):
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

        Shape.__init__(self, position=position, colour=colour,
                         anti_aliasing=anti_aliasing)

        self._resolution_factor = resolution_factor
        self._ellipse_size = list(size)
        self._circumference = None
        self._line_with = line_width

        n_vtx = self._default_number_of_vertices * self._resolution_factor
        s = 2 * _math.pi / n_vtx
        w, h = self.ellipse_size
        l = 0
        points = []
        while l < 2 * _math.pi:
            p = _geometry.XYPoint(x = .5 * _math.cos(l) * w + .5 * w,
                              y = .5 * _math.sin(l) * h + .5 * h)
            points.append(p)
            l = l + s
        self._vertices = _geometry.points_to_vertices(points)
        self._update_points()

    @property
    def line_width(self):
        """Getter for line width."""
        return self._line_with

    @property
    def circumference(self):
        """Getter for circumference.

        Notes
        -----
        Calculates the circumference if required. The algorithm for this
        calculation is taken from http://paulbourke.net/geometry/ellipsecirc/
        Ramanujan, Second Approximation

        """

        if self._circumference is None:
            a, b = self._ellipse_size
            h3 = 3 * (_math.pow((a - b), 2) / _math.pow((a + b), 2))
            self._circumference = _math.pi * (a + b) * \
                              (1.0 + h3 / (10.0 + _math.sqrt(4.0 - h3)))
        return self._circumference

    @property
    def ellipse_size(self):
        """Getter for frame_size."""

        return self._ellipse_size

    @property
    def resolution_factor(self):
        """Getter for the resolution."""

        return self._resolution_factor


if __name__ == "__main__":
    from expyriment import control
    control.set_develop_mode(True)
    control.defaults.event_logging = 0
    exp = control.initialize()
    stim = PolygonEllipse(size=(100, 100), line_width=5)
    stim.present()
    exp.clock.wait(2000)
