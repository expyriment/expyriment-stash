"""
Input and output parallel port.

This module contains a class implementing parallel port input/output.

"""
from __future__ import absolute_import, print_function, division
from builtins import *

__author__ = 'Florian Krause <florian@expyriment.org> \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


try:
    import parallel
except:
    parallel = None


class SimpleParallelPort:
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

        if not isinstance(parallel, ModuleType):
            return None
        ports = []
        if platform.startswith("linux"): #for Linux operation systems
            dev = listdir('/dev')
            for p in dev:
                if p.startswith("parport"):
                    ports.append(p)
        elif platform == "dawin": #for MacOS
            pass
        else: #for windows, os2
            for p in range(256):
                try:
                    p = parallel.Parallel(p)
                    ports.append("LTP{0}".format(p + 1))
                except:
                    pass
        ports.sort()

        return ports


