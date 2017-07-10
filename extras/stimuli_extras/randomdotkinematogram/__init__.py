#!/usr/bin/env python

"""
A random dot kinematogram (stimulus-like).

This module contains a class implementing a random dot kinematogram.

"""
from __future__ import absolute_import, print_function, division
from builtins import *


__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


class RandomDotKinematogram:
    """Random Dot Kinematogram"""

    def __init__(self, area_radius, n_dots, target_direction,
                 target_dot_ratio, position=None, dot_speed=100,
                 dot_lifetime=400, dot_radius=3, dot_colour=None,
                 background_colour=None, north_up_clockwise=True):
        """Create a Random Dot Kinematogram

        Parameters:
        -----------
        area_radius : int
            the radius of the stimulus area
        n_dots : int
            number of moving dots
        target_direction : int, float (0-360)
            movement target direction in degrees
        target_dot_ratio : float (0-1)
            ratio of dots that move consistently in the same target direction
            (the rest of the target moves in a random direction)
            can be sometimes only approximated! self.target_dot_ratio returns the
            precise actual target dot ratio
        position : (int, int), optional
            position of the stimulus
        dot_speed : int, optional
            the moving speed in pixel per second (default=100)
        dot_lifetime : int, optional
            the time the object lives in milliseconds (default=400)
        dot_radius : int, optional
            radius of the dots (default=3)
        dot_colour : (int, int, int), optional
            colour (RGB) of the dots (default=experiment.foreground_colour)
        background_colour : (int, int, int), optional
            colour (RGB) of the background (default=experiment.background_colour)
        north_up_clockwise : bool, optional
            if true (default) all directional information refer to an
            north up and clockwise system
            otherwise 0 is right, counterclockwise (default=True)

        Notes:
        ------
        Logging is switch off per default

        """

        from ._randomdotkinematogram import RandomDotKinematogram
        self.__class__ = RandomDotKinematogram
        RandomDotKinematogram.__init__(self, area_radius, n_dots,
                                       target_direction, target_dot_ratio,
                                       position, dot_speed, dot_lifetime,
                                       dot_radius, dot_colour,
                                       background_colour, north_up_clockwise)
