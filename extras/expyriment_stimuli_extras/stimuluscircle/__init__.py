#!/usr/bin/env python

"""
A stimulus circle stimulus.

This module contains a class implementing a stimulus circle stimulus.

"""
from __future__ import absolute_import, print_function, division
from builtins import *

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


class StimulusCircle(object):
    """A stimulus circle class.

    """

    def __init__(self, radius, stimuli, position=None,
                 background_colour=None):
        """Create a stimulus circle.

        Parameters
        ----------
        radius : int
            radius of the circle
        stimuli : expyriment stimulus
            stimuli to put into the circle
        position : (int, int), optional
            position of the circle
        background_colour : (int, int, int), optional
            background colour of the circle

        """

        from ._stimuluscircle import StimulusCircle
        self.__class__ = StimulusCircle
        StimulusCircle.__init__(self, radius, stimuli, position,
                                background_colour)
