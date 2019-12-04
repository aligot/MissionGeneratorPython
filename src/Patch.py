# coding: utf-8

from EnvironmentalObject import EnvironmentalObject


class Patch(EnvironmentalObject):

    def __init__(self, index, type, position, size, color):
        self.Index = index
        self.Type = type
        self.Position = position
        self.Size = size
        self.Color = color

    def _get_type(self):
        return self.Type

    def _get_size(self):
        return self.Size

    def _get_color(self):
        return self.Color

    def _get_low_level_desciption(self):
        return "--tp{0} {1} --dp{0} {2} --cxp{0} {3} --cyp{0} {4} --cp{0} {5}".format(self.Index, self.Type, self.Size, self.Position.X, self.Position.Y, self.Color)

    low_level_desciption = property(_get_low_level_desciption)
