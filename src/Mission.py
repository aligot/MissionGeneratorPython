# coding: utf-8

import random
import math

from decimal import Decimal
from collections import OrderedDict
from Vector3 import Vector3, Distance, Middle, HorizontalAngle


class Mission:

    def __init__(self):
        self.DicVariables = OrderedDict()
        self.ListPatches = []
        self.ListObstacles = []
        self.ListLights = []
        self.MaxNumberTries = 100

    def AddVariable(self, key, value):
        self.DicVariables[key] = value

    def IsInstanciated(self, key, value):
        return key in self.DicVariables and eval(value) == self.DicVariables[key]

    def IsGreaterThan(self, key, value):
        return key in self.DicVariables and self.DicVariables[key] > eval(value)

    def IsDifferent(self, key, value):
        return key in self.DicVariables and eval(value) != self.DicVariables[key]

    def PrintDictionary(self):
        for key, value in self.DicVariables.items():
            print(key, ':', value)

    def SetArena(self, arena):
        self.Arena = arena
        arena.GenerateWalls()

    def AddLight(self, light):
        self.PositionLight(light)
        light.Index = len(self.ListLights)
        self.ListLights.append(light)

    def AddPatch(self, patch):
        # The position of the patch needs to be specified.
        pass

    def AddObstacle(self, obstacle):
        # The position of the patch needs to be specified.
        obstacle.Index = len(self.ListObstacles)
        self.PositionObstacle(obstacle)
        self.ListObstacles.append(obstacle)

    def GetPossiblePatchColors(self, index_variable):
        pass

    def GetDescription(self):
        print("Generic mission...")

    def GetLightsDescription(self):
        lightsDesciption = ""
        for light in self.ListLights:
            lightsDesciption += light.GetARGoSDescription() + '\n'
        return lightsDesciption

    def GetArenaDescription(self):
        return self.Arena.GetARGoSDescription()

    def GetObstaclesDescription(self):
        obstaclesDescription = ""
        for obstacle in self.ListObstacles:
            obstaclesDescription += obstacle.GetARGoSDescription() + '\n'
        return obstaclesDescription

    def PositionLight(self, light):
        distanceCenter = 0.25
        heightLight = 0.4
        if self.Arena.Shape == 'dodeca':
            inradiusDodecArena = (math.sqrt(6) + math.sqrt(2)) * self.Arena.SideLength / 2
            distanceCenter += inradiusDodecArena
        elif self.Arena.Shape == 'square':
            distanceCenter += self.Arena.SideLength / 2
        if light.Status == 'on':
            if self.Arena.Shape == 'dodeca':
                if light.Position == "north":
                    light.Coordinates = Vector3(distanceCenter, 0.0, heightLight)
                elif light.Position == "east":
                    light.Coordinates = Vector3(0.0, -distanceCenter, heightLight)
                elif light.Position == "south":
                    light.Coordinates = Vector3(-distanceCenter, 0.0, heightLight)
                elif light.Position == "west":
                    light.Coordinates = Vector3(0.0, distanceCenter, heightLight)
            elif self.Arena.Shape == 'square':
                if light.Position == "north":
                    light.Coordinates = Vector3(distanceCenter, distanceCenter, heightLight)
                elif light.Position == "east":
                    light.Coordinates = Vector3(-distanceCenter, -distanceCenter, heightLight)
                elif light.Position == "south":
                    light.Coordinates = Vector3(-distanceCenter, -distanceCenter, heightLight)
                elif light.Position == "west":
                    light.Coordinates = Vector3(distanceCenter, distanceCenter, heightLight)
        else:
            light.Coordinates = Vector3(distanceCenter, 0, -heightLight)

    def PositionObstacle(self, obstacle):
        numberTries = 0
        boolPositioned = False
        minMaxPositionValues = self.Arena.GetMinMaxPositionValues()
        if obstacle.Distribution == 'unif':
            while numberTries <= self.MaxNumberTries and not(boolPositioned):
                posX = float(round(Decimal(random.uniform(minMaxPositionValues[0], minMaxPositionValues[1])), 2))
                posY = float(round(Decimal(random.uniform(minMaxPositionValues[0], minMaxPositionValues[1])), 2))
                if self.Arena.IsObstacleInArena(obstacle, posX, posY):  # and not(self.IsBlockingSpace(obstacle, posX, posY)):
                    boolPositioned = True
                    obstacle.Position = Vector3(posX, posY, 0)
                numberTries += 1
            if not(boolPositioned):
                print("Error: could not position patch #{}".format(obstacle.Index))
                exit(2)
            else:
                return boolPositioned
        elif obstacle.Distribution == 'side':
            while numberTries <= self.MaxNumberTries and not(boolPositioned):
                squarePatches = []
                for patch in self.ListPatches:
                    if patch.Type == 'rect':
                        squarePatches.append(patch)
                if len(squarePatches) > 0:
                    randomPatch = random.choice(squarePatches)
                    obstacle.Length = randomPatch.Size
                    posY = randomPatch.Position.Y
                    posX = randomPatch.Position.X + randomPatch.Size/2 + obstacle.Width/2
                    if self.Arena.IsObstacleInArena(obstacle, posX, posY):
                        obstacle.Position = Vector3(posX, posY, 0.0)
                        boolPositioned = True
                    else:
                        numberTries += 1
                else:
                    print("Warning: no rectangular patches in environment, switch from \"side\" to \"between\" distribution")
                    obstacle.Distribution = 'between'
                    return self.PositionObstacle(obstacle)
            if not(boolPositioned):
                print("Error: could not position obstacle #{}".format(obstacle.Index))
                exit(2)
            else:
                return boolPositioned
        elif obstacle.Distribution == 'between':
            while numberTries <= self.MaxNumberTries and not(boolPositioned):
                print(numberTries)
                twoPatches = []
                try:
                    twoPatches = random.sample(self.ListPatches, 2)
                    print('Yes')
                except ValueError:
                    print("Warning: not enough patches in environment, switch from \"between\" to \"unif\" distribution")
                    obstacle.Distribution = 'unif'
                    return self.PositionObstacle(obstacle)
                print('ok')
                posX = Middle(twoPatches[0].Position, twoPatches[1].Position).X
                posY = Middle(twoPatches[0].Position, twoPatches[1].Position).Y
                obstacle.Orientation.X = 90 - HorizontalAngle(twoPatches[0].Position, twoPatches[1].Position)
                print(posX, posY)
                if self.Arena.IsObstacleInArena(obstacle, posX, posY):
                    obstacle.Position = Vector3(posX, posY, 0.0)
                    boolPositioned = True
                else:
                    numberTries += 1
            if not(boolPositioned):
                print("Error: could not position obstacle #{}".format(obstacle.Index))
                exit(2)
            else:
                return boolPositioned
        else:
            print("Error: distribution {} unknown!".format(obstacle.Distribution))

    def IsIntersectingWithOtherPatches(self, current_patch, pos_x, pos_y):
        intersecting = False
        positionCurrentPatch = Vector3(pos_x, pos_y, 0)
        if len(self.ListPatches) > 0:
            for patch in self.ListPatches:
                minimalDistanceBetweenPatches = self.ComputeMinimalDistancesNeededToAvoidOverlap(current_patch, patch)
                distBetweenPatches = Distance(positionCurrentPatch, patch.Position)
                if distBetweenPatches < minimalDistanceBetweenPatches:
                    intersecting = True
        return(intersecting)

    def ComputeMinimalDistancesNeededToAvoidOverlap(self, patch1, patch2):
        minimalDistanceBetweenPatches = 0
        if patch1.Type == "circ":
            minimalDistanceBetweenPatches += patch1.Size
        elif patch1.Type == "rect":
            minimalDistanceBetweenPatches += patch1.Size/2
        if patch2.Type == "circ":
            minimalDistanceBetweenPatches += patch2.Size
        elif patch2.Type == "rect":
            minimalDistanceBetweenPatches += patch2.Size/2
        return(minimalDistanceBetweenPatches)
