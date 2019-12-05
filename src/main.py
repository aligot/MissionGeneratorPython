#!/usr/bin/python3

from __future__ import print_function
from ConfigurationParser import ConfigurationParser
from Generator import Generator
from Vector3 import Vector3
from Patch import Patch

import sys
import argparse


cArgumentParser = argparse.ArgumentParser(description="Generator of missions")
cArgumentParser.add_argument('-c', '--paramsFile', help='the file containing the conifguration parameters', required=True)

if __name__ == "__main__":
    cArguments = cArgumentParser.parse_args()

    cConfigurationParser = ConfigurationParser()
    cConfigurationParser.configuration_file = cArguments.paramsFile
    listConfigurationParameters = cConfigurationParser.parse()

    missionGenerator = Generator(listConfigurationParameters)
    missionGenerator.Sample()

    positionPatch = Vector3(1, 1.2, 0)
    firstPatch = Patch(0, 'circ', positionPatch, 0.2, 'black')

    # print(firstPatch.low_level_desciption)

    sys.exit(1)
