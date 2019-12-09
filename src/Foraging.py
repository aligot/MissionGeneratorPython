# coding: utf-8

import random
from decimal import Decimal
from Mission import Mission
from Vector3 import Vector3, Distance


class Foraging(Mission):

    def GetPossiblePatchColors(self, index_patch):
        possibleColors = ['white', 'gray', 'black']
        possibleColors.remove(self.Arena.FloorColor)
        totalNumberPatches = self.DicVariables['nPatchesFor']
        if index_patch == totalNumberPatches-1:
            if len(self.GetColorsExistingPatch()) == 2:
                return(possibleColors)
            else:
                possibleColors = list(set(possibleColors) - set(self.GetColorsExistingPatch()))
                return(possibleColors)
        else:
            return(possibleColors)

    def GetColorsExistingPatch(self):
        existingColors = []
        for patch in self.ListPatches:
            existingColors.append(patch.Color)
        return list(set(existingColors))  # Removing duplicates before returning

    def AddPatch(self, patch):
        self.PositionPatch(patch)
        self.ListPatches.append(patch)
        print('New patch added!! Type: {}, color: {}, size: {}, position: {}'.format(patch.Type, patch.Color, patch.Size, patch.Position))

    def PositionPatch(self, patch):
        numberTries = 0
        boolPositioned = False
        minMaxPositionValues = self.Arena.GetMinMaxPositionValues()
        if patch.Distribution == 'unif':
            while numberTries <= 100 and not(boolPositioned):
                print("Try #{}".format(numberTries))
                print(minMaxPositionValues)
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
            while numberTries <= 0 and not(boolPositioned):
                patchRelated = random.choice(self.ListPatches)
                relatedPosition = patchRelated.Position
                side = random.choice(['North', 'East', 'South', 'West'])
                if side == 'North':  # Coord x is fixed, y can only increase
                    posX = relatedPosition.GetX()
                    posY = float(round(Decimal(random.uniform(relatedPosition.GetY(), minMaxPositionValues[1])), 2))
                elif side == 'East':  # Coord y is fixed, x can only increase
                    posX = float(round(Decimal(random.uniform(relatedPosition.GetX(), minMaxPositionValues[1])), 2))
                    posY = relatedPosition.GetY()
                elif side == 'South':  # Coord x is fixed, y can only decrease
                    posX = relatedPosition.GetX()
                    posY = float(round(Decimal(random.uniform(minMaxPositionValues[0], relatedPosition.GetY())), 2))
                elif side == 'West':  # Coord y is fixed, x can only decrease
                    posX = float(round(Decimal(random.uniform(relatedPosition.GetX(), minMaxPositionValues[1])), 2))
                    posY = relatedPosition.GetY()
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

    def GetDescription(self):
        print('Foraging Mission')
