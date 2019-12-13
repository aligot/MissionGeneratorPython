#!/usr/bin/python3

from __future__ import print_function
from ConfigurationParser import ConfigurationParser
from Generator import Generator

import sys
import random
import argparse


cArgumentParser = argparse.ArgumentParser(description="Generator of missions")
cArgumentParser.add_argument('-c', '--paramsFile', help='the file containing the conifguration parameters', required=True)
cArgumentParser.add_argument('-s', '--seed', help='the seed for the RNG (if no value specified or set to 0, a random seed is used)', required=False, default=0)

if __name__ == "__main__":
    cArguments = cArgumentParser.parse_args()

    if cArguments.seed != 0:
        random.seed(cArguments.seed)

    cConfigurationParser = ConfigurationParser()
    cConfigurationParser.configuration_file = cArguments.paramsFile
    listConfigurationParameters = cConfigurationParser.parse()

    missionGenerator = Generator(listConfigurationParameters)
    missionGenerator.Sample()

    sys.exit(1)
