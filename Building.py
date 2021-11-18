import json
from Elevator import Elevator

class Building:

    # cunstractur for the building.the cunstractur recives a json file that contains 
    # the objects of the buliding:min floor,max floor and the elevators

    def __init__(self, file):
        with open(file,'r') as f:
            input = json.load(f)
            self._minFloor = int(input["_minFloor"])
            self._maxFloor = int(input["_maxFloor"])
            self._elevators = []
            for elev in input["_elevators"]:
                self._elevators.append(Elevator(elev)) 

    # prints the objects of the building
    def __str__(self):
        print = "[" + str(self._minFloor) + ", " + str(self._maxFloor) + "]\n"
        for elev in self._elevators:
            print += elev.__str__()
        return print

    # function that returns the min floor
    def getMinFloor(self):
        return self._minFloor

    # funstion that returns the max floor
    def getMaxFloor(self):
        return self._maxFloor
        
    # function that returns elevators
    def getElevators(self):
        return self._elevators