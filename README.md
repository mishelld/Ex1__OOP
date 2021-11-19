# Ex.1: Off-line Algorithms for the Smart Elevator Scheduling Problem

# Overview

# The Elevator Problem:

The main problem we face is the shortening of the waiting time and the operating time of the elevators, ie the efficient timing of the elevators, which will suit any building, regardless of the number of floors or the number of elevators in it.

The problem in detail:
1. There are "F" floors in a building.
2. There are "N" smart elevators in a building.
3. There are elevator calls coming from people on each floor according to the Of-line record. 
4. The request of each call is to go from one floor (source) to another (destination).
5. In smart elevators, the destination floor is already set at the time of the elevator call and cannot be changed during the elevator ride.
6. The elevator can stop on floors other than its destination floor only on the condition that it has not yet reached the same floor and if the direction is the same as the original direction of the elevator.
7. Important to note: Each call comes at a particular time which means the calls do not necessarily overlap.
8. The goal is to allocate an elevator in the fastest time so that the waiting time for the elevator and the operation time from the moment of the call to the moment when the elevator reaches the destination floor will be the shortest. Needless to say, it is important for the algorithm to provide an answer to all calls without exception.



# Motivation:

Unlike the online algorithm, in the off-line, we know the arrival time of the elevator call, and then we can find the optimal schedule between the elevators in the building in relation to their location, speed, state, and direction.


# Algorithm:

	def algorithm():
	    global calls
	    global building
	    elevators = building.getElevators()
	    currTime = 0 # Our Time tracker
	    for c in calls:
		# Finding the elevator with the shortes time to arrive to the call, and set it to min
		min = building.getElevators()[0]
		for e in elevators:
		    # Removing all the done calls from this elevator's list of calls.
		    e.removeDoneCalls(currTime)
		    if min.timeToArrive(c) > e.timeToArrive(c):
			min = e
		# Adds the call to min's list of calls.
		min.addCall(c)
		# Allocate this call to min.
		c.setAllocatedTo(min, building)
		# Update the finised time of this call.
		c.setFinishedTime(currTime + min.timeToArrive(c) + min.calculateSingleCallTime(c.getSrc(), c.getDest()))
		# Update our current time.
		currTime = c.getTime()


# Removing all the done calls from to do list of calls.
    def removeDoneCalls(self, currTime):
        for c in self._calls:
            if currTime > c.getFinishedTime():
                # Update call's state to done.
                c.setState(c.DONE)
                self._calls.remove(c)
                # Update the position of the elevator.
                self._position = c.getDest()


# Returns the time length that will take the elevator to arrive to the call's source,inculding the time complition of it's current calls.
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


# Calculate time that will take the elevator to go to destination floor from it's current position.
    def calculateSingleCallTime(self, currPos, dest):
        floors = abs(dest - currPos) # Number of floors to pass.
        addtime = self._startTime + self._stopTime + self._openTime + self._closeTime # Time of elevator's functions.
        # If already on destination's floor, this elevator doesn't need to start.
        if currPos == dest:  
            addtime -= self._startTime
        return floors / self._speed + addtime


# a function that adds calls to the arraylist.
    def addCall(self, call):
        self._calls.append(call)



   # a function that sets the current position of the elevator.
    def setPosition(self, position):
        if position < self._minFloor or position > self._maxFloor:
            raise Exception("ERROR: trying to set unvalid floor to: " + str(self._id))
        self._position = position
	
	
# a function that sets to which elevator to allocate the call.
	def setAllocatedTo(self, elevator, building):
	   isThere = False
	   for elev in building.getElevators():
	       if elevator.getId() == elev.getId() :
		   isThere = True
	   if not isThere:
	       raise Exception("ERROR: trying to set unvalid elevator to: \n" + self.__str__())
	   self._allocatedTo = elevator.getId()

 # UML:
![diagram - Page 2 (8)](https://user-images.githubusercontent.com/93199677/142676116-282ca067-e7db-4b5e-a938-4198132ffb98.png)

# Report results:
![d7e8df7a_1](https://user-images.githubusercontent.com/93255163/142496370-4bb65169-f64f-453e-9154-a3104c66e076.png)

# Bonus:
Simulation Link: https://www.youtube.com/watch?v=d09JXNFEY3g

# Helpful Links:

1. Project Idea | Smart Elevator : On this site you can find an explanation of the operation process of smart elevators, how the elevator is assigned to the user and more. We used the site to understand the process and adapt it to the offline algorithm.
Link:https://www.geeksforgeeks.org/smart-elevator-pro-geek-cup/

2. System Design — Elevator System Design Interview Question: On this site you can find a guide who plans an elevator system and also implements the actual solution, but it is important to note that these are regular elevators and not smart elevators, and yet you can get inspiration and motivation from the site.
Link:https://medium.com/geekculture/system-design-elevator-system-design-interview-question-6e8d03ce1b44

3. On-line Algorithms versus Off-line Algorithms for the Elevator: On this site you can find most of the differences between the online algorithm and the offline, in addition to an in-depth explanation of the problem space, solutions, actual algorithms and more.
Link:https://studylib.net/doc/7878746/on-line-algorithms-versus-off-line-algorithms-for-the-ele…

# Credits:
1. Mishell dubovitski.
2. Mark vertenberg.
3. Alina zakhozha.
