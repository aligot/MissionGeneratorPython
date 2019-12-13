# coding: utf-8

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

    def GetARGoSDescription(self):
        return "<box id=\"{}_{}\" size=\"{},{},{}\" movable=\"false\"> <body position=\"{}\" orientation=\"{}\"/> </box>".format(self.Type, self.Index, self.Width, self.Length, self.Height, self.Position, self.Orientation)
