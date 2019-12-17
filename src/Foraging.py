# coding: utf-8

import math
import random
from decimal import Decimal

from Patch import Patch
from Mission import Mission
from Vector3 import Vector3


class Foraging(Mission):

    def GetPossiblePatchColors(self, index_patch):
        possibleColors = ['white', 'gray', 'black']
        possibleColors.remove(self.Arena.FloorColor)
        totalNumberPatches = self.DicVariables['numberFoodSource']
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
        if not(patch.Placed):
            self.PositionPatch(patch)
        patch.Index = len(self.ListPatches)
        self.ListPatches.append(patch)

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

    def InitializeNests(self):
        # Creation of patches for nest:
        for indexNest in range(self.DicVariables['numberNests']):
            currentNest = Patch()
            currentWidth = self.DicVariables['widthNest{}'.format(indexNest)]
            currentNest.Color = self.DicVariables['colorNest']
            currentNest.Placed = True
            if self.Arena.Shape == "dodeca":
                currentNest.Type = 'rect'
                inradiusDodecArena = (math.sqrt(6) + math.sqrt(2)) * self.Arena.SideLength / 2
                currentNest.Size = inradiusDodecArena * 2
                if indexNest == 0:
                    currentNest.Position.Y = inradiusDodecArena * 2 - currentWidth
                elif indexNest == 1:
                    currentNest.Position.Y = -inradiusDodecArena * 2 + currentWidth
            elif self.Arena.Shape == "square":
                currentNest.Type = 'circ'
                currentNest.Size = currentWidth
                if indexNest == 0:
                    currentNest.Position.X = self.Arena.SideLength / 2
                    currentNest.Position.Y = self.Arena.SideLength / 2
                elif indexNest == 1:
                    currentNest.Position.X = -self.Arena.SideLength / 2
                    currentNest.Position.Y = -self.Arena.SideLength / 2
            self.AddPatch(currentNest)

    def TerminateInitialization(self):
        possibleColors = ['white', 'gray', 'black']
        possibleColors.remove(self.Arena.FloorColor)
        self.ColorNest = self.DicVariables['colorNest']
        possibleColors.remove(self.ColorNest)
        self.ColorFoodSource = possibleColors[0]

    def GetDescription(self):
        self.TerminateInitialization()
        lowLevelDescription = "--m {} --el {} --r {} --io {} --ip {} --cnf {} --cfsf {} --np {} ".format(self.DicVariables['mission'], self.DicVariables['expLength'], self.DicVariables['robots'], self.DicVariables['initOrient'], self.DicVariables['initPosit'], self.ColorNest, self.ColorFoodSource, self.DicVariables['numberNests'] + self.DicVariables['numberFoodSource'])
        lowLevelDescription += self.Arena.GetLowLevelDescription()
        for patch in self.ListPatches:
            lowLevelDescription += patch.GetLowLevelDescription()
        return(lowLevelDescription)
