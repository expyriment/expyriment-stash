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

from types import ModuleType

from expyriment.stimuli._canvas import Canvas
from expyriment.misc import constants

try:
    import numpy as np
except:
    np = None

class GaborPatch(Canvas):
    """A class implementing a Gabor Patch."""

    def __init__(self, position=None,
                 sigma=55,
                 theta=35,
                 lambda_=12.5,
                 phase=0.5,
                 psi=120,
                 gamma=1,
                 background_colour=(127, 127, 127)):
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
            colour of the background, default: (127, 127, 127)

        Notes
        -----
        The background colour of the stimulus depends of the parameters of
        the Gabor patch and can be determined (e.g. for plotting) with the
        property `GaborPatch.background_colour`.

        """

        if not isinstance(np, ModuleType):
            message = """GaborPatch can not be initialized.
The Python package 'Numpy' is not installed."""
            raise ImportError(message)


        sigma_x = sigma
        sigma_y = float(sigma) / gamma

        # Bounding box
        nstds = 3
        theta = theta / 180.0 * np.pi
        xmax = max(abs(nstds * sigma_x * np.cos(theta)), abs(nstds * sigma_y * np.sin(theta)))
        xmax = np.ceil(max(1, xmax))
        ymax = max(abs(nstds * sigma_x * np.sin(theta)), abs(nstds * sigma_y * np.cos(theta)))
        ymax = np.ceil(max(1, ymax))
        xmin = -xmax
        ymin = -ymax
        (x, y) = np.meshgrid(np.arange(xmin, xmax + 1), np.arange(ymin, ymax + 1))
        (y, x) = np.meshgrid(np.arange(ymin, ymax + 1), np.arange(xmin, xmax + 1))

        # Rotation
        x_theta = x * np.cos(theta) + y * np.sin(theta)
        y_theta = -x * np.sin(theta) + y * np.cos(theta)

        pattern = np.exp(-.5 * (x_theta ** 2 / sigma_x ** 2 + y_theta ** 2 / sigma_y ** 2)) * np.cos(
            2 * np.pi / lambda_ * x_theta + psi)

        # make numpy pixel array
        bkg = np.ones((pattern.shape[0], pattern.shape[1], 3)) * \
                                    (np.ones((pattern.shape[1], 3)) * background_colour) #background
        modulation = np.ones((3, pattern.shape[1], pattern.shape[0])) * \
                                    ((255/2.0) * phase * np.ones(pattern.shape) * pattern)  # alpha

        self._pixel_array = bkg + modulation.T
        self._pixel_array[self._pixel_array<0] = 0
        self._pixel_array[self._pixel_array>255] = 255

        # make stimulus
        Canvas.__init__(self, size=pattern.shape, position=position, colour=background_colour)
        self._background_colour = background_colour

    @property
    def background_colour(self):
        """Getter for background_colour"""

        return self._background_colour


    @property
    def pixel_array(self):
        """Getter for pixel_array"""

        return self._pixel_array

    def _create_surface(self):
        """Get the surface of the stimulus.

        This method has to be overwritten for all subclasses individually!

        """

        self.set_surface(self._pixel_array)
        return self._surface

if __name__ == "__main__":
    from expyriment import control, design, misc
    control.set_develop_mode(True)
    control.defaults.event_logging = 0
    exp = design.Experiment(background_colour=misc.constants.C_DARKGREY)
    garbor = GaborPatch(background_colour = exp.background_colour)

    control.initialize(exp)
    garbor.present()
    exp.clock.wait(1000)
