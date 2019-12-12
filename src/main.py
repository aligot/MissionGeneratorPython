#!/usr/bin/python3

from __future__ import print_function
from ConfigurationParser import ConfigurationParser
from Generator import Generator

import sys
import argparse
from string import Template


cArgumentParser = argparse.ArgumentParser(description="Generator of missions")
cArgumentParser.add_argument('-c', '--paramsFile', help='the file containing the conifguration parameters', required=True)

if __name__ == "__main__":
    cArguments = cArgumentParser.parse_args()

    cConfigurationParser = ConfigurationParser()
    cConfigurationParser.configuration_file = cArguments.paramsFile
    listConfigurationParameters = cConfigurationParser.parse()

    missionGenerator = Generator(listConfigurationParameters)
    generatedMissionDescription = missionGenerator.Sample()
    print(generatedMissionDescription)

    templateFile = open('../mission_config_template.argos')
    sourceTemplateFile = Template(templateFile.read())
    filledFile = sourceTemplateFile.substitute(missionDescription=generatedMissionDescription)

    outputFile = open("../mission_config.argos", 'w')
    outputFile.write(filledFile)
    outputFile.close()

    sys.exit(1)
