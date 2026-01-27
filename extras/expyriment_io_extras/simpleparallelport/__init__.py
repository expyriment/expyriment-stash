"""
Input and output parallel port.

This module contains a class implementing parallel port input/output.

"""

__author__ = 'Florian Krause <florian@expyriment.org> \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


from abc import ABC


class SimpleParallelPort(ABC):
    """A class implementing a parallel port input and output.

    Notes
    -----
    CAUTION: Under Windows (starting from 2000) direct I/O is blocked.
    Install http://sourceforge.net/projects/pyserial/files/pyparallel/giveio/

    """

    def __init__(self, port=0):
        """Create a parallel port input and output.

        Parameters:
        -----------
        port : int, optional
            The port to use (default=0).

        """

        from ._simpleparallelport import SimpleParallelPort
        self.__class__ = SimpleParallelPort
        SimpleParallelPort.__init__(self, port)

    @staticmethod
    def get_available_ports():
        """Return an array of strings representing the available parallel ports.

        If pyparallel is not installed, 'None' will be returned.

        Returns
        -------
        ports : list
            array of strings representing the available parallel ports

        """

        from ._simpleparallelport import SimpleParallelPort
        return SimpleParallelPort.get_available_ports()
