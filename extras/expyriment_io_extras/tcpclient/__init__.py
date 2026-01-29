"""TCP client.

This module contains a class implementing a TCP network client.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'

from abc import ABC


class TcpClient(ABC):
    """A class implementing a TCP network client."""

    def __init__(self, host, port, default_package_size=1024, connect=True):
        """Create a TcpClient.

        Parameters:
        -----------
        host : str
            The hostname or IPv4 address of the server to connect to.
        port : int
            The port to connect to.
        default_package_size : int, optional
            The default size of the packages to be received (default=1024).
        connect : bool, optional
            If True, connect immediately (default=True).

        """

        from ._tcpclient import TcpClient
        self.__class__ = TcpClient
        TcpClient.__init__(self, host, port, default_package_size, connect)
