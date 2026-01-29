#!/usr/bin/env python

"""
A Rectangle stimulus.

This module contains a class implementing a rectangle stimulus.

"""


__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'

from expyriment.stimuli._shape import Shape


class PolygonRectangle(Shape):
    """A class implementing a rectangle stimulus."""

    def __init__(self, size, position=None, colour=None, anti_aliasing=0):
        """Create a filled rectangle.

        Parameters
        ----------
        size : (int, int)
            size (width, height) of the Rectangle
        position : (int, int), optional
            position of the stimulus
        colour   : (int, int, int), optional
            colour of the rectangle
        anti_aliasing : int, optional
            anti aliasing parameter (default=0)

        """

        Shape.__init__(self, position=position, colour=colour,
                        anti_aliasing=anti_aliasing)
        self.add_vertex((size[0], 0))
        self.add_vertex((0, size[1]))
        self.add_vertex((-size[0], 0))



if __name__ == "__main__":
    from expyriment import control, stimuli
    control.set_develop_mode(True)
    control.defaults.event_logging = 0
    exp = control.initialize()
    cnvs = stimuli.Rectangle((20, 200), colour=(255, 0, 255))
    cnvs.present()
    exp.clock.wait(1000)
