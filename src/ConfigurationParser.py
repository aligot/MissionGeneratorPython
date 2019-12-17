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
                name, label, type, range, distribution = 'NA', 'NA', 'NA', 'NA', 'NA'
                strVariableDescription, strConditionDescription = re.split(r'\|', strLine)
                strVariableDescription = re.sub(' +', ' ', strVariableDescription)
                vecConditionDescription = re.split('and', re.sub(' +', '', strConditionDescription))
                vecVariableDescription = re.split(' ', strVariableDescription)
                if len(vecVariableDescription) == 5:  # 4 variables + ''
                    name, label, type, range = vecVariableDescription[0:4]
                elif len(vecVariableDescription) == 6:  # 5 variables + ''
                    name, label, type, range, distribution = vecVariableDescription[0:5]
                cCurrentVariable = ConfigurationVariable(name, label, type, range, distribution, vecConditionDescription)
                self.m_listConfigurationVariable.append(cCurrentVariable)
        return self.m_listConfigurationVariable

    def check(self):
        for variable in self.m_listConfigurationVariable:
            if variable.Type == 'categorical' and variable.Distribution != 'NA':
                if len(variable.Range) != len(variable.Distribution):
                    print("Error in variable {}: mismatch in length of possible values and distribution".format(variable.Name))
                    exit(1)
                elif (sum(variable.Distribution) != 1.0):
                    print("Error in variable {}: distribution values does not sum to 1".format(variable.Name))
                    exit(1)

    configuration_file = property(_get_configuration_file, _set_configuration_file)
