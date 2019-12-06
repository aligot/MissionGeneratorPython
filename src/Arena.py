# coding: utf-8

import mpmath as mp
from Vector3 import Vector3, Distance
from EnvironmentalObject import EnvironmentalObject


class Arena(EnvironmentalObject):

    def __init__(self):
        self.Center = Vector3(0, 0, 0)
        self.SideLength = 0
        self.Shape = ''
        self.FloorColor = ''

    def SetSideLength(self, side_length):
        self.SideLength = side_length

    def SetShape(self, shape):
        self.Shape = shape

    def SetFloorColor(self, color):
        self.FloorColor = color

    def IsWithinArena(self, point_x, point_y):
        point = Vector3(point_x, point_y, 0)
        if self.Shape == 'square':
            if (-self.SideLength/2 <= point.X <= self.SideLength/2) and (-self.SideLength/2 <= point.Y <= self.SideLength/2):
                return True
        elif self.Shape == 'dodeca':
            nbSides = 12
            inradius = self.SideLength/2 * mp.cot(mp.pi/nbSides)
            if Distance(self.Center, point) <= inradius:
                return True
            else:
                return False

    def _get_low_level_desciption(self):
        return("--asi {} --ash {} --afc {}".format(self.SideLength, self.Shape, self.FloorColor))