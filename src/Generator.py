# coding: utf-8

import re
import random
from decimal import Decimal
from Mission import Mission
from Foraging import Foraging
from Arena import Arena
from Patch import Patch


class Generator:

    def __init__(self, list_of_configuration_variables):
        self.ConfigurationVariables = list_of_configuration_variables
        self.Mission = Mission()

    def Sample(self):
        self.HandleMission()
        self.HandleArena()
        for variable in self.ConfigurationVariables:
            # print(variable)
            if "PatchFor" in variable.Name:
                currentObjectIndex = int(re.findall(r'\d', variable.Name)[0])
                currentObjectVariables = [x for x in self.ConfigurationVariables if (('PatchFor' in x.Name) and (int(re.findall(r'\d', x.Name)[0]) == currentObjectIndex))]
                self.HandlePatch(currentObjectVariables, currentObjectIndex)
            elif "PatchAgg" in variable.Name:
                pass
            # Else: global variable that does not need specific treatment
            else:
                if self.IsConditionRespected(variable):
                    self.InitializeVariable(variable)
        self.Mission.PrintDictionary()

    def IsConditionRespected(self, variable):
        if variable.Condition[0] == 'NA':
            return True
        else:
            for condition in variable.Condition:
                if re.findall('==', condition):
                    key, value = re.split('==', condition)
                    return True if self.Mission.IsInstanciated(key, value) else False
                elif re.findall('>', condition):
                    key, value = re.split('>', condition)
                    return True if self.Mission.IsGreaterThan(key, value) else False

    def InitializeVariable(self, variable):
        if re.findall('Patch', variable.Name):
            pass
        if variable.Type == 'categorical':
            if type(variable.Range) is tuple:
                self.Mission.AddVariable(variable.Name, random.choice(variable.Range))
            else:
                self.Mission.AddVariable(variable.Name, variable.Range)
        elif variable.Type == 'integer':
            self.Mission.AddVariable(variable.Name, random.randint(variable.Range[0], variable.Range[1]))
        elif variable.Type == 'real':
            value = Decimal(random.uniform(variable.Range[0], variable.Range[1]))
            self.Mission.AddVariable(variable.Name, float(round(value, 2)))
        elif variable.Type == 'function':
            pass

    def HandleMission(self):
        missionVariable = self.ConfigurationVariables[0]
        self.ConfigurationVariables.remove(missionVariable)
        mission = self.InitializeVariable(missionVariable)
        if mission == "for":
            self.Mission = Foraging()
            self.Mission.AddVariable('mission', mission)
        elif mission == "agg":
            print("Aggregation Not implemented yet")
            exit(1)
        elif mission == "dg":
            print("DirectionalGate Not implemented yet")
            exit(1)

    def HandleArena(self):
        arena = Arena()
        arenaVariables = [x for x in self.ConfigurationVariables if re.findall('arena', x.Name)]
        for variable in arenaVariables:
            self.ConfigurationVariables.remove(variable)
            if variable.Name == 'arenaSide':
                arena.SetSideLength(self.SampleVariable(variable))
            elif variable.Name == 'arenaShape':
                arena.SetShape(self.SampleVariable(variable))
            elif variable.Name == 'arenaFloorCol':
                arena.SetFloorColor(self.SampleVariable(variable))
            else:
                print("Error: unknown variable Arena variable name {}".format(variable.Name))
                exit(2)
        self.Mission.SetArena(arena)

    def HandlePatch(self, patch_variables, index):
        print("------ Patch {} ------".format(index))
        if self.IsConditionRespected(patch_variables[0]):
            currentPatch = Patch()
        for variable in patch_variables[1:]:
            print(variable.Name, self.IsConditionRespected(variable))

        for variable in patch_variables:
            self.ConfigurationVariables.remove(variable)

    def SampleVariable(self, variable):
        if variable.Type == 'categorical':
            if type(variable.Range) is tuple:
                return(random.choice(variable.Range))
            else:
                return(variable.Range)
        elif variable.Type == 'integer':
            return(random.randint(variable.Range[0], variable.Range[1]))
        elif variable.Type == 'real':
            value = Decimal(random.uniform(variable.Range[0], variable.Range[1]))
            return(float(round(value, 2)))
