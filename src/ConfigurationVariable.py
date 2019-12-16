# coding: utf-8


class ConfigurationVariable:

    def __init__(self, name, label, type, range, distribution, condition):
        self.Name = name
        self.Label = label
        self.Type = type
        # Range is a list of strings if range or string if function
        self.Range = eval(range) if self.Type != 'function' else range
        self.Distribution = eval(distribution) if self.Type == 'categorical' else distribution
        self.Condition = condition   # list of different conditions

    def __str__(self):
        return "Name: {}\nLabel: {}\nType: {}\nRange: {}\nCondition: {}".format(self.Name, self.Label, self.Type, self.Range, self.Condition)
