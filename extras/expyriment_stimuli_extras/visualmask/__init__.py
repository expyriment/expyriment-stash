#!/usr/bin/env python

"""
A Visual Mask.

This module contains a class implementing a Visual Mask.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'

from abc import ABC


class VisualMask(ABC):
    """A class implementing a visual mask stimulus."""

    def __init__(self, size, position=None, dot_size=(5,5),
                 background_colour=None, dot_colour=None,
                 dot_percentage=50, smoothing=3):
        """Create a visual mask.

        Parameters
        ----------
        size : (int, int)
            size (x, y) of the mask
        position   : (int, int), optional
            position of the mask stimulus
        dot_size : (int, int), optional
            size (x, y) of the dots (default=(5,5))
        background_colour : (int, int), optional
        dot_colour   : (int, int), optional
        dot_percentage : int, optional
            percentage of covered area by the dots (1 to 100) (default=50)
        smoothing : int, optional
            smoothing (default=3)

        """

        from ._visualmask import VisualMask
        self.__class__ = VisualMask
        VisualMask.__init__(self, size, position, dot_size, background_colour,
                            dot_colour, dot_percentage, smoothing)
