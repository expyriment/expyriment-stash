"""TCP server.

This module contains a class implementing a TCP network server.

"""


__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


from abc import ABC


class TcpServer(ABC):
    """A class implementing a TCP network server for a single client."""

    def __init__(self, port, default_package_size=1024, start_listening=True):
        """Create a TcpServer.

        Parameters:
        -----------
        port : int
            The port to connect to.
        default_package_size : int, optional
            The default size of the packages to be received (default=1024).
        start_listening : bool
            If True, start listening on port immediately (default=True).

        """

        from ._tcpserver import TcpServer
        self.__class__ = TcpServer
        TcpServer.__init__(self, port, default_package_size, connect)
