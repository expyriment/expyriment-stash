#!/usr/bin/env python

"""
The noise tone stimulus module.

This module contains a class implementing a noise tone stimulus.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


from abc import ABC


class NoiseTone(ABC):
    """A class implementing a noise tone stimulus."""

    def __init__(self, duration, samplerate=44100, bitdepth=16,
                 amplitude=0.5):
        """Create a noise tone.

        Parameters
        ----------
        duration : int
            duration of the noise tone in ms
        samplerate : int, optional
            samplerate of the noise tone (default=44100)
        bitdepth : int, optional
            bitdeth of the noise tone (default=16)
        amplitude : int, optional
            amplitude of the noise tone (default=0.5)

        """

        from ._noisetone import NoiseTone
        self.__class__ = NoiseTone
        NoiseTone.__init__(self, duration, samplerate, bitdepth, amplitude)
