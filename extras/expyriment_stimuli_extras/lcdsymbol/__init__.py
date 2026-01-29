#!/usr/bin/env python

"""
A LCD symbol.

This module contains a class implementing a LCD symbol.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'


from abc import ABC


class LcdSymbol(ABC):
    """A LCD symbol class.

    IDs for points and line ::

        Point=      Lines =
        0---1         X-0-X
        |   |         1   2
        2---3         X-3-X
        |   |         4   5
        4---5         X-6-X

    Valid shapes are::

        '0','1','2','3','4','5','6','7','8','9'
        'A','C','E','F','U','H','L','P','h'

    """

    _shapes = {"0":(0, 1, 2, 4, 5, 6),
              "1":(2, 5),
              "2":(0, 2, 3, 4, 6),
              "3":(0, 2, 3, 5, 6),
              "4":(1, 2, 3, 5),
              "5":(0, 1, 3, 5, 6),
              "6":(0, 1, 3, 4, 5, 6),
              "7":(0, 2 , 5),
              "8":(0, 1, 2 , 3 , 4 , 5 , 6),
              "9":(0, 1 , 2 , 3 , 5, 6),
              "A":(0, 1, 2, 3, 4, 5),
              "C":(0, 1, 4, 6),
              "E":(0, 1, 3, 4, 6),
              "F":(0, 1, 3, 4),
              "U":(1, 4, 6, 5, 2),
              "H":(1, 2, 3, 4, 5),
              "L":(1, 4, 6),
              "P":(0, 1, 2, 3, 4),
              "h":(1, 3, 4, 5)
              }

    _lines = ((0, 1), (0, 2), (1, 3), (2, 3), (2, 4), (3, 5), (4, 5))

    def __init__(self, shape, position=None, size=None, colour=None,
                 inactive_colour=None, background_colour=None,
                 line_width=1, gap=5, simple_lines=False):
        """Create a LCD symbol.

        Parameters
        ----------
        shape : list
            shape to show
        position : (int, int), optional
            position to show the symbol
        size : (int, int)
            size of the LCD symbol
        colour : (int, int, int), optional
            LCD symbol colour
        inactive_colour : (int, int, int), optional
            colour of inactive lines
        background_colour : (int, int, int), optional
        line_width : int, optional
            width of the lines (default=1)
        gap :int, optional
            gap between lines (default=5)
        simple_lines : bool, optional
            use simple lines (default=False)

        """

        from ._lcdsymbol import LcdSymbol
        self.__class__ = LcdSymbol
        LcdSymbol.__init__(self, shape, position, size, colour,
                           inactive_colour, background_colour, line_width,
                           gap, simple_lines)
