
"""MIDI input.

This module contains a class implementing a MIDI input device.

"""
from __future__ import absolute_import, print_function, division
from builtins import *

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


try:
    from pygame import midi as _midi
    _midi.init()
except:
    _midi = None


class MidiIn(object):
    """A class implementing a MIDI input.

    **EXPERIMENTAL!**

    Due to a bug in Pygame's midi module, closing a MidiIn (or the programme)
    will cause an error message. Until this is fixed in Pygame, MidiIn will
    stay in extras.

    """

    def __init__(self, device, buffer_size=1024):
        """Create a MIDI input.

        Parameters
        ----------
        device : int or str
            id or name of the MIDI device
        buffer_size : int, optional
            number of events to be buffered (default=1024)

        """

        from ._midiin import MidiIn
        self.__class__ = MidiIn
        MidiIn.__init__(self, device, buffer_size)

    @staticmethod
    def get_devices():
        """Get a list of all MIDI input devices connected to the system."""

        if _midi is None:
            return
        indevices = []
        all_ids = _midi.get_count()
        for device_id in all_ids:
            info = _midi.get_device_info(device_id)
            if info[2] == 1:
                indevices.add([device_id, info[1]])
        return indevices


