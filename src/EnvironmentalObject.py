# coding: utf-8

import abc


class EnvironmentalObject(abc.ABC):

    @property
    def _get_position(self):
        return self.Center

    @property
    def _set_position(self, position):
        self.Center = position
