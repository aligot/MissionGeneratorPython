# coding: utf-8

from Vector3 import Vector3
from EnvironmentalObject import EnvironmentalObject


class Patch(EnvironmentalObject):

    def __init__(self):
        self.Index = None
        self.Type = None
        self.Position = Vector3(0, 0, 0)
        self.Size = None
        self.Color = None
        self.RelationDistance = None

    def GetLowLevelDescription(self):
        return "--tp{0} {1} --sp{0} {2} --cxp{0} {3} --cyp{0} {4} --cp{0} {5} ".format(self.Index, self.Type, self.Size, self.Position.X, self.Position.Y, self.Color)
