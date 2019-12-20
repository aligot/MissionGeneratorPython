#!/usr/bin/python3

from __future__ import print_function
from ConfigurationParser import ConfigurationParser
from Generator import Generator
from Box import Box
from Vector3 import Vector3, HorizontalAngle

import re
import sys
import random
import argparse
import datetime


cArgumentParser = argparse.ArgumentParser(description="Generator of missions")
cArgumentParser.add_argument('-c', '--paramsFile', help='the file containing the conifguration parameters', required=True)
cArgumentParser.add_argument('-s', '--seed', help='the seed for the RNG (if no value specified or set to 0, a random seed is used)', required=False, type=int)

if __name__ == "__main__":
    cArguments = cArgumentParser.parse_args()

    if cArguments.seed:
        seed = cArguments.seed
        random.seed(int(seed))
        print("Using given seed {}".format(seed))
    else:
        seed = int(re.split(r'\.', str(datetime.datetime.now()))[1])
        random.seed(seed)
        print("Using random seed {}".format(seed))

    cConfigurationParser = ConfigurationParser()
    cConfigurationParser.configuration_file = cArguments.paramsFile
    listConfigurationParameters = cConfigurationParser.parse()
    cConfigurationParser.check()

    missionGenerator = Generator(listConfigurationParameters)
    missionGenerator.Sample()


    sys.exit(1)
