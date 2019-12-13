# coding: utf-8

from Mission import Mission


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

    def TerminateInitialization(self):
        possibleColors = ['white', 'gray', 'black']
        possibleColors.remove(self.Arena.FloorColor)
        self.ColorNest = self.DicVariables['colorNest']
        possibleColors.remove(self.ColorNest)
        self.ColorFoodSource = possibleColors[0]

    def GetDescription(self):
        self.TerminateInitialization()
        lowLevelDescription = "--m {} --el {} --r {} --io {} --ip {} --cnf {} --cfsf {} --np {} ".format(self.DicVariables['mission'], self.DicVariables['expLength'], self.DicVariables['robots'], self.DicVariables['initOrient'], self.DicVariables['initPosit'], self.ColorNest, self.ColorFoodSource, self.DicVariables['nPatchesFor'])
        lowLevelDescription += self.Arena.GetLowLevelDescription()
        for patch in self.ListPatches:
            lowLevelDescription += patch.GetLowLevelDescription()
        return(lowLevelDescription)
