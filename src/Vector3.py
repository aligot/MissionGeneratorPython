# coding: utf-8

import math


class Vector3:

    def __init__(self, x, y, z):
        self.X = x
        self.Y = y
        self.Z = z

    def _get_length(self):
        return math.sqrt(self.SquareLength())

    def SquareLength(self):
        return math.pow(self.X, 2) + math.pow(self.Y, 2) + math.pow(self.Z, 2)

    def __str__(self):
        return "{}, {}, {}".format(self.X, self.Y, self.Z)

    def __sub__(self, other):
        x = self.X - other.X
        y = self.Y - other.Y
        z = self.Z - other.Z
        return Vector3(x, y, z)

    def __add__(self, other):
        x = self.X + other.X
        y = self.Y + other.Y
        z = self.Z + other.Z
        return Vector3(x, y, z)

    def __imul__(self, int):
        x = self.X * int
        y = self.Y * int
        z = self.Z * int
        return Vector3(x, y, z)

    length = property(_get_length)


def Distance(first, second):
    return (first - second).length
