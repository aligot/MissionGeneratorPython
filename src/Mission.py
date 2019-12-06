# coding: utf-8

from collections import OrderedDict
from Arena import Arena


class Mission:

    def __init__(self):
        self.DicVariables = OrderedDict()

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

    # Checks wether object is in the arena or not
    def CheckInArena(self):
        pass
