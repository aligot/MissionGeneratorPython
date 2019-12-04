# coding: utf-8

import abc


class EnvironmentalObject(abc.ABC):

    @property
    def _get_position(self):
        return self.position

    @property
    def _set_position(self, position):
        self.position = position

    @property
    @abc.abstractproperty
    def _get_low_level_desciption(self):
        """ Implement me! """
        pass
