# coding: utf-8

import random
from decimal import Decimal
from collections import OrderedDict
from Vector3 import Vector3, Distance


class Mission:

    def __init__(self):
        self.DicVariables = OrderedDict()
        self.ListPatches = []
        self.ListObstacles = []
        self.ListLights = []

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

    def AddPatch(self, patch):
        # The position of the patch needs to be specified.
        pass

    def GetPossiblePatchColors(self, index_variable):
        pass

    def GetDescription(self):
        print("Generic mission...")

    def PositionPatch(self, patch):
        numberTries = 0
        boolPositioned = False
        minMaxPositionValues = self.Arena.GetMinMaxPositionValues()
        if patch.Distribution == 'unif':
            while numberTries <= 100 and not(boolPositioned):
                posX = float(round(Decimal(random.uniform(minMaxPositionValues[0], minMaxPositionValues[1])), 2))
                posY = float(round(Decimal(random.uniform(minMaxPositionValues[0], minMaxPositionValues[1])), 2))
                if self.Arena.IsWithinArena(posX, posY) and not(self.IsIntersectingWithOtherPatches(patch, posX, posY)):
                    boolPositioned = True
                    patch.Position = Vector3(posX, posY, 0)
                numberTries += 1
            if not(boolPositioned):
                print("Error: could not position patch #{}".format(patch.Index))
                exit(2)
        elif patch.Distribution == 'relation':
            while numberTries <= 100 and not(boolPositioned):
                patchRelated = random.choice(self.ListPatches)
                relatedPosition = patchRelated.Position
                side = random.choice(['North', 'East', 'South', 'West'])
                if side == 'North':  # Coord x is fixed, y can only increase
                    posX = relatedPosition.X
                    posY = float(round(Decimal(random.uniform(relatedPosition.Y, minMaxPositionValues[1])), 2))
                elif side == 'East':  # Coord y is fixed, x can only increase
                    posX = float(round(Decimal(random.uniform(relatedPosition.X, minMaxPositionValues[1])), 2))
                    posY = relatedPosition.Y
                elif side == 'South':  # Coord x is fixed, y can only decrease
                    posX = relatedPosition.X
                    posY = float(round(Decimal(random.uniform(minMaxPositionValues[0], relatedPosition.Y)), 2))
                elif side == 'West':  # Coord y is fixed, x can only decrease
                    posX = float(round(Decimal(random.uniform(relatedPosition.X, minMaxPositionValues[1])), 2))
                    posY = relatedPosition.Y
                if self.Arena.IsWithinArena(posX, posY) and not(self.IsIntersectingWithOtherPatches(patch, posX, posY)):
                    print(side, posX, posY)
                    boolPositioned = True
                    patch.Position = Vector3(posX, posY, 0)
                numberTries += 1
            if not(boolPositioned):
                print("Error: could not position patch #{}".format(patch.Index))
                exit(2)
        else:
            print("Error: distribution {} unknown!".format(patch.Distribution))

    def IsIntersectingWithOtherPatches(self, current_patch, pos_x, pos_y):
        positionCurrentPatch = Vector3(pos_x, pos_y, 0)
        if len(self.ListPatches) > 0:
            for patch in self.ListPatches:
                minimalDistanceBetweenPatches = self.ComputeMinimalDistancesNeededToAvoidOverlap(current_patch, patch)
                distBetweenPatches = Distance(positionCurrentPatch, patch.Position)
                if distBetweenPatches >= minimalDistanceBetweenPatches:
                    return(False)
                else:
                    return(True)
        else:
            return(False)

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
