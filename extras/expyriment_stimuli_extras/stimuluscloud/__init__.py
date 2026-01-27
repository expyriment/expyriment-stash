#!/usr/bin/env python

"""
A stimulus cloud stimulus.

This module contains a class implementing a stimulus cloud stimulus.

"""

__author__ = 'Florian Krause <florian@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


from abc import ABC


class StimulusCloud(ABC):
    """A stimulus cloud class.

    This class produces a cloud of ANY visual stimuli.
    The cloud will be of rectengular shape!

    """

    def __init__(self, size=None, position=None, background_colour=None):
        """Create a stimulus cloud.

        Parameters
        ----------
        size : (int, int), optional
            size of the cloud
        position : (int, int), optional
            position of the cloud
        background_colour : (int, int, int), optional
            colour of the background

        """

        from ._stimuluscloud import StimulusCloud
        self.__class__ = StimulusCloud
        StimulusCloud.__init__(self, size, position, background_colour)
