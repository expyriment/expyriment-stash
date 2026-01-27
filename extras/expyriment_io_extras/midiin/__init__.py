
"""MIDI input.

This module contains a class implementing a MIDI input device.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


from abc import ABC


class MidiIn(ABC):
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

        from ._midiin import MidiIn
        return MidiIn.get_devices()

