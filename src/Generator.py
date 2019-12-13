# coding: utf-8

import re
import random
from decimal import Decimal
from string import Template

from Mission import Mission
from Foraging import Foraging
from Arena import Arena
from Patch import Patch
from Light import Light
from Box import Box


class Generator:

    def __init__(self, list_of_configuration_variables):
        self.ConfigurationVariables = list_of_configuration_variables
        self.Mission = Mission()

    def Sample(self):
        self.HandleMission()
        self.HandleArena()
        while len(self.ConfigurationVariables) > 0:
            variable = self.ConfigurationVariables[0]
            if "PatchFor" in variable.Name:
                currentPatchIndex = int(re.findall(r'\d', variable.Name)[0])
                currentPatchVariables = [x for x in self.ConfigurationVariables if (('PatchFor' in x.Name) and (int(re.findall(r'\d', x.Name)[0]) == currentPatchIndex))]
                self.HandlePatch(currentPatchVariables, currentPatchIndex)
            elif "PatchAgg" in variable.Name:
                pass
            elif "light" in variable.Name:
                currentObjectVariables = [x for x in self.ConfigurationVariables if ('light' in x.Name)]
                self.HandleLight(currentObjectVariables)
            elif "Obs" in variable.Name and re.findall(r'\d', variable.Name):
                currentObstacleIndex = int(re.findall(r'\d', variable.Name)[0])
                currentObstacleVariables = [x for x in self.ConfigurationVariables if (('Obs' in x.Name) and (int(re.findall(r'\d', x.Name)[0]) == currentObstacleIndex))]
                self.HandleObstacle(currentObstacleVariables, currentObstacleIndex)
            # Else: global variable that does not need specific treatment
            else:
                if self.IsConditionRespected(variable):
                    self.InitializeVariable(variable)
                self.ConfigurationVariables.remove(variable)
        print(self.Mission.GetDescription())
        self.WriteARGoSFile()

    def WriteARGoSFile(self):
        templateFile = open('../mission_config_template.argos')
        sourceTemplateFile = Template(templateFile.read())
        filledFile = sourceTemplateFile.substitute(missionDescription=self.Mission.GetDescription(), lightsDescription=self.Mission.GetLightsDescription(), arenaDescription=self.Mission.GetArenaDescription())

        print(self.Mission.GetArenaDescription())

        outputFile = open("../mission_config.argos", 'w')
        outputFile.write(filledFile)
        outputFile.close()

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
                elif re.findall('!=', condition):
                    key, value = re.split('!=', condition)
                    return True if self.Mission.IsDifferent(key, value) else False

    def InitializeVariable(self, variable):
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

    def HandleMission(self):
        missionVariable = self.ConfigurationVariables[0]
        self.ConfigurationVariables.remove(missionVariable)
        mission = self.SampleVariable(missionVariable)
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
        for variable in arenaVariables:
            self.ConfigurationVariables.remove(variable)

    def HandlePatch(self, patch_variables, index):
        if self.IsConditionRespected(patch_variables[0]):
            currentPatch = Patch()
            currentPatch.Index = index
            for variable in patch_variables:
                if self.IsConditionRespected(variable):
                    if 'type' in variable.Name:
                        currentPatch.Type = self.SampleVariable(variable)
                    elif 'color' in variable.Name:
                        if variable.Range != 'SelectColor()':
                            currentPatch.Color = self.SampleVariable(variable)
                        else:
                            currentPatch.Color = self.SamplePossibleValues(variable, self.Mission.GetPossiblePatchColors(index))
                    elif 'dim' in variable.Name:
                        currentPatch.Size = self.SampleVariable(variable)
                    elif 'dist' in variable.Name:
                        currentPatch.Distribution = self.SampleVariable(variable)
                    elif 'sep' in variable.Name:
                        currentPatch.RelationDistance = self.SampleVariable(variable)
            self.Mission.AddPatch(currentPatch)
        for variable in patch_variables:
            self.ConfigurationVariables.remove(variable)

    def HandleLight(self, light_variables):
        light = Light()
        for variable in light_variables:
            if self.IsConditionRespected(variable):
                if variable.Name == "light":
                    light.Status = self.SampleVariable(variable)
                    self.Mission.AddVariable(variable.Name, light.Status)
                elif variable.Name == "lightPos":
                    light.Position = self.SampleVariable(variable)
        self.Mission.AddLight(light)
        for variable in light_variables:
            self.ConfigurationVariables.remove(variable)

    def HandleObstacle(self, obst_variables, obst_index):
        print("----- OBSTACLE {} ------".format(obst_index))
        if (self.IsConditionRespected(obst_variables[0])):
            for variable in obst_variables:
                if self.IsConditionRespected(variable):
                    currentObstacle = Box()
                    currentObstacle.Type = "obstacle"
                    currentObstacle.Index = obst_index
                    if "size" in variable.Name:
                        currentObstacle.Length = self.SampleVariable(variable)
                    elif 'dist' in variable.Name:
                        currentObstacle.Distribution = self.SampleVariable(variable)
                    elif 'sep' in variable.Name:
                        currentObstacle.RelationDistance = self.SampleVariable(variable)
            self.Mission.AddObstacle(currentObstacle)
        for variable in obst_variables:
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

    def SamplePossibleValues(self, variable, possible_values):
        if type(possible_values) is tuple or list:
            return(random.choice(possible_values))
        else:
            return(possible_values)
