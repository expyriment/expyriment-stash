#!/usr/bin/env python

"""
A thermometer display stimulus.

This module contains a class implementing a thermometer display stimulus.

"""
from __future__ import absolute_import, print_function, division
from builtins import *


__author__ = 'Florian Krause <florian@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


class ThermometerDisplay(object):
    """A class implementing a thermometer display."""

    def __init__(self, state, goal=None, size=(128,340), nr_segments=10,
                 gap=3, frame_line_width=20, active_colour=(150,150,150),
                 inactive_colour=(0,0,0), frame_colour=(100,100,100),
                 goal_colour=(0,255,0), gap_colour=(255,255,255),
                 position=None):
        """Initializing a thermometer display.

        Parameters:
        -----------
        state : int
            The state of the thermometer in percent.
        goal : int, optional
            The goal state indication in percent.
        size : (int, int), optional
            The size of the thermometer display (default=(128,340)).
        nr_segments : int, optional
            The number of segments to use (default=10).
        gap : int, optional
            The visual gap between the individual segments (default=3).
        frame_line_width : int, optional
            The line width of the frame around the thermometer display
            (default=20).
        active_colour : (int, int, int), optional
            The colour of the active segments (default=(150,150,150)).
        inactive_colour : (int, int, int), optional
            The colour of the inactive segments (default=(0,0,0)).
        frame_colour : (int, int, int), optional
            The colour of the frame around the thermometer display
            (default=(100,100,100)).
        goal_colour : (int, int, int), optional
            The colour of the goal indicator (default=(0,255,0)).
        gap_colour : (int, int, int), optional
            The gap colour of the thermometer stimulus
            (default=(255,255,255)).
        position : (int, int), optional
            The position of the thermometer display.
        """

        from ._thermometerdisplay import ThermometerDisplay
        self.__class__ = ThermometerDisplay
        ThermometerDisplay.__init__(self, state, goal, size, nr_segments, gap,
                                    frame_line_width, active_colour,
                                    inactive_colour, frame_colour,
                                    goal_colour, gap_colour, position)
