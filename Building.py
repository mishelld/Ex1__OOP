import json
from Elevator import Elevator

class Building:
    
    def __init__(self, file):
        with open(file,'r') as f:
            data = json.load(f)
            self._minFloor = int(data["_minFloor"])
            self._maxFloor = int(data["_maxFloor"])
            self._elevators = []
            currId = 0
            for elev in data["_elevators"]:
                self._elevators.append(Elevator(elev, currId))   
                currId += 1
    
    def __str__(self):
        print = "[" + str(self._minFloor) + ", " + str(self._maxFloor) + "]\n"
        for elev in self._elevators:
            print += elev.__str__()
        return print
    
    def getMinFloor(self):
        return self._minFloor

    def getMaxFloor(self):
        return self._maxFloor
    
    def getElevators(self):
        return self._elevators