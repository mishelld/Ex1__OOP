from CallForElevator import *

class Elevator:

    # Cunstractur for the elevator.
    # The cunstractur recives the data from the building class
    # that represents the elevator:
    # id of the elevator, the speed of the elevator,the min floor of the elevator,
    # the max floor of the elevator,the closing time of the elevator,the opening time of the elevator
    # the strat time of the elevator, the stoping time of the elevator, list of it's calls to finish and
    # it's position

    def __init__(self, input):
        self._id = int(input["_id"])
        self._speed = float(input["_speed"])
        self._minFloor = int(input["_minFloor"])
        self._maxFloor = int(input["_maxFloor"])
        self._closeTime = float(input["_closeTime"])
        self._openTime = float(input["_openTime"])
        self._startTime = float(input["_startTime"])
        self._stopTime = float(input["_stopTime"])
        self._calls = []
        self._position = 0
        self._reset = True
        self._counter = 0

    # a function that print the objects
    def __str__(self):
        print = "Elevator number: " + str(self._id) + "\n"
        print += "Speed: " + str(self._speed)
        print += " CloseTime: " + str(self._closeTime)
        print += " OpenTime: " + str(self._openTime)
        print += " StartTime: " + str(self._startTime)
        print += " StopTime: " + str(self._stopTime) + "\n"
        return print

    # Removing all the done calls from to do list of calls.
    def removeDoneCalls(self, currTime):
        for c in self._calls:
            if currTime > c.getFinishedTime():
                # Update call's state to done.
                c.setState(c.DONE)
                self._calls.remove(c)
                # Update the position of the elevator.
                self._position = c.getDest()

    # Returns the time length that will take the elevator to arrive to the call's source,
    # inculding the time complition of it's current calls.
    def timeToArrive(self, call):
        currPos = self._position
        time = 0
        # For each call in it's list of calls, calculate the time to complete the calls
        for c in self._calls:
            time += self.calculateSingleCallTime(currPos, c.getSrc())
            currPos = c.getSrc()
        if not self._calls.__len__() == 0:
            time += self.calculateSingleCallTime(currPos, self._calls[-1].getDest())
            currPos = self._calls[-1].getDest()
        # Add the time for arriving to call's source.
        time += self.calculateSingleCallTime(currPos, call.getSrc())
        return time
    
    # Calculate time that will take taKe elevator to go to destination floor from it's current position.
    def calculateSingleCallTime(self, currPos, dest):
        floors = abs(dest - currPos) # Number of floors to pass.
        addtime = self._startTime + self._stopTime + self._openTime + self._closeTime # Time of elevator's functions.
        # If already on destination's floor, this elevator doesn't need to start.
        if currPos == dest:   
            addtime -= self._startTime
        return floors / self._speed + addtime

    # a function that adds calls to the arraylist
    def insertCall(self, call):
        self._calls.append(call)

    def removeCall(self, call):
        try:
            self._calls.remove(call)
        except:
            raise Exception("ERROR: trying to remove undefined call from: " + str(self._id))

    # a funciton that sets the current position of the elevator
    def setPosition(self, position):
        if position < self._minFloor or position > self._maxFloor:
            raise Exception("ERROR: trying to set unvalid floor to: " + str(self._id))
        self._position = position

    def setReset(self, reset):
        self._reset = reset

    def setCounter(self, counter):
        self._counter = counter
    # a funciton that returns the id of the elevator
    def getId(self):
        return self._id

    def getPosition(self):
        return self._position

    def getCalls(self):
        return self._calls

    def getSpeed(self):
        return self._speed

    def getReset(self):
        return self._reset

    def getCounter(self):
        return self._counter
