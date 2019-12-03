# coding: utf-8

import re
import sys

class ConfigurationParser:

    def __init__(self):
        self.m_strConfigurationFile = ''

    def _get_configuration_file(self):
        return self.m_strConfigurationFile

    def _set_configuration_file(self, str_conf_file):
        self.m_strConfigurationFile = str_conf_file

    configuration_file = property(_get_configuration_file, _set_configuration_file)

    def open_configuration_file(self):
        try:
            self.m_strFileContent = open(self.m_strConfigurationFile, "r")
            print("Successfully opened parameter file", self.m_strConfigurationFile)
        except IOError:
            print("Error: file", self.m_strConfigurationFile, " does not exist!")
            sys.exit(2)

    def parse(self):
        self.open_configuration_file()
        content = self.m_strFileContent.readlines()
        for line in content:
            comment = re.findall("^#", line)
            if not(comment):
                print(line)
                variable, condition = re.split('\|', line)
                print("variable:", re.sub('\s+', ' ',variable))
                print("condition:", condition)
