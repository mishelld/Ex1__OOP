import csv
import sys
import subprocess
from Elevator import Elevator
from Building import Building
from CallForElevator import CallForElevator


def insertFiles():
    global files
    arguments = sys.argv
    try:
        files.append("inputs\\buildings\\" + arguments[1])
        files.append("inputs\\calls\\" + arguments[2])
        files.append("outputs\\" + arguments[3])
    except:
        defult = ["inputs\\buildings\\B5.json", "inputs\\calls\\Calls_d.csv", "outputs\\output_5d.csv"]
        files = defult
        print("ERROR: missing files, inserted defult files insted")
        
def insertCalls(file):
    global calls
    with open(file, 'r') as f:
        data = csv.reader(f)
        for call in data:
            if isValidCall(call):
                calls.append(CallForElevator(call))

def isValidCall(call):
    global building
    source = int(call[2])
    dest = int(call[3])
    if source > building.getMaxFloor() or source < building.getMinFloor():
        return False
    if dest > building.getMaxFloor() or dest < building.getMinFloor():
        return False
    return True

def algorithm():
    global calls
    global building
    elevators = building.getElevators()
    currTime = 0
    for c in calls:
        min = building.getElevators()[0]
        for e in elevators:
            e.removeDoneCalls(currTime)
            if min.timeToArrive(c) > e.timeToArrive(c):
                min = e
        min.addCall(c)
        c.setAllocatedTo(min, building)
        c.setFinishedTime(currTime + min.timeToArrive(c) + min.calculateSingleCallTime(c.getSrc(), c.getDest()))
        currTime = c.getTime()


def writeOutput(file):
    global calls
    data = []
    for c in calls:
        values = c.__dict__
        values.popitem()
        data.append(values.values())
    with open(file, 'w', newline='') as f:
        output = csv.writer(f)
        output.writerows(data)

def runTester(building, output):
    subprocess.Popen(["powershell.exe", "java -jar tester\\Ex1_checker_V1.2_obf.jar 1111,2222,3333 "+ building + "  "+ output + "  "+ output + "_tester.log"])


if __name__ == "__main__":
    files = [] 
    insertFiles()
    print("Files inserted")
    building = Building(files[0])
    print("Building inserted")
    calls = []
    insertCalls(files[1])
    print("Calls inserted")
    algorithm()
    print("passedAlgo")
    writeOutput(files[2])
    runTester(files[0], files[2])
    print("Done")
