# coding: utf-8

from collections import OrderedDict
from Arena import Arena


class Mission:

    def __init__(self):
        self.DicVariables = OrderedDict()
        self.ListObjects = []

    def AddVariable(self, key, value):
        self.DicVariables[key] = value

    def IsInstanciated(self, key, value):
        return key in self.DicVariables and eval(value) == self.DicVariables[key]

    def IsGreaterThan(self, key, value):
        return key in self.DicVariables and self.DicVariables[key] > eval(value)

    def PrintDictionary(self):
        for key, value in self.DicVariables.items():
            print(key, ':', value)

    def SetArena(self, arena):
        self.Arena = arena

    def AddPatch(self, patch):
        # The position of the patch needs to be specified.
        pass

    def GetPossiblePatchColors(self):
        pass
