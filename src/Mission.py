# coding: utf-8


class Mission:

    def __init__(self):
        self.DicVariables = {}

    def AddVariable(self, key, value):
        self.DicVariables[key] = value

    def IsInstanciated(self, key, value):
        return key in self.DicVariables and eval(value) == self.DicVariables[key]

    def IsGreaterThan(self, key, value):
        key in self.DicVariables and self.DicVariables[key] > eval(value)

    def PrintDictionary(self):
        for key, value in self.DicVariables.items:
            print(key, ':', value)
