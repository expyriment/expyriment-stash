#!/usr/bin/env python

"""
A dotcloud stimulus.

This module contains a class implementing a dotcloud stimulus.

"""
from __future__ import absolute_import, print_function, division
from builtins import *


__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


from abc import ABC


class DotCloud(ABC):
    """A dot cloud class.

    This class creates dots arranged in a circular cloud.

    """

    def __init__(self, radius=None, position=None, background_colour=None,
                 dot_colour=None):
        """Create a dot cloud.

        Parameters
        ----------
        radius : int, optional
            radius of the cloud
        position : (int, int), optional
            position of the stimulus
        background_colour : (int, int, int), optional
            colour of the background
        dot_colour : (int, int, int), optional
            colour of the dots

        """

        from ._dotcloud import DotCloud
        self.__class__ = DotCloud
        DotCloud.__init__(self, radius, position, background_colour,
                          dot_colour)
