# coding: utf-8

from EnvironmentalObject import EnvironmentalObject


class Light(EnvironmentalObject):

    def __init__(self):
        self.Status = None
        self.Position = None

    # def GetLowLevelDescription(self):
    #     return "--l {0} --pl {1} ".format(self.Status, self.Position)

    def GetARGoSDescription(self):
        return "<light id=\"{0}\" position=\"{1}\" orientation=\"0,0,0\" color=\"yellow\" intensity=\"{2}\" medium=\"leds\"/>".format('light', self.GetCoordinates(), self.GetIntensity())

    def GetCoordinates(self):
        if self.Status == 'on':
            if self.Position == "north":
                return "1.5,0,0.4"
            elif self.Position == "east":
                return "0,-1.5,0.4"
            elif self.Position == "south":
                return "-1.5,0,0.4"
            elif self.Position == "west":
                return "0,1.5,0.4"
        else:
            return "0,2.5,0.4"

    def GetIntensity(self):
        if self.Status == 'on':
            return '5.0'
        else:
            return '0.0'
