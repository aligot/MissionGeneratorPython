# coding: utf-8

import mpmath as mp
import copy
from decimal import Decimal

from Vector3 import Vector3, Distance
from EnvironmentalObject import EnvironmentalObject
from Box import Box


class Arena(EnvironmentalObject):

    def __init__(self):
        self.Center = Vector3(0, 0, 0)
        self.SideLength = 0
        self.Shape = ''
        self.FloorColor = ''
        self.ListWalls = []

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
            else:
                return False
        elif self.Shape == 'dodeca':
            nbSides = 12
            inradius = self.SideLength/2 * mp.cot(mp.pi/nbSides)
            if Distance(self.Center, point) <= inradius:
                return True
            else:
                return False

    def IsObstacleInArena(self, obstacle, posX, posY):
        tempObstacle = copy.deepcopy(obstacle)
        tempObstacle.Position = Vector3(posX, posY, 0)
        boolInArena = True
        for corner in tempObstacle.GetBoundingBox():
            if not(self.IsWithinArena(corner.X, corner.Y)):
                boolInArena = False
        return boolInArena

    def GetMinMaxPositionValues(self):
        minMaxValues = (0, 0)
        if self.Shape == 'square':
            minMaxValues = (-self.SideLength/2, self.SideLength/2)
        elif self.Shape == 'dodeca':
            nbSides = 12
            inradius = float(round(Decimal(float(self.SideLength/2 * mp.cot(mp.pi/nbSides))), 2))
            minMaxValues = (-inradius, inradius)
        return(minMaxValues)

    def GenerateWalls(self):
        if self.Shape == 'dodeca':
            cos30 = mp.cos(mp.pi/6)
            cos60 = mp.cos(mp.pi/3)
            magicnumber = 0.536
            apothem = self.SideLength/magicnumber
            # South Wall
            self.CreateWall(0, Vector3(-apothem, 0, 0), 0)
            # North Wall
            self.CreateWall(1, Vector3(apothem, 0, 0), 0)
            # East Wall
            self.CreateWall(2, Vector3(0, apothem, 0), 90)
            # West Wall
            self.CreateWall(3, Vector3(0, -apothem, 0), 90)
            # South East Wall
            self.CreateWall(4, Vector3(-apothem*cos60, -apothem*cos30, 0), 60)
            # South South East Wall
            self.CreateWall(5, Vector3(-apothem*cos30, -apothem*cos60, 0), 30)
            # North West Wall
            self.CreateWall(6, Vector3(apothem*cos60, apothem*cos30, 0), 60)
            # North North West Wall
            self.CreateWall(7, Vector3(apothem*cos30, apothem*cos60, 0), 30)
            # South West wall
            self.CreateWall(8, Vector3(-apothem*cos60, apothem*cos30, 0), -60)
            # South South West wall
            self.CreateWall(9, Vector3(-apothem*cos30, apothem*cos60, 0), -30)
            # North East wall
            self.CreateWall(10, Vector3(apothem*cos60, -apothem*cos30, 0), -60)
            # North North East wall
            self.CreateWall(11, Vector3(apothem*cos30, -apothem*cos60, 0), -30)
        elif self.Shape == 'hexagon':
            inradius = self.SideLength/2 * mp.cot(mp.pi/6)
            cos60 = mp.cos(mp.pi/3)
            sin60 = mp.sin(mp.pi/3)
            posY = cos60 * inradius
            posX = sin60 * inradius
            # East Wall
            self.CreateWall(0, Vector3(0, -inradius, 0), 90)
            # West Wall
            self.CreateWall(1, Vector3(0, inradius, 0), 90)
            self.CreateWall(2, Vector3(posX, posY, 0), 30)
            self.CreateWall(3, Vector3(posX, -posY, 0), -30)
            self.CreateWall(4, Vector3(-posX, posY, 0), -30)
            self.CreateWall(5, Vector3(-posX, - posY, 0), 30)
        elif self.Shape == 'square':
            inradius = self.SideLength/2
            cos45 = mp.cos(mp.pi/4)
            sin45 = mp.sin(mp.pi/4)
            posX = cos45 * inradius
            posY = sin45 * inradius
            # South Wall
            self.CreateWall(0, Vector3(posX, posY, 0), 45)
            # North Wall
            self.CreateWall(1, Vector3(-posX, -posY, 0), 45)
            # East Wall
            self.CreateWall(2, Vector3(posX, -posY, 0), -45)
            # West Wall
            self.CreateWall(3, Vector3(-posX, posY, 0), -45)
        elif self.Shape == 'trigon':
            inradius = self.SideLength/2 * mp.cot(mp.pi/3)
            cos20 = mp.cos(mp.pi/6)
            sin20 = mp.sin(mp.pi/6)
            posX = cos20 * inradius
            posY = sin20 * inradius
            # South Wall
            self.CreateWall(0, Vector3(posY, posX, 0), 60)
            # North Wall
            self.CreateWall(1, Vector3(posY, -posX, 0), -60)
            # East Wall
            self.CreateWall(2, Vector3(-inradius, 0, 0), 0)
        elif self.Shape == 'heart':
            inradius = self.SideLength/2
            cos45 = mp.cos(mp.pi/4)
            sin45 = mp.sin(mp.pi/4)
            posX = cos45 * inradius
            posY = sin45 * inradius
            # South Wall
            self.CreateWall(0, Vector3(-posX, -posY, 0), 45)
            # North Wall
            self.CreateWall(1, Vector3(-posX, posY, 0), -45)
            # East Wall
            self.CreateWall(2, Vector3(posX/2, posY/2, 0), -45, self.SideLength/2)
            self.CreateWall(3, Vector3(posX/2, -posY/2, 0), 45, self.SideLength/2)
            self.CreateWall(4, Vector3(posX/2, self.SideLength/2, 0), 45, self.SideLength/2)
            self.CreateWall(5, Vector3(posX/2, -posY/2, 0), 45, self.SideLength/2)
        else:
            print("Error: undefined arena shape: {}".format(self.Shape))
            exit(2)

    def CreateWall(self, index, position, orientation, length=None):
        if not(length):
            length = self.SideLength
        newWall = Box()
        newWall.Type = 'wall'
        newWall.Index = index
        newWall.Length = length
        newWall.Height = 0.08
        newWall.Width = 0.01
        newWall.Position = position
        newWall.Orientation = Vector3(orientation, 0, 0)
        self.ListWalls.append(newWall)

    def GetLowLevelDescription(self):
        return("--asi {} --ash {} --afc {} ".format(self.SideLength, self.Shape, self.FloorColor))

    def GetARGoSDescription(self):
        argosDescription = ""
        for wall in self.ListWalls:
            argosDescription += wall.GetARGoSDescription() + '\n'
        return argosDescription
