
class CallForElevator:

    INIT = 0; DONE = 3
    
    def __init__(self, data):
        self._name = data[0]
        self._time = float(data[1])
        self._src = int(data[2])
        self._dest = int(data[3])
        self._state = int(data[4])
        self._allocatedTo = int(data[5])
        self._finishedTime = -1

    def __str__(self):
        print = self._name + ": "
        print += "at " + str(self._time)
        print += " from " + str(self._src)
        print += " to " + str(self._dest)
        if self._state == self.INIT:
            print += " waiting for " + str(self._allocatedTo)
        elif self._state == self.DONE:
            print += " is Done!"
        else:
            print += " allocatedTo: " + str(self._allocatedTo)
        return print
    
    def setState(self, state):
        if not (state == self.INIT or state == self.DONE):
            raise Exception("ERROR: trying to set unvalid state to: \n" + self.__str__())
        self._state = state

    def setAllocatedTo(self, elevator, building):
        isThere = False
        for elev in building.getElevators():
            if elevator.getId() == elev.getId() :
                isThere = True
        if not isThere:
            raise Exception("ERROR: trying to set unvalid elevator to: \n" + self.__str__())
        self._allocatedTo = elevator.getId() 
    
    def setFinishedTime(self, time):
        self._finishedTime = time

    def getTime(self):
       return  self._time 

    def getSrc(self):
       return  self._src

    def getDest(self):
       return  self._dest  
       
    def getState(self):
        return self._state
    
    def getAllocatedTo(self):
        return self._allocatedTo
    
    def getFinishedTime(self):
        return self._finishedTime