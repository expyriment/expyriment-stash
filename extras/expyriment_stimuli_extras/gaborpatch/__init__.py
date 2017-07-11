#!/usr/bin/env python

"""
A Gabor patch stimulus.

This module contains a class implementing a Gabor patch stimulus.

"""
from __future__ import absolute_import, print_function, division
from builtins import *

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


class GaborPatch:
    """A class implementing a Gabor Patch."""

    def __init__(self, size=300, position=None, lambda_=10, theta=15,
                sigma=20, phase=.25, trim=.005):
        """Create a Gabor Patch.

        Parameters
        ----------
        size : (int, int), optional
            size (x, y) of the mask (default=300)
        position  : (int, int), optional
            position of the mask stimulus
        lambda_ : int, optional
            Spatial frequency (pixel per cycle) (default=10)
        theta : int or float, optional
            Grating orientation in degrees (default=15)
        sigma : int or float, optional
            gaussian standard deviation (in pixels) (default=20)
        phase : float
            0 to 1 inclusive (default=.25)
        trim : float
            trim off Gaussian values smaller than this (default=.005)

        Notes
        -----
        The background colour of the stimulus depends of the parameters of
        the Gabor patch and can be determined (e.g. for plotting) with the
        property `GaborPatch.background_colour`.

        """

        from ._gaborpath import GaborPath
        self.__class__ = GaborPatch
        GaborPatch.__init__(self, size, position, lambda_, theta, sigma,
                            phase, trim)
