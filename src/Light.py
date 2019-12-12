# coding: utf-8

from Vector3 import Vector3
from EnvironmentalObject import EnvironmentalObject


class Light(EnvironmentalObject):

    def __init__(self):
        self.Status = None
        self.Position = None

    def GetLowLevelDescription(self):
        return "--l {0} --pl {1} ".format(self.Status, self.Position)

    def GetStringCoordinates(self):
        coordinates = ""
        if self.Position == "north":
            coordinates = "1.5,0,0.4"
        elif self.Position == "east":
            coordinates = "0,-1.5,0.4"
        elif self.Position == "south":
            coordinates = "-1.5,0,0.4"
        elif self.Position == "west":
            coordinates = "0,1.5,0.4"
        return coordinates
