"""Turbo-Satori network interface.

This module contains a class implementing a network interface for Turbo-Satori
(see www.brainvoyager.com/products/turbosatori.html).

"""
from __future__ import absolute_import, print_function, division
from builtins import *


__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


class TurbosatoriNetworkInterface(object):
    """A class implementing a network interface to Turbo-Satori.

    See http://www.brainvoyager.com/products/turbosatori.html
    for more information.

     """

    def __init__(self, host, port, timeout=2000, connect=True):
        """Create a TurbosatoriNetworkInterface.

        Parameters:
        -----------
        host : str
            The hostname or IPv4 address of the TBV server to connect to.
        port : int
            The port on the Turbo-Satori server to connect to.
        timeout : int, optional
            The maximal time to wait for a response from the server for each
            request (default=2000).
        connect : bool, optional
            If True, connect immediately (default=True).

        """

        from ._turbosatorinetworkinterface import TurbosatoriNetworkInterface
        self.__class__ = TurbosatoriNetworkInterface
        TurbosatoriNetworkInterface.__init__(self, host, port, timeout, connect)
