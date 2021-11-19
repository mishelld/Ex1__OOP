import csv
import sys
import subprocess
from Elevator import Elevator
from Building import Building
from CallForElevator import CallForElevator

# a function that recivies the jason, and cvs files and then read its data.
def insertFiles():
    global files
    arguments = sys.argv
    try:
        files.append("inputs\\buildings\\" + arguments[1])
        files.append("inputs\\calls\\" + arguments[2])
        files.append("outputs\\" + arguments[3])
    except:
        defult = ["inputs\\buildings\\B3.json", "inputs\\calls\\Calls_b.csv", "outputs\\output_3b.csv"]
        files = defult
        print("ERROR: missing files, inserted defult files insted")

# a function that recivies a csv file and reads the data from the file
# and then inserts the data which is a call to an arraylist.      
def insertCalls(file):
    global calls
    with open(file, 'r') as f:
        data = csv.reader(f)
        for call in data:
            if isValidCall(call):
                calls.append(CallForElevator(call))

# a function that checks if the call that is recived from the file is valid.
def isValidCall(call):
    global building
    source = int(call[2])
    dest = int(call[3])
    if source > building.getMaxFloor() or source < building.getMinFloor():
        return False
    if dest > building.getMaxFloor() or dest < building.getMinFloor():
        return False
    return True

# For each call in call's list finds the best elevator,
# by selecting the elevator with the shortes time arriving to the call.
def OffLineAlgorithm():
    global calls
    global building
    elevators = building.getElevators()
    currTime = 0 # Our Time tracker
    for c in calls:
        # Finding the elevator with the shortes time to arrive to thr call, and set it to min
        min = building.getElevators()[0]
        for e in elevators:
            # Removing all the done calls from this elevator's list of calls.
            e.removeDoneCalls(currTime) 
            if min.timeToArrive(c) > e.timeToArrive(c):
                min = e
        # Adds the call to min's list of calls.
        min.insertCall(c)
        # Allocate this call to min
        c.setAllocatedTo(min, building)
        # Update the finised time of this call.
        c.setFinishedTime(currTime + min.timeToArrive(c) + min.calculateSingleCallTime(c.getSrc(), c.getDest()))
        # Update our current time.
        currTime = c.getTime() 

# a function that writes the output file.
def writeOutput(file):
    global calls
    input = []
    for c in calls:
        values = c.__dict__
        values.popitem()
        input.append(values.values())
    with open(file, 'w', newline='') as f:
        output = csv.writer(f)
        output.writerows(input)

# Runs the jar file for testing 
def test(building, output):
    subprocess.Popen(["powershell.exe", "java -jar tester\\Ex1_checker_V1.2_obf.jar 212471551,211886494,323431965 "+ building + "  "+ output + "  "+ output + "_tester.log"])

# Main function
if __name__ == "__main__":
    files = [] 
    # Insert the files to list.
    insertFiles()
    building = Building(files[0])
    calls = []
    # insert calls from the file.
    insertCalls(files[1])
    # Run the algorithm.
    OffLineAlgorithm()
    # Write to output file the calls.
    writeOutput(files[2])
    # Run the tester.
    test(files[0], files[2])
    print("DONE")
