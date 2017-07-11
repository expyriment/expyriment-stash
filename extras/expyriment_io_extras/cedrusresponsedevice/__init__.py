"""Cedrus XID response device.

This module contains a class implementing a Cedrus XID response device.

"""
from __future__ import absolute_import, print_function, division
from builtins import *

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


try:
    import pyxid as _pyxid
except:
    _pyxid = None


class CedrusResponseDevice:
    """A class implementing a Cedrus XID response device.

    Notes
    -----
    The CedrusResponseDevice class requires a free Python package for Cedrus
    devices called "pyxid".
    For installation instructions see Expyriment online documentation:
    http://docs.expyriment.org/Hardware.html.
    The class does not use the hardware timer, due to the known bug in the
    Cedrus hardware. Events will be time stamped by Expyriment. Thus, ensure
    constant polling / checking when not using the wait function.

    To install Cedrus resonse device under Linux, you have to set the USB product
    ID. To do so, edit the file /etc/modules and add the following line::

        ftdi_sio vendor=0403 product=f228

    """

    def __init__(self, device_ID=0, error_screen=True):
        """Create a Cedrus Device Input.

        Notes
        -----
        If no Cedrus device is connected, an error text screen will be
        presented informing that the device could not be found and suggesting
        to check the connection and to switch on the device. After keypress the
        class tries to reconnect with the device. Use <q> to quit this
        procedure.

        Parameters
        ----------
        device_id : int, optional
            device ID (default=0). Only required if more than one
            Cedrus Devices are connected.
        error_screen : bool, optional
            set False to switch off the 'device not found' error screen.
            An exception will be raise instead (default=True)

        """

        from ._cedrusresponsedevice import CedrusResponseDevice
        self.__class__ = CedrusResponseDevice
        CedrusResponseDevice.__init__(self, device_ID, error_screen)
