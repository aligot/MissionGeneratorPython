#!/usr/bin/python3

from __future__ import print_function
from ConfigurationParser import ConfigurationParser
from Generator import Generator

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
    print(missionGenerator.Sample())

    sys.exit(1)
