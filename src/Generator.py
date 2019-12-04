# coding: utf-8

import re
import random
from decimal import Decimal
from Mission import Mission
from Foraging import Foraging


class Generator:

    def __init__(self, list_of_configuration_variables):
        self.ConfigurationVariables = list_of_configuration_variables

    def Sample(self):
        # First variable: the mission
        self.InitializeMission(self.ConfigurationVariables[0])
        for variable in self.ConfigurationVariables:
            print(variable)
            if variable.Condition[0] == 'NA':
                print("No conditions detected")
                self.InitializeVariable(variable)
            else:
                for condition in variable.Condition:
                    if re.findall('==', condition):
                        key, value = re.split('==', condition)
                        if key in self.DicVariables and eval(value) == self.DicVariables[key]:
                            self.InitializeVariable(variable)
                    elif re.findall('>', condition):
                        key, value = re.split('>', condition)
                        if key in self.DicVariables and self.DicVariables[key] > eval(value):
                            self.InitializeVariable(variable)
            print('----------------------')
            print(self.DicVariables)
            print('----------------------')

    def InitializeVariable(self, variable):
        if variable.Type == 'categorical':
            if type(variable.Range) is tuple:
                self.DicVariables[variable.Name] = random.choice(variable.Range)
            else:
                self.DicVariables[variable.Name] = variable.Range
        elif variable.Type == 'integer':
            self.DicVariables[variable.Name] = random.randint(variable.Range[0], variable.Range[1])
        elif variable.Type == 'real':
            value = Decimal(random.uniform(variable.Range[0], variable.Range[1]))
            self.DicVariables[variable.Name] = float(round(value, 2))
        elif variable.Type == 'function':
            pass

    def InitializeMission(self, variable):
        mission = Mission()
        if variable.Type == 'categorical':
            if type(variable.Range) is tuple:
                missionType = random.choice(variable.Range)
            else:
                missionType = variable.Range
            if missionType == "for":
                mission = Foraging()
            elif missionType == "agg":
                print("Not implemented yet")
                exit(1)
            elif missionType == "dg":
                print("Not implemented yet")
                exit(1)
        else:
            print("Error: variable type for mission should be 'categorical'")
            exit(2)
        return mission
