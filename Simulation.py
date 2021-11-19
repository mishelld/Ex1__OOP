import sys
import csv
import pygame
from Building import Building
from CallForElevator import CallForElevator

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
REFRESH_RATE = 60


def insertFiles():
    global files
    arguments = sys.argv
    try:
        files.append("inputs\\buildings\\" + arguments[1])
        files.append("inputs\\outputs\\" + arguments[2])
    except:
        defult = ["inputs\\buildings\\B5.json", "results\\output_5d.csv"]
        files = defult
        print("ERROR: missing files, inserted defult files instead")


def insertCalls(file):
    global calls
    with open(file, 'r') as f:
        data = csv.reader(f)
        for call in data:
            if isValidCall(call):
                objCall = CallForElevator(call)
                calls.append(objCall)
                objCall.setState(objCall.INIT)


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


def simulation():

    global building
    global elevators

    windowWidth = 100 * len((building.getElevators()))
    windowHeight = 300

    pygame.init()
    size = (windowWidth, windowHeight)
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    pygame.display.set_caption("OffLine Elevator simulation")

    space = 10
    width = 80
    finish = False
    while not finish:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
        currTime = pygame.time.get_ticks() / 1000.0
        addCallToSystem(currTime)
        print(currTime)
        screen.fill(WHITE)
        drawElevators(screen, currTime, space, width)
        pygame.display.flip()
        clock.tick(REFRESH_RATE)
    pygame.quit()


def drawElevators(screen, currTime, space, width):
    global elevators
    for e in elevators:
        updateCall(e)
        timeToPassFloor = 1.0 / e.getSpeed()
        x = e.getId() * 100 + space
        y = 100
        pygame.draw.rect(screen, BLACK, (x, y, width, 100), 5)
        diraction = drawDirection(screen, e, x, y, width)
        if e.getReset():
            e.setCounter(currTime)
            e.setReset(False)
        drawStickMan(screen, e, x, y)
        moveElevator(e, diraction, currTime, timeToPassFloor)
        drawCurrentFloor(screen, e, x, y, width)
        showId(screen, e.getId(), x, y, width)


def updateCall(elev):
    if len(elev.getCalls()) > 0:
        currCall = elev.getCalls()[0]
        if currCall.getState() == currCall.GOING2SRC:
            if elev.getPosition() == currCall.getSrc():
                currCall.setState(currCall.GOING2DEST)
        if currCall.getState() == currCall.GOING2DEST:
            if elev.getPosition() == currCall.getDest():
                currCall.setState(currCall.DONE)
        if currCall.getState() == currCall.DONE:
            elev.removeCall(currCall)


def moveElevator(elev, diraction, currTime, timeToPassFloor):
    if currTime - elev.getCounter() >= timeToPassFloor:
        currFloor = elev.getPosition()
        if diraction == 1:
            currFloor += 1
            elev.setPosition(currFloor)
        elif diraction == -1:
            currFloor -= 1
            elev.setPosition(currFloor)
        elev.setReset(True)


def showId(screen, id, x, y, width):
    font = pygame.font.Font('freesansbold.ttf', 14)
    numOfElev = font.render(str(id), True, BLACK)
    screen.blit(numOfElev, (x + width / 2 - 5, y + 110))


def drawCurrentFloor(screen, elev, x, y, width):
    font = pygame.font.Font('freesansbold.ttf', 48)
    numOfFloor = font.render(str(elev.getPosition()), True, BLACK)
    screen.blit(numOfFloor, (x + width / 2, y - 50))


def drawDirection(screen, elev, x, y, width):
    up = 1; down = -1; static = 0
    if len(elev.getCalls()) == 0:
        drawStatic(screen, x, y - 30, x + width / 2 - 10, y - 30)
        return static
    else:
        currCall = elev.getCalls()[0]
        if currCall.getState() == currCall.GOING2SRC:
            if elev.getPosition() < currCall.getSrc():
                drawUp(screen, x, y - 15, x + width / 2 - 10, y - 15, x + width / 4 - 5, y - 40)
                return up
            else:
                drawDown(screen, x, y - 40, x + width / 2 - 10, y - 40, x + width / 4 - 5, y - 15)
                return down
        elif currCall.getState() == currCall.GOING2DEST:
            if elev.getPosition() < currCall.getDest():
                drawUp(screen, x, y - 15, x + width / 2 - 10, y - 15, x + width / 4 - 5, y - 40)
                return up
            else:
                drawDown(screen, x, y - 40, x + width / 2 - 10, y - 40, x + width / 4 - 5, y - 15)
                return down
        else:
            drawStatic(screen, x, y - 30, x + width / 2 - 10, y - 30)
            return static

def drawStickMan(screen, elev, x, y):
    if len(elev.getCalls()) > 0:
        if elev.getCalls()[0].getState() == CallForElevator.GOING2DEST:
            filename = 'stickMan.png'
            picture = pygame.image.load(filename)
            picture = pygame.transform.scale(picture, (80, 100))
            screen.blit(picture, (x, y))

def drawUp(screen, x1, y1, x2, y2, x3, y3):
    pygame.draw.polygon(screen, GREEN, [[x1, y1], [x2, y2], [x3, y3]])


def drawDown(screen, x1, y1, x2, y2, x3, y3):
    pygame.draw.polygon(screen, RED, [[x1, y1], [x2, y2], [x3, y3]])


def drawStatic(screen, x1, y1, x2, y2):
    pygame.draw.line(screen, BLACK, (x1, y1), (x2, y2), 10)


def addCallToSystem(currTime):
    global calls
    global building
    for c in calls:
        if c.getTime() < currTime and c.getState() == c.INIT:
            c.setState(c.GOING2SRC)
            building.getElevators()[c.getAllocatedTo()].insertCall(c)
            print(c)


if __name__ == '__main__':
    files = []
    insertFiles()
    building = Building(files[0])
    elevators = building.getElevators()
    calls = []
    insertCalls(files[1])
    simulation()


