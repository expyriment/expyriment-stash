#!/usr/bin/env python

"""
A stimulation protocol.

This module contains a class implementing a stimulation protocol.

"""
__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


from abc import ABC


class StimulationProtocol(ABC):
    """A class implementing a stimulation protocol."""

    def __init__(self, unit):
        """Create a stimulation protocol.

        Parameters
        ----------

        unit : str
            The unit of the stimulation protocol ('time' or 'volume')

        """

        from ._stimulationprotocol import StimulationProtocol
        self.__class__ = StimulationProtocol
        StimulationProtocol.__init__(self, unit)
