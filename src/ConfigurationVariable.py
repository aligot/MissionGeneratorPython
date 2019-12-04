# coding: utf-8

import re


class ConfigurationVariable:

    def __init__(self, name, label, type, range, condition):
        self.Name = name
        self.Label = label
        self.Type = type
        self.Range = eval(range)     # list of strings
        self.Condition = condition   # list of different conditions

    def __str__(self):
        return "Name: {}\nLabel: {}\nType: {}\nRange: {}\nCondition: {}".format(self.Name, self.Label, self.Type, self.Range, self.Condition)
