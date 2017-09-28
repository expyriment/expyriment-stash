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

from expyriment.misc import constants

class GaborPatch:
    """A class implementing a Gabor Patch."""

    def __init__(self, position=None,
                 sigma=55,
                 theta=35,
                 lambda_=12.5,
                 phase=0.5,
                 psi=120,
                 gamma=1,
                 background_colour=constants.C_DARKGREY):
        """Create a Gabor Patch.
        Parameters
        ----------
        position  : (int, int), optional
            position of the mask stimulus
        sigma : int or float, optional
            gaussian standard deviation (in pixels) (default=20)
        theta : int or float, optional
            Grating orientation in degrees (default=35)
        lambda_ : int, optional
            Spatial frequency (pixel per cycle) (default=10)
        phase : float
            0 to 1 inclusive (default=.5)
        psi : int, optional
            0 to 1 inclusive (default=1)
        gamma : float
            0 to 1 inclusive (default=1)
        background_colour : (int,int,int), optional
            colour of the background, default: misc.constants.C_DARKGREY
        Notes
        -----
        The background colour of the stimulus depends of the parameters of
        the Gabor patch and can be determined (e.g. for plotting) with the
        property `GaborPatch.background_colour`.
        """

        from ._gaborpatch import GaborPatch
        self.__class__ = GaborPatch
        GaborPatch.__init__(self, position=position,
                            sigma=sigma, theta=theta, lambda_=lambda_, 
                            phase=phase, psi=psi, gamma=gamma, 
                            background_colour=background_colour)
