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
cArgumentParser.add_argument('-s', '--seed', help='the seed for the RNG (if no value specified or set to 0, a random seed is used)', required=False, default=0)

if __name__ == "__main__":
    cArguments = cArgumentParser.parse_args()

    if cArguments.seed != 0:
        random.seed(cArguments.seed)
        print("Using given seed {}".format(cArguments.seed))
    else:
        time = datetime.datetime.now()
        seed = int(re.split(r'\.', str(time))[1])
        random.seed(seed)
        print("Using random seed {}".format(seed))

    cConfigurationParser = ConfigurationParser()
    cConfigurationParser.configuration_file = cArguments.paramsFile
    listConfigurationParameters = cConfigurationParser.parse()
    cConfigurationParser.check()

    missionGenerator = Generator(listConfigurationParameters)
    missionGenerator.Sample()
    #
    # box = Box()
    # box.Length = 0.50
    # box.Position = Vector3(0, 0, 0)
    # box.Orientation = Vector3(90, 0, 0)
    # box.GetBoundingBox()

    sys.exit(1)
