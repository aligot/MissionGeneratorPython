# coding: utf-8

import re
import sys

from ConfigurationVariable import ConfigurationVariable


class ConfigurationParser:

    def __init__(self):
        self.m_strConfigurationFile = ''
        self.m_listConfigurationVariable = []

    def _get_configuration_file(self):
        return self.m_strConfigurationFile

    def _set_configuration_file(self, str_conf_file):
        self.m_strConfigurationFile = str_conf_file

    def open_configuration_file(self):
        try:
            self.m_strFileContent = open(self.m_strConfigurationFile, "r")
            print("Successfully opened parameter file {}".format(self.m_strConfigurationFile))
        except IOError:
            print("Error: file {} does not exist!".format(self.m_strConfigurationFile))
            sys.exit(2)

    def parse(self):
        self.open_configuration_file()
        vecContent = self.m_strFileContent.readlines()
        for strLine in vecContent:
            comment = re.findall("^#", strLine)
            if not(comment):
                strLine = re.sub('\n', '', strLine)
                strVariableDescription, strConditionDescription = re.split(r'\|', strLine)
                strVariableDescription = re.sub(' +', ' ', strVariableDescription)
                vecConditionDescription = re.split(',', re.sub(' +', '', strConditionDescription))
                name, label, type, range = re.split(' ', strVariableDescription)[0:4]
                cCurrentVariable = ConfigurationVariable(name, label, type, range, vecConditionDescription)
                self.m_listConfigurationVariable.append(cCurrentVariable)
        return self.m_listConfigurationVariable

    configuration_file = property(_get_configuration_file, _set_configuration_file)
