# coding: utf-8

import math
from EnvironmentalObject import EnvironmentalObject
from Vector3 import Vector3


class Box(EnvironmentalObject):

    def __init__(self):
        self.Type = None
        self.Index = None
        self.Width = 0.05
        self.Height = 0.05
        self.Length = None
        self.Position = Vector3(0, 0, 0)
        self.Orientation = Vector3(0, 0, 0)
        self.Distribution = None
        self.RelationDistance = 0

    def __str__(self):
        return("Box {} # {} of Length {} and Orientation {}".format(self.Type, self.Index, self.Length, self.Orientation.X))

    def GetARGoSDescription(self):
        return "<box id=\"{}_{}\" size=\"{},{},{}\" movable=\"false\"> <body position=\"{}\" orientation=\"{}\"/> </box>".format(self.Type, self.Index, self.Width, self.Length, self.Height, self.Position, self.Orientation)

    def GetBoundingBox(self):
        # create the perpendicular vectors
        v1 = Vector3(math.cos(math.radians(self.Orientation.X)), math.sin(math.radians(self.Orientation.X)), 0)
        v2 = Vector3(-v1.Y, v1.X, 0)

        # scale the verctors by the dimension of the box
        v1 *= self.Length/2
        v2 *= self.Height/2

        # use the vectors to compute the four corners of the box
        return [self.Position + v1 + v2, self.Position - v1 + v2, self.Position - v1 - v2, self.Position + v1 - v2]
