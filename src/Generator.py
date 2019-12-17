# coding: utf-8

import re
import random
from numpy import cumsum
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
            if "Nest" in variable.Name:  # Foraging Nest; to be handled as a non-regular patch
                currentObjectVariables = [x for x in self.ConfigurationVariables if ('Nest' in x.Name)]
                self.HandleForagingNests(currentObjectVariables)
            elif "FS" in variable.Name:  # Foraging FoodSource; to be handled as a regular patch
                currentPatchIndex = int(re.findall(r'\d', variable.Name)[0])
                currentPatchVariables = [x for x in self.ConfigurationVariables if (('FS' in x.Name) and (int(re.findall(r'\d', x.Name)[0]) == currentPatchIndex))]
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
        print(self.Mission.PrintDictionary())
        print(self.Mission.GetDescription())
        self.WriteARGoSFile()

    def WriteARGoSFile(self):
        templateFile = open('../mission_config_template.argos')
        sourceTemplateFile = Template(templateFile.read())
        filledFile = sourceTemplateFile.substitute(missionDescription=self.Mission.GetDescription(), lightsDescription=self.Mission.GetLightsDescription(), arenaDescription=self.Mission.GetArenaDescription(), obstaclesDescription=self.Mission.GetObstaclesDescription())

        # print(self.Mission.GetArenaDescription())
        # print(self.Mission.GetObstaclesDescription())

        outputFile = open("../mission_config.argos", 'w')
        outputFile.write(filledFile)
        outputFile.close()

    def IsConditionRespected(self, variable):
        if variable.Condition[0] == 'NA':
            return True
        else:
            respected = True
            for condition in variable.Condition:
                if (respected):
                    if re.findall('==', condition):
                        key, value = re.split('==', condition)
                        respected = True if self.Mission.IsInstanciated(key, value) else False
                    elif re.findall('>', condition):
                        key, value = re.split('>', condition)
                        respected = True if self.Mission.IsGreaterThan(key, value) else False
                    elif re.findall('!=', condition):
                        key, value = re.split('!=', condition)
                        respected = True if self.Mission.IsDifferent(key, value) else False
            return respected

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
            if self.IsConditionRespected(variable):
                if variable.Name == 'arenaSide':
                    arena.SetSideLength(self.SampleVariable(variable))
                    self.Mission.AddVariable(variable.Name, arena.SideLength)
                elif variable.Name == 'arenaShape':
                    arena.SetShape(self.SampleVariable(variable))
                    self.Mission.AddVariable(variable.Name, arena.Shape)
                elif variable.Name == 'arenaFloorCol':
                    arena.SetFloorColor(self.SampleVariable(variable))
                    self.Mission.AddVariable(variable.Name, arena.FloorColor)
                else:
                    print("Error: unknown variable Arena variable name {}".format(variable.Name))
                    exit(2)
        self.Mission.SetArena(arena)
        for variable in arenaVariables:
            self.ConfigurationVariables.remove(variable)

    def HandleForagingNests(self, nests_variables):
        if self.IsConditionRespected(nests_variables[0]):
            for variable in nests_variables:
                if self.IsConditionRespected(variable):
                    self.InitializeVariable(variable)
                self.ConfigurationVariables.remove(variable)
            self.Mission.InitializeNests()

    def HandlePatch(self, patch_variables, index):
        if self.IsConditionRespected(patch_variables[0]):
            currentPatch = Patch()
            for variable in patch_variables:
                if self.IsConditionRespected(variable):
                    if 'type' in variable.Name:
                        currentPatch.Type = self.SampleVariable(variable)
                        self.Mission.AddVariable(variable.Name, currentPatch.Type)
                    elif 'color' in variable.Name:
                        if variable.Range != 'SelectColor()':
                            currentPatch.Color = self.SampleVariable(variable)
                        else:
                            currentPatch.Color = self.SamplePossibleValues(variable, self.Mission.GetPossiblePatchColors(index))
                        self.Mission.AddVariable(variable.Name, currentPatch.Color)
                    elif 'dim' in variable.Name:
                        currentPatch.Size = self.SampleVariable(variable)
                        self.Mission.AddVariable(variable.Name, currentPatch.Size)
                    elif 'dist' in variable.Name:
                        currentPatch.Distribution = self.SampleVariable(variable)
                        self.Mission.AddVariable(variable.Name, currentPatch.Distribution)
                    elif 'sep' in variable.Name:
                        currentPatch.RelationDistance = self.SampleVariable(variable)
                        self.Mission.AddVariable(variable.Name, currentPatch.RelationDistance)
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
                    self.Mission.AddVariable(variable.Name, light.Position)
        self.Mission.AddLight(light)
        for variable in light_variables:
            self.ConfigurationVariables.remove(variable)

    def HandleObstacle(self, obst_variables, obst_index):
        print("----- OBSTACLE {} ------".format(obst_index))
        if (self.IsConditionRespected(obst_variables[0])):
            currentObstacle = Box()
            for variable in obst_variables:
                if self.IsConditionRespected(variable):
                    currentObstacle.Type = "obstacle"
                    if 'size' in variable.Name:
                        currentObstacle.Length = self.SampleVariable(variable)
                        self.Mission.AddVariable(variable.Name, currentObstacle.Length)
                    elif 'ori' in variable.Name:
                        currentObstacle.Orientation.X = self.SampleVariable(variable)
                        self.Mission.AddVariable(variable.Name, currentObstacle.Orientation.X)
                    elif 'dist' in variable.Name:
                        currentObstacle.Distribution = self.SampleVariable(variable)
                        self.Mission.AddVariable(variable.Name, currentObstacle.Distribution)
                    elif 'sep' in variable.Name:
                        currentObstacle.RelationDistance = self.SampleVariable(variable)
            self.Mission.AddObstacle(currentObstacle)
        for variable in obst_variables:
            self.ConfigurationVariables.remove(variable)

    def SampleVariable(self, variable):
        if variable.Type == 'categorical':
            if type(variable.Range) is tuple:
                if variable.Distribution == "NA":
                    return(random.choice(variable.Range))
                else:
                    return(self.WeightedChoice(variable.Range, variable.Distribution))
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

    def WeightedChoice(self, possible_values, weights):
        cumulativeSum = cumsum(weights)
        index = sum(cumulativeSum < random.random())
        return possible_values[index]
