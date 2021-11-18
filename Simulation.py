import pygame
from Building import Building
from CallForElevator import CallForElevator

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 500

def insertFiles():
    global files
    arguments = sys.argv
    try:
        files.append("inputs\\buildings\\" + arguments[1])
        files.append("inputs\\outputs\\" + arguments[2])
    except:
        defult = ["inputs\\buildings\\B2.json", "results\\output_2a.csv"]
        files = defult
        print("ERROR: missing files, inserted defult files instead")

def simulation():
    global building
    pygame.init()
    size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Game")
    finish = False
    while not finish:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
    pygame.quit()

if __name__ == '__main__':
    files = []
    insertFiles(files)
    building = Building(files[0])
    print(building)
    simulation()


