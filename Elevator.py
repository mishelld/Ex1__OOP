from CallForElevator import *

class Elevator:

    def __init__(self, data):
        self._id = int(data["_id"])
        self._speed = float(data["_speed"])
        self._minFloor = int(data["_minFloor"])
        self._maxFloor = int(data["_maxFloor"])
        self._closeTime = float(data["_closeTime"])
        self._openTime = float(data["_openTime"])
        self._startTime = float(data["_startTime"])
        self._stopTime = float(data["_stopTime"])
        self._calls = []
        self._position = 0

    def __str__(self):
        print = "Elevator number: " + str(self._id) + "\n"
        print += "Speed: " + str(self._speed)
        print += " CloseTime: " + str(self._closeTime)
        print += " OpenTime: " + str(self._openTime)
        print += " StartTime: " + str(self._startTime)
        print += " StopTime: " + str(self._stopTime) + "\n"
        return print

    def removeDoneCalls(self, currTime):
        for c in self._calls:
            if currTime > c.getFinishedTime():
                c.setState(c.DONE)
                self._calls.remove(c)
                self._position = c.getDest()

    def timeToArrive(self, call):
        currPos = self._position
        time = 0
        for c in self._calls:
            time += self.calculateSingleCallTime(currPos, c.getSrc())
            currPos = c.getSrc()
        if not self._calls.__len__() == 0:
            time += self.calculateSingleCallTime(currPos, self._calls[-1].getDest())
            currPos = self._calls[-1].getDest()
        time += self.calculateSingleCallTime(currPos, call.getSrc())
        return time
    
    def calculateSingleCallTime(self, currPos, dest):
        floors = abs(dest - currPos)
        addtime = self._startTime + self._stopTime + self._openTime + self._closeTime
        if currPos == dest:   
            addtime -= self._startTime
        return floors / self._speed + addtime

    def addCall(self, call):
        self._calls.append(call)

    def isFree(self):
        return self._calls.isEmpty()

    def setPosition(self, position):
        if position < self._minFloor or position > self._maxFloor:
            raise Exception("ERROR: trying to set unvalid floor to: " + str(self._id))
        self._position = position

    def getId(self):
        return self._id

    def getSpeed(self):
        return self._speed
    
    def getMinFloor(self):
        return self._minFloor

    def getMaxFloor(self):
        return self._maxFloor

    def getCloseTime(self):
        return self._closeTime

    def getOpenTime(self):
        return self._openTime

    def getStartTime(self):
        return self._startTime

    def getStopTime(self):
        return self._stopTime

    def getCalls(self):
        return self._calls

    def getPosition(self):
        return self._position