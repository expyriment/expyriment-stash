"""MIDI output.

This module contains a class implementing a MIDI output device.

"""
from __future__ import absolute_import, print_function, division
from builtins import *


__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


from abc import ABC
try:
    from pygame import midi as _midi
    _midi.init()
except:
    _midi = None


class MidiOut(ABC):
    """A class implementing a MIDI output.

    **EXPERIMENTAL!**

    Due to a bug in Pygame's midi module, closing a MidiOut (or the programme)
    will cause an error message. Until this is fixed in Pygame, MidiOut will
    stay in extras.

    """

    def __init__(self, device, latency=0, buffer_size=1024):
        """Create a MIDI output.

        Parameters
        ----------
        device : int or str
            id or name of the MIDI device
        latency : int, optional
            delay in ms applied to timestamp (default=0)
        buffer_size : int, optional
            number of events to be buffered (default=1024)

        """

        from ._midiout import MidiOut
        self.__class__ = MidiOut
        MidiOut.__init__(self, device, latency, buffer_size)

    @staticmethod
    def get_devices():
        """Get a list of all MIDI output devices connected to the system."""

        if _midi is None:
            return
        outdevices = []
        for device_id in range(_midi.get_count()):
            info = _midi.get_device_info(device_id)
            if info[3] == 1:
                outdevices.add([device_id, info[1]])
        return outdevices
