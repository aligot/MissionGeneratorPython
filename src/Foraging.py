# coding: utf-8

from Mission import Mission


class Foraging(Mission):

    def GetPossiblePatchColors(self):
        totalNumberPatches = self.DicVariables['nPatchesFor']
        print(totalNumberPatches)

    def GetColorsExistingPatch(self):
        pass

    def AddPatch(self, patch):
        self.PositionPatch(patch)
        self.ListObjects.append(patch)

    def PositionPatch(self, patch):
        pass
